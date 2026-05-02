import argparse
import inspect
import logging
import os
import secrets
import subprocess
import sys
import threading
import time

import uvicorn

from .app_support import FileWatcher, print_terminal_splash


class AppLauncherMixin:
    @staticmethod
    def _normalize_host_arg(args):
        if getattr(args, "localhost", False) or args.host == "localhost":
            args.host = "127.0.0.1"

    @staticmethod
    def _get_web_launch_urls(host, port):
        local_url = f"http://localhost:{port}"

        if host in ("127.0.0.1", "localhost"):
            return local_url, None

        if host == "0.0.0.0":
            import socket

            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                    sock.connect(("8.8.8.8", 80))
                    local_ip = sock.getsockname()[0]
            except Exception:
                local_ip = None

            return local_url, f"http://{local_ip}:{port}" if local_ip else None

        return local_url, f"http://{host}:{port}"

    def _print_web_launch_urls(self, host, port, reload_tag=""):
        local_url, network_url = self._get_web_launch_urls(host, port)

        print("")
        print("  You can now view your Violit app in your browser.")
        print("")
        print(f"  Local URL:   {local_url}{reload_tag}")
        if network_url:
            label = "Network URL:" if host == "0.0.0.0" else "Server URL:"
            print(f"  {label} {network_url}{reload_tag}")
        print("")

    def _run_web_reload(self, args):
        """Run with hot reload in web mode using uvicorn's native reload"""
        self.debug_print(f"[HOT RELOAD] Starting with uvicorn native reload...")

        frame = inspect.currentframe()
        app_var_name = None
        module_string = None
        file_path = None

        try:
            while frame:
                if frame.f_code.co_name == "<module>":
                    file_path = frame.f_globals.get("__file__")
                    if file_path:
                        module_string = os.path.splitext(os.path.basename(file_path))[0]

                        for name, obj in frame.f_globals.items():
                            if obj is self:
                                app_var_name = name
                                break

                        if app_var_name:
                            break
                frame = frame.f_back
        finally:
            del frame

        def _run_subprocess_reload(script_path):
            watch_dir = os.path.dirname(os.path.abspath(script_path)) if script_path else os.getcwd()
            self.debug_print(f"[HOT RELOAD] Falling back to subprocess reload watcher for {watch_dir}")
            print(f"INFO:     Violit web app running on http://localhost:{args.port} (hot reload)")
            print(f"INFO:     (listening on all interfaces: 0.0.0.0:{args.port})")

            is_unix = sys.platform != 'win32'
            popen_kwargs = {}
            if is_unix:
                popen_kwargs['start_new_session'] = True

            child = None

            def _terminate_process(proc):
                try:
                    if is_unix:
                        import signal
                        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                    else:
                        proc.terminate()
                except (ProcessLookupError, OSError):
                    pass

            def _kill_process(proc):
                try:
                    if is_unix:
                        import signal
                        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                    else:
                        proc.kill()
                except (ProcessLookupError, OSError):
                    pass

            try:
                while True:
                    env = os.environ.copy()
                    env["VIOLIT_WORKER"] = "1"

                    self.debug_print("[HOT RELOAD] Starting child server process...", flush=True)
                    child = subprocess.Popen([sys.executable] + sys.argv, env=env, **popen_kwargs)
                    time.sleep(0.3)

                    watcher = FileWatcher(watch_dir=watch_dir, debug_mode=self.debug_mode)
                    intentional_restart = False

                    while child.poll() is None:
                        if watcher.check():
                            self.debug_print("\n[HOT RELOAD] File change detected. Restarting server...", flush=True)
                            intentional_restart = True
                            _terminate_process(child)
                            try:
                                child.wait(timeout=2)
                            except subprocess.TimeoutExpired:
                                _kill_process(child)
                                child.wait()
                            break
                        time.sleep(0.5)

                    if intentional_restart:
                        time.sleep(0.3)
                        continue

                    self.debug_print("[HOT RELOAD] Child server exited. Waiting for file changes...", flush=True)
                    while not watcher.check():
                        time.sleep(0.5)
            except KeyboardInterrupt:
                if child and child.poll() is None:
                    _terminate_process(child)
                    try:
                        child.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        _kill_process(child)
                print("INFO:     Stopping reloader process")
                return

        if sys.platform == 'win32':
            self.debug_print("[HOT RELOAD] Windows detected; using subprocess-based reload watcher.")
            _run_subprocess_reload(file_path or sys.argv[0])
            return

        if app_var_name and module_string:
            uvicorn_target = f"{module_string}:{app_var_name}.fastapi"
            self.debug_print(f"[HOT RELOAD] Delegating to uvicorn -> {uvicorn_target}")

            reload_dir = os.path.dirname(os.path.abspath(file_path)) if file_path else os.getcwd()

            if reload_dir not in sys.path:
                sys.path.insert(0, reload_dir)

            os.environ["VIOLIT_WORKER"] = "1"
            os.environ["VIOLIT_UVICORN_RELOAD"] = "1"

            class _SuppressUvicornRunningFilter(logging.Filter):
                def filter(self, record):
                    return 'Uvicorn running on' not in record.getMessage()
            logging.getLogger("uvicorn.error").addFilter(_SuppressUvicornRunningFilter())

            try:
                self._print_web_launch_urls(args.host, args.port, " (hot reload)")

                uvicorn.run(
                    uvicorn_target,
                    host=args.host,
                    port=args.port,
                    ws_ping_interval=None,
                    ws_ping_timeout=None,
                    reload=True,
                    reload_dirs=[reload_dir],
                    reload_includes=["*.py"],
                    reload_delay=0.1
                )
            except Exception as exc:
                self.debug_print(f"[HOT RELOAD] Failed to start uvicorn: {exc}")
                sys.exit(1)
        else:
            self.debug_print("[HOT RELOAD] Could not dynamically resolve a module-level App instance.")
            self.debug_print("[HOT RELOAD] Falling back to subprocess-based reloader.")
            _run_subprocess_reload(file_path or sys.argv[0])

    def _run_native_reload(self, args):
        """Run with hot reload in desktop mode"""
        import webview

        self.native_token = secrets.token_urlsafe(32)
        self.is_native_mode = True

        script_dir = os.path.dirname(os.path.abspath(sys.argv[0])) or os.getcwd()
        self.debug_print(f"[HOT RELOAD] Desktop mode - Watching {script_dir}...")

        is_unix = sys.platform != 'win32'

        server_process = [None]
        should_exit = [False]

        def _terminate_process(proc):
            try:
                if is_unix:
                    import signal
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                else:
                    proc.terminate()
            except (ProcessLookupError, OSError):
                pass

        def _kill_process(proc):
            try:
                if is_unix:
                    import signal
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                else:
                    proc.kill()
            except (ProcessLookupError, OSError):
                pass

        def server_manager():
            iteration = 0
            while not should_exit[0]:
                iteration += 1
                env = os.environ.copy()
                env["VIOLIT_WORKER"] = "1"
                env["VIOLIT_SERVER_ONLY"] = "1"
                env["VIOLIT_NATIVE_TOKEN"] = self.native_token
                env["VIOLIT_NATIVE_MODE"] = "1"

                self.debug_print(f"\n[Server Manager] Starting server (iteration {iteration})...", flush=True)
                popen_kwargs = {}
                if is_unix:
                    popen_kwargs['start_new_session'] = True
                server_process[0] = subprocess.Popen(
                    [sys.executable] + sys.argv,
                    env=env,
                    stdout=subprocess.PIPE if iteration > 1 else None,
                    stderr=subprocess.STDOUT if iteration > 1 else None,
                    **popen_kwargs
                )

                time.sleep(0.3)

                watcher = FileWatcher(watch_dir=script_dir, debug_mode=self.debug_mode)
                intentional_restart = False
                while server_process[0].poll() is None and not should_exit[0]:
                    if watcher.check():
                        self.debug_print("\n[Server Manager] Reloading server...", flush=True)
                        intentional_restart = True
                        _terminate_process(server_process[0])
                        try:
                            server_process[0].wait(timeout=2)
                            self.debug_print("[Server Manager] Server stopped gracefully", flush=True)
                        except subprocess.TimeoutExpired:
                            self.debug_print("[Server Manager] WARNING: Force killing server...", flush=True)
                            _kill_process(server_process[0])
                            server_process[0].wait()
                        break
                    time.sleep(0.5)

                if intentional_restart:
                    time.sleep(0.5)
                    try:
                        if webview.windows:
                            webview.windows[0].load_url(f"http://127.0.0.1:{args.port}?_native_token={self.native_token}")
                            self.debug_print("[Server Manager] ✓ Webview reloaded", flush=True)
                    except Exception as exc:
                        self.debug_print(f"[Server Manager] ⚠ Webview reload failed: {exc}", flush=True)
                    continue

                if server_process[0].poll() is not None and not should_exit[0]:
                    self.debug_print("[Server Manager] WARNING: Server exited unexpectedly. Waiting for file changes...", flush=True)
                    while not watcher.check() and not should_exit[0]:
                        time.sleep(0.5)

        thread = threading.Thread(target=server_manager, daemon=True)
        thread.start()

        self._patch_webview_icon()

        win_args = {
            'text_select': True,
            'width': self.width,
            'height': self.height,
            'on_top': self.on_top,
        }

        start_args = {}
        sig_start = inspect.signature(webview.start)
        if 'icon' in sig_start.parameters and self.app_icon:
            start_args['icon'] = self.app_icon

        window = webview.create_window(self.app_title, f"http://127.0.0.1:{args.port}?_native_token={self.native_token}", **win_args)

        def _bring_to_front_reload():
            try:
                import ctypes
                hwnd = window.gui
                ctypes.windll.user32.SwitchToThisWindow(hwnd, True)
            except Exception:
                pass
        window.events.shown += _bring_to_front_reload
        webview.start(**start_args)

        should_exit[0] = True
        if server_process[0]:
            try:
                _terminate_process(server_process[0])
            except Exception:
                pass
        sys.exit(0)

    def run(self, port: int = None):
        """Run the application"""
        parser = argparse.ArgumentParser()
        parser.add_argument("--native", action="store_true")
        parser.add_argument("--nosplash", action="store_true", help="Disable splash screen")
        parser.add_argument("--reload", action="store_true", help="Enable hot reload")
        parser.add_argument("--lite", action="store_true", help="Use Lite mode (HTMX)")
        parser.add_argument("--debug", action="store_true", help="Enable developer tools (native mode)")
        parser.add_argument("--on-top", action="store_true", help="Keep window always on top (native mode)")
        parser.add_argument("--port", type=int, default=8000)
        parser.add_argument("--host", type=str, default="0.0.0.0", help="Host address to bind to (e.g. 0.0.0.0, 127.0.0.1)")
        parser.add_argument("--localhost", action="store_true", help="Bind to 127.0.0.1 and show localhost URLs")
        parser.add_argument("--make-migration", metavar="MSG", default=None,
                            help="Generate Alembic migration file and exit (requires migrate='files' mode)")
        parser.add_argument("--apply", action="store_true",
                            help="Apply pending Alembic migrations and exit")
        parser.add_argument("--rollback", type=int, metavar="N", nargs="?", const=1, default=None,
                            help="Rollback N steps of Alembic migrations and exit")
        args, _ = parser.parse_known_args()
        if port is not None:
            args.port = port
        self._normalize_host_arg(args)

        if self.db is not None:
            if args.make_migration is not None:
                self.db.make_migration(args.make_migration)
                return
            if args.apply:
                self.db.apply()
                return
            if args.rollback is not None:
                self.db.rollback(steps=args.rollback)
                return
        if args.on_top:
            self.on_top = True

        if os.environ.get("VIOLIT_UVICORN_RELOAD"):
            self.debug_print("[HOT RELOAD] Uvicorn reload child/import detected; skipping nested app.run()")
            return

        try:
            class PollingFilter(logging.Filter):
                def filter(self, record: logging.LogRecord) -> bool:
                    return "/?_t=" not in record.getMessage()

            logging.getLogger("uvicorn.access").addFilter(PollingFilter())

            if not args.debug:
                class StaticResourceFilter(logging.Filter):
                    def filter(self, record: logging.LogRecord) -> bool:
                        return "/static/vendor/" not in record.getMessage()
                logging.getLogger("uvicorn.access").addFilter(StaticResourceFilter())
        except Exception:
            pass

        if self.db is not None:
            try:
                self.db._run_startup_migration()
            except Exception as db_exc:
                import logging as db_logging
                db_logging.getLogger("violit.db").error(
                    f"[violit:db] Migration error during startup: {db_exc}"
                )

        if args.lite:
            self.mode = "lite"
            if self.lite_engine is None:
                from .engine import LiteEngine
                self.lite_engine = LiteEngine()

        is_server_only = bool(os.environ.get("VIOLIT_SERVER_ONLY"))
        if is_server_only:
            args.native = False

        if args.nosplash:
            os.environ["VIOLIT_NOSPLASH"] = "1"

        if not args.nosplash and not os.environ.get("VIOLIT_WORKER") and not is_server_only:
            print_terminal_splash()

        if args.reload and not os.environ.get("VIOLIT_WORKER"):
            if args.native:
                self._run_native_reload(args)
            else:
                self._run_web_reload(args)
            return

        if args.native:
            import webview

            self.native_token = secrets.token_urlsafe(32)
            self.is_native_mode = True
            self.csrf_enabled = False
            server_shutdown = threading.Event()

            @self.fastapi.on_event("startup")
            async def _on_native_startup():
                class _SuppressUvicornRunningFilter(logging.Filter):
                    def filter(self, record):
                        return 'Uvicorn running on' not in record.getMessage()

                class _Suppress403Filter(logging.Filter):
                    def filter(self, record):
                        return '403' not in record.getMessage()

                logging.getLogger("uvicorn.error").addFilter(_SuppressUvicornRunningFilter())
                logging.getLogger("uvicorn.access").addFilter(_Suppress403Filter())
                print(f"INFO:     Violit desktop app running on port {args.port}")

            def srv():
                uvicorn.run(
                    self.fastapi,
                    host="127.0.0.1",
                    port=args.port,
                    ws_ping_interval=None,
                    ws_ping_timeout=None,
                )

            thread = threading.Thread(target=srv, daemon=True)
            thread.start()

            self._patch_webview_icon()

            win_args = {
                'text_select': True,
                'width': self.width,
                'height': self.height,
                'on_top': self.on_top,
            }

            start_args = {}
            sig_start = inspect.signature(webview.start)

            if args.debug:
                start_args['debug'] = True
                print("INFO:     Debug mode enabled: Press F12 or Ctrl+Shift+I to open developer tools")

            if 'icon' in sig_start.parameters and self.app_icon:
                start_args['icon'] = self.app_icon

            window = webview.create_window(self.app_title, f"http://127.0.0.1:{args.port}?_native_token={self.native_token}", **win_args)

            def _bring_to_front():
                try:
                    import ctypes
                    hwnd = window.gui
                    ctypes.windll.user32.SwitchToThisWindow(hwnd, True)
                except Exception:
                    pass
            window.events.shown += _bring_to_front
            webview.start(**start_args)

            print("App closed. Exiting...")
            os._exit(0)
        elif is_server_only:
            @self.fastapi.on_event("startup")
            async def _on_native_reload_startup():
                class _SuppressForbiddenAndRunningFilter(logging.Filter):
                    def filter(self, record):
                        msg = record.getMessage()
                        return '403' not in msg and 'Uvicorn running on' not in msg
                logging.getLogger("uvicorn.access").addFilter(_SuppressForbiddenAndRunningFilter())
                logging.getLogger("uvicorn.error").addFilter(_SuppressForbiddenAndRunningFilter())
                print(f"INFO:     Violit desktop app running on port {args.port} (hot reload)")
            uvicorn.run(
                self.fastapi,
                host=args.host,
                port=args.port,
                ws_ping_interval=None,
                ws_ping_timeout=None,
            )
        else:
            class _SuppressUvicornRunningFilter(logging.Filter):
                def filter(self, record):
                    return 'Uvicorn running on' not in record.getMessage()

            logging.getLogger("uvicorn.error").addFilter(_SuppressUvicornRunningFilter())

            reload_tag = " (hot reload)" if args.reload else ""
            self._print_web_launch_urls(args.host, args.port, reload_tag)

            uvicorn.run(
                self.fastapi,
                host=args.host,
                port=args.port,
                ws_ping_interval=None,
                ws_ping_timeout=None,
            )