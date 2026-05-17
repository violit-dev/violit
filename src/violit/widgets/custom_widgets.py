"""Custom widget registry mixin for Violit."""

from __future__ import annotations

from dataclasses import dataclass, field
import html
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
    return value


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

        cid = (
            f"custom_widget_{_sanitize_custom_widget_key(name)}_{_sanitize_custom_widget_key(key)}"
            if key is not None
            else app_self._get_next_cid(f"custom_widget_{_sanitize_custom_widget_key(name)}")
        )

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
