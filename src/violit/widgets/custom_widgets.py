"""Custom widget registry mixin for Violit."""

from __future__ import annotations

from dataclasses import dataclass, field
import html
import inspect
import json
import keyword
import re
from types import MethodType
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, Mapping, Optional, Protocol, cast

from ..app_runtime import _invoke_action_callback
from ..component import Component
from ..context import rendering_ctx
from ..state import ComputedState, State
from ..style_utils import merge_cls, merge_style


if TYPE_CHECKING:
    class _CustomWidgetAppProtocol(Protocol):
        _custom_widget_registry: Dict[str, Any]
        _custom_widget_exposed_methods: Dict[str, str]
        static_builders: Dict[str, Callable]
        static_order: list[str]

        def _get_next_cid(self, prefix: str) -> str: ...
        def _resolve_widget_cid(self, prefix: str, key: Any = None) -> str: ...
        def _register_component(self, cid: str, builder: Callable, action: Optional[Callable] = None): ...
        def _get_widget_defaults(self, widget_type: str) -> Dict[str, Any]: ...


def _sanitize_custom_widget_key(value: Any) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "_", str(value)).strip("_") or "widget"


def _normalize_init_names(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        names = value.split()
    elif isinstance(value, Iterable):
        names = []
        for item in value:
            names.extend(str(item).split())
    else:
        names = str(value).split()
    return tuple(name.strip() for name in names if str(name).strip())


def _coerce_widget_payload(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    stripped = value.strip()
    if not stripped:
        return value
    if stripped.startswith("{") or stripped.startswith("["):
        try:
            return json.loads(stripped)
        except Exception:
            return value
    return value


def _resolve_widget_prop_value(value: Any) -> Any:
    if isinstance(value, (State, ComputedState)):
        return value.value
    if callable(value) and not inspect.isclass(value):
        try:
            signature = inspect.signature(value)
        except (TypeError, ValueError):
            signature = None

        if signature is None or all(
            parameter.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
            or parameter.default is not inspect.Parameter.empty
            for parameter in signature.parameters.values()
        ):
            return _resolve_widget_prop_value(value())
    return value


def _normalize_external_asset_urls(value: Any) -> tuple[str, ...]:
        if value is None:
                return ()
        if isinstance(value, str):
                items = [value]
        elif isinstance(value, Iterable):
                items = [str(item) for item in value]
        else:
                items = [str(value)]
        return tuple(item.strip() for item in items if str(item).strip())


def _build_js_widget_assets(
        initializer_name: str,
        mount_js: str,
        *,
        js_urls: tuple[str, ...],
        css_urls: tuple[str, ...],
) -> str:
        css_tags = "\n".join(
                f'<link rel="stylesheet" href={json.dumps(url, ensure_ascii=False)} />' for url in css_urls
        )
        js_tags = "\n".join(
                f'<script src={json.dumps(url, ensure_ascii=False)}></script>' for url in js_urls
        )
        initializer_literal = json.dumps(initializer_name, ensure_ascii=False)
        mount_js_literal = json.dumps(mount_js, ensure_ascii=False)

        script = f"""
        <script>
            (function() {{
                if (!window.__vlRegisteredJsWidgets) {{
                    window.__vlRegisteredJsWidgets = {{}};
                }}

                function destroyJsWidgetNode(node) {{
                    if (!(node instanceof Element)) return;

                    if (typeof node.__vlJsWidgetDestroy === 'function') {{
                        try {{
                            node.__vlJsWidgetDestroy();
                        }} catch (error) {{
                            console.error('register_js_widget destroy() failed', error);
                        }}
                    }}

                    node.__vlJsWidgetDestroy = null;
                    node.__vlJsWidgetController = null;

                    node.querySelectorAll('*').forEach(function(child) {{
                        if (typeof child.__vlJsWidgetDestroy === 'function') {{
                            try {{
                                child.__vlJsWidgetDestroy();
                            }} catch (error) {{
                                console.error('register_js_widget destroy() failed', error);
                            }}
                        }}
                        child.__vlJsWidgetDestroy = null;
                        child.__vlJsWidgetController = null;
                    }});
                }}

                if (!window.__vlJsWidgetCleanupObserver) {{
                    window.__vlJsWidgetCleanupObserver = new MutationObserver(function(records) {{
                        records.forEach(function(record) {{
                            record.removedNodes.forEach(destroyJsWidgetNode);
                        }});
                    }});
                    window.__vlJsWidgetCleanupObserver.observe(document.documentElement, {{ childList: true, subtree: true }});
                }}

                function boot(attempts) {{
                    if (!window.violitRuntime || typeof window.violitRuntime.registerInitializer !== 'function') {{
                        if (attempts < 80) setTimeout(function() {{ boot(attempts + 1); }}, 50);
                        return;
                    }}

                    const initializerName = {initializer_literal};
                    if (window.__vlRegisteredJsWidgets[initializerName]) {{
                        return;
                    }}
                    window.__vlRegisteredJsWidgets[initializerName] = true;

                    const runtime = window.violitRuntime;
                    const mount = new Function('element', 'props', 'emit', {mount_js_literal});

                    runtime.registerInitializer(initializerName, function(element) {{
                        const config = runtime.readJsonAttr(element, 'data-cw-js-widget-config', null);
                        if (!config || typeof config !== 'object') {{
                            return;
                        }}

                        const props = config.props || {{}};
                        const events = config.events || {{}};
                        const emit = function(eventName, value) {{
                            const cid = events[eventName];
                            if (!cid || !window.violitRuntime || typeof window.violitRuntime.emitAction !== 'function') {{
                                return;
                            }}
                            window.violitRuntime.emitAction(cid, value);
                        }};

                        let controller = element.__vlJsWidgetController;
                        if (!controller) {{
                            try {{
                                controller = mount(element, props, emit) || {{}};
                            }} catch (error) {{
                                console.error('register_js_widget mount() failed', error);
                                return;
                            }}
                            element.__vlJsWidgetController = controller;
                            element.__vlJsWidgetDestroy = controller && typeof controller.destroy === 'function' ? controller.destroy.bind(controller) : null;
                            return;
                        }}

                        if (typeof controller.update === 'function') {{
                            try {{
                                controller.update(props);
                            }} catch (error) {{
                                console.error('register_js_widget update() failed', error);
                            }}
                            return;
                        }}

                        if (typeof element.__vlJsWidgetDestroy === 'function') {{
                            try {{
                                element.__vlJsWidgetDestroy();
                            }} catch (error) {{
                                console.error('register_js_widget destroy() failed', error);
                            }}
                        }}

                        try {{
                            controller = mount(element, props, emit) || {{}};
                        }} catch (error) {{
                            console.error('register_js_widget remount() failed', error);
                            return;
                        }}
                        element.__vlJsWidgetController = controller;
                        element.__vlJsWidgetDestroy = controller && typeof controller.destroy === 'function' ? controller.destroy.bind(controller) : null;
                    }});

                    document.querySelectorAll('[data-vl-init="' + initializerName + '"]').forEach(function(element) {{
                        runtime.initElement(element);
                    }});
                }}

                boot(0);
            }})();
        </script>
        """.strip()
        return "\n".join(part for part in (css_tags, js_tags, script) if part)


@dataclass(slots=True)
class CustomWidgetResult:
    content: str
    attrs: Dict[str, Any] = field(default_factory=dict)
    cls: str = ""
    style: str = ""
    tag: str = "div"


@dataclass(slots=True)
class _CustomWidgetDefinition:
    name: str
    render: Callable[..., Any]
    initializer_names: tuple[str, ...] = ()
    events: tuple[str, ...] = ()
    assets: Any = None
    exposed_method_name: str | None = None


@dataclass(slots=True)
class CustomWidgetContext:
    app: Any
    name: str
    cid: str
    event_cids: Dict[str, str]
    props: Dict[str, Any]

    def event_cid(self, event_name: str) -> str:
        return self.event_cids.get(event_name, "")

    @staticmethod
    def json_attr(payload: Any) -> str:
        return html.escape(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), quote=True)


def _normalize_custom_widget_result(value: Any) -> CustomWidgetResult:
    if isinstance(value, CustomWidgetResult):
        return value
    if isinstance(value, Component):
        props = dict(value.props)
        content = str(props.pop("content", ""))
        props.pop("id", None)
        return CustomWidgetResult(
            content=content,
            attrs=props,
            tag=value.tag or "div",
        )
    return CustomWidgetResult(content=str(value))


class CustomWidgetsMixin:
    def register_js_widget(
        self,
        name: str,
        *,
        mount_js: str,
        js: Optional[Any] = None,
        css: Optional[Any] = None,
        tag: str = "div",
        events: Optional[Iterable[str]] = None,
        expose_method: bool = True,
    ):
        """Register a JS-backed widget with a small declarative API.

        The supplied mount_js runs in the browser with arguments:
            element: host DOM element
            props: JSON-serializable props passed from Python
            emit: function(eventName, value)

        The script may return an object with optional update(nextProps) and destroy() methods.
        """
        widget_tag = str(tag or "div").strip() or "div"
        mount_source = str(mount_js or "").strip()
        if not mount_source:
            raise ValueError("register_js_widget() mount_js cannot be empty.")

        initializer_name = f"cw-js-widget-{_sanitize_custom_widget_key(name)}"
        js_urls = _normalize_external_asset_urls(js)
        css_urls = _normalize_external_asset_urls(css)
        normalized_events = ("change",) if events is None else tuple(events)

        def render_js_widget(ctx: CustomWidgetContext, **props):
            config = json.dumps(
                {
                    "props": props,
                    "events": {event_name: ctx.event_cid(event_name) for event_name in normalized_events},
                },
                ensure_ascii=False,
                separators=(",", ":"),
            )
            return CustomWidgetResult(
                content="",
                attrs={"data_cw_js_widget_config": config},
                tag=widget_tag,
            )

        return self.register_widget(
            name,
            render_js_widget,
            initializer=initializer_name,
            events=normalized_events,
            assets=_build_js_widget_assets(
                initializer_name,
                mount_source,
                js_urls=js_urls,
                css_urls=css_urls,
            ),
            expose_method=expose_method,
        )

    def register_widget(
        self,
        name: str,
        render: Callable[..., Any],
        *,
        initializer: Optional[Any] = None,
        events: Optional[Iterable[str]] = None,
        assets: Any = None,
        expose_method: bool = False,
    ):
        """Register a project-local custom widget definition.

        Args:
            name: Widget name used by app.widget(name, ...)
            render: Callable with signature render(ctx, **props)
            initializer: One or more data-vl-init initializer names for the widget host
            events: Event names exposed as on_<event> callback props at use time
            assets: Optional raw HTML bootstrap string inserted once at app level
            expose_method: If True, expose this widget as app.<name>(**props)
        """
        app_self = cast("_CustomWidgetAppProtocol", self)
        widget_name = str(name or "").strip()
        if not widget_name:
            raise ValueError("register_widget() name cannot be empty.")
        if not callable(render):
            raise TypeError("register_widget() render must be callable.")
        if widget_name in app_self._custom_widget_registry:
            raise ValueError(f"Custom widget '{widget_name}' is already registered.")

        if events is None:
            normalized_events: tuple[str, ...] = ()
        else:
            normalized_events = tuple(
                event_name.strip()
                for event_name in (events.keys() if isinstance(events, Mapping) else events)
                if str(event_name).strip()
            )

        definition = _CustomWidgetDefinition(
            name=widget_name,
            render=render,
            initializer_names=_normalize_init_names(initializer),
            events=normalized_events,
            assets=assets,
            exposed_method_name=widget_name if expose_method else None,
        )
        app_self._custom_widget_registry[widget_name] = definition
        self._register_custom_widget_assets(definition)
        if expose_method:
            self._install_custom_widget_method(definition)
        return self

    def _install_custom_widget_method(self, definition: _CustomWidgetDefinition):
        app_self = cast("_CustomWidgetAppProtocol", self)
        method_name = definition.exposed_method_name or ""
        if not method_name:
            return
        if not method_name.isidentifier() or keyword.iskeyword(method_name):
            raise ValueError(
                f"Custom widget '{definition.name}' cannot be exposed as a method because '{method_name}' is not a valid Python identifier."
            )

        existing_owner = app_self._custom_widget_exposed_methods.get(method_name)
        if existing_owner and existing_owner != definition.name:
            raise ValueError(
                f"Custom widget method '{method_name}' is already exposed by widget '{existing_owner}'."
            )

        if hasattr(self, method_name) and existing_owner is None:
            raise ValueError(
                f"Cannot expose custom widget '{definition.name}' as app.{method_name}() because that attribute already exists."
            )

        def exposed_widget_method(app_self, *args, **kwargs):
            if args:
                raise TypeError(
                    f"app.{method_name}() accepts keyword arguments only. Use app.{method_name}(key=..., ...)."
                )
            return app_self.widget(definition.name, **kwargs)

        exposed_widget_method.__name__ = method_name
        exposed_widget_method.__qualname__ = method_name
        exposed_widget_method.__doc__ = f"Expose custom widget '{definition.name}' via app.{method_name}(**props)."
        setattr(self, method_name, MethodType(exposed_widget_method, self))
        app_self._custom_widget_exposed_methods[method_name] = definition.name

    def _register_custom_widget_assets(self, definition: _CustomWidgetDefinition):
        app_self = cast("_CustomWidgetAppProtocol", self)
        if definition.assets is None:
            return

        cid = f"custom_widget_assets_{_sanitize_custom_widget_key(definition.name)}"

        def builder():
            raw_assets = definition.assets() if callable(definition.assets) else definition.assets
            if isinstance(raw_assets, (list, tuple)):
                content = "\n".join(str(part) for part in raw_assets if part is not None)
            else:
                content = "" if raw_assets is None else str(raw_assets)
            return Component("div", id=cid, style="display:none", content=content)

        app_self.static_builders[cid] = builder
        if cid not in app_self.static_order:
            app_self.static_order.append(cid)

    def widget(self, name: str, *, key: Optional[Any] = None, cls: str = "", style: str = "", **props):
        """Render a registered custom widget."""
        app_self = cast("_CustomWidgetAppProtocol", self)
        definition = app_self._custom_widget_registry.get(name)
        if definition is None:
            raise ValueError(f"Unknown custom widget '{name}'. Register it with app.register_widget() first.")

        cid = app_self._resolve_widget_cid(f"custom_widget_{_sanitize_custom_widget_key(name)}", key)

        event_cids: Dict[str, str] = {}
        render_props = dict(props)
        for event_name in definition.events:
            callback_prop = f"on_{event_name}"
            callback = render_props.pop(callback_prop, None)
            if callback is None:
                event_cids[event_name] = ""
                continue
            if not callable(callback):
                raise TypeError(f"{callback_prop} must be callable when passed to app.widget().")

            action_cid = f"{cid}_{_sanitize_custom_widget_key(event_name)}_action"

            def action_builder(_action_cid=action_cid):
                return Component("div", id=_action_cid, style="display:none")

            def action(value=None, _callback=callback):
                _invoke_action_callback(_callback, _coerce_widget_payload(value))

            app_self._register_component(action_cid, action_builder, action=action)
            event_cids[event_name] = action_cid

        def builder():
            token = rendering_ctx.set(cid)
            try:
                resolved_props = {
                    prop_name: _resolve_widget_prop_value(prop_value)
                    for prop_name, prop_value in render_props.items()
                }
                context = CustomWidgetContext(
                    app=self,
                    name=name,
                    cid=cid,
                    event_cids=dict(event_cids),
                    props=dict(resolved_props),
                )
                result = _normalize_custom_widget_result(definition.render(context, **resolved_props))
            finally:
                rendering_ctx.reset(token)

            host_attrs = dict(result.attrs)
            host_attrs.pop("id", None)
            host_class = host_attrs.pop("class", "") or host_attrs.pop("class_", "")
            host_style = host_attrs.pop("style", "")
            host_init_names = _normalize_init_names(
                host_attrs.pop("data_vl_init", None) or host_attrs.pop("data-vl-init", None)
            )
            merged_init_names = tuple(dict.fromkeys(definition.initializer_names + host_init_names))
            if merged_init_names:
                host_attrs["data_vl_init"] = " ".join(merged_init_names)
            host_attrs.setdefault("data_vl_widget", name)

            widget_defaults = app_self._get_widget_defaults(name)
            final_cls = merge_cls(widget_defaults.get("cls", ""), cls, result.cls, host_class)
            final_style = merge_style(widget_defaults.get("style", ""), style, result.style, host_style)
            return Component(
                result.tag or "div",
                id=cid,
                content=result.content,
                class_=final_cls or None,
                style=final_style or None,
                **host_attrs,
            )

        app_self._register_component(cid, builder)
