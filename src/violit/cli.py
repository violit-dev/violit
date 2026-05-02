"""
violit/cli.py
=============
Violit Command Line Interface.
"""

import argparse
import os
import sys
import runpy
from pathlib import Path
import textwrap

def run_app(args, unknown_args):
    """
    Execute the target script.
    Passes any unknown_args to the script so App.run() can parse them (e.g. --reload, --make-migration).
    """
    script_path = os.path.abspath(args.script)
    script_dir = os.path.dirname(script_path)
    
    if not os.path.exists(script_path):
        print(f"Error: Script '{script_path}' does not exist.", file=sys.stderr)
        sys.exit(1)
        
    # Rewrite sys.argv so the target script sees itself as the main executable
    sys.argv = [script_path] + unknown_args
    original_sys_path = list(sys.path)
    if script_dir:
        sys.path.insert(0, script_dir)
    
    # Run the script as __main__
    try:
        runpy.run_path(script_path, run_name="__main__")
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error running '{script_path}': {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        sys.path[:] = original_sys_path

def create_project(args):
    """
    Create a new violit project boilerplate.
    """
    project_name = args.name
    project_dir = Path(project_name)
    
    if project_dir.exists():
        print(f"Error: Directory '{project_name}' already exists.", file=sys.stderr)
        sys.exit(1)
        
    project_dir.mkdir(parents=True)
    
    # 1. main.py
    main_py_content = textwrap.dedent("""\
        import violit as vl

        app = vl.App(title="My Violit App", theme="ocean")

        def home_page():
            app.title("Welcome to Violit")
            app.text("This is your new project.")
            
            count = app.state(0)
            app.button("Click me!", on_click=lambda: count.set(count.value + 1))
            app.text(lambda: f"Button clicked {count.value} times.")

        def settings_page():
            app.title("Settings")
            theme = app.selectbox("Theme", ["ocean", "dark", "light", "cyberpunk"])
            app.button("Apply Theme", on_click=lambda: app.set_theme(theme.value))

        # Setup sidebar and navigation
        with app.sidebar:
            app.markdown("## Navigation")

        app.navigation([
            vl.Page(home_page, title="Home", icon="house"),
            vl.Page(settings_page, title="Settings", icon="gear"),
        ])

        if __name__ == "__main__":
            app.run()
    """)
    (project_dir / "main.py").write_text(main_py_content, encoding="utf-8")
    
    # 2. requirements.txt
    req_content = textwrap.dedent("""\
        violit>=0.6.9
    """)
    (project_dir / "requirements.txt").write_text(req_content, encoding="utf-8")
    
    # 3. .gitignore
    gitignore_content = textwrap.dedent("""\
        __pycache__/
        *.py[cod]
        *$py.class
        .venv/
        venv/
        *.db
        .env
        alembic.ini
        migrations/
    """)
    (project_dir / ".gitignore").write_text(gitignore_content, encoding="utf-8")
    
    # 4. README.md
    readme_content = textwrap.dedent(f"""\
        # {project_name}

        A new web application built with [Violit](https://github.com/violit-dev/violit).

        ## How to run

        ```bash
        pip install -r requirements.txt
        violit run main.py --reload
        ```
    """)
    (project_dir / "README.md").write_text(readme_content, encoding="utf-8")
    
    print(f"[Success] Created Violit project '{project_name}' successfully!")
    print(f"\nNext steps:")
    print(f"  cd {project_name}")
    print(f"  violit run main.py --reload\n")

def main():
    parser = argparse.ArgumentParser(
        prog="violit",
        description="Violit CLI - Pure Python Web Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              violit create my_app
              violit run app.py
              violit run app.py --reload --localhost
              violit run app.py --help
        """)
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 1. violit run <script> [args...]
    run_parser = subparsers.add_parser(
        "run",
        help="Run a Violit script",
        description=textwrap.dedent("""\
            Run a Violit script.

            Any arguments after the script path are passed directly to app.run().
            That means the same runtime flags work in both styles:

              python app.py --reload --localhost
              violit run app.py --reload --localhost
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Common examples:
              violit run app.py
              violit run app.py --reload
              violit run app.py --reload --localhost
              violit run app.py --port 8010
              violit run app.py --native
              violit run app.py --lite
              violit run app.py --make-migration "add_users"
              violit run app.py --help
        """)
    )
    run_parser.add_argument("script", help="Path to the python script (e.g. main.py)")
    run_parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        metavar="APP_ARGS",
        help="Arguments passed directly to app.run() (for example: --reload --localhost --port 8010)"
    )
    
    # 2. violit create <project_name>
    create_parser = subparsers.add_parser("create", help="Create a new violit project")
    create_parser.add_argument("name", help="Name of the new project directory")

    args = parser.parse_args()

    if args.command == "run":
        run_app(args, args.args)
    elif args.command == "create":
        create_project(args)

if __name__ == "__main__":
    main()
