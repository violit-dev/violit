"""Input widgets"""

from typing import Union, Callable, Optional, List, Any
import base64
import html as html_lib
import io
import json
from ..component import Component
from ..context import rendering_ctx, layout_ctx
from ..state import State
from ..style_utils import auto_split_widget_cls, merge_cls, merge_style, merge_part_cls, serialize_part_cls, wrap_html


class UploadedFile(io.BytesIO):
    def __init__(self, name, type, size, content_b64):
        self.name = name
        self.type = type
        self.size = size
        # content_b64 is like "data:text/csv;base64,AAAA..."
        if "," in content_b64:
             self.header, data = content_b64.split(",", 1)
        else:
             self.header = ""
             data = content_b64
        try:
            decoded = base64.b64decode(data)
        except:
            decoded = b""
        super().__init__(decoded)
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<UploadedFile name='{self.name}' type='{self.type}' size={self.size}>"


class InputWidgetsMixin:

    @staticmethod
    def _part_bridge_script(target_selector: str) -> str:
        escaped_selector = json.dumps(target_selector)
        return f'''<script>(function() {{
            let attempts = 0;
            const run = function() {{
                attempts += 1;
                const hosts = Array.from(document.querySelectorAll({escaped_selector}));
                if (hosts.length && hosts.every((el) => el.shadowRoot) && window.applyPartStyles) {{
                    hosts.forEach((el) => window.applyPartStyles(el));
                    return;
                }}
                if (attempts < 20) setTimeout(run, 80);
            }};
            run();
        }})();</script>'''

    @staticmethod
    def _label_vis_attrs(label_visibility):
        """Return (label_style, wrapper_style) for Streamlit label_visibility compat."""
        if label_visibility == "hidden":
            return 'style="visibility:hidden;height:0;overflow:hidden;"', ''
        elif label_visibility == "collapsed":
            return 'style="display:none;"', ''
        return '', ''  # "visible"

    def text_input(self, label, value="", key=None, on_change=None,
                   on_submit=None,
                   type="default", max_chars=None, placeholder="",
                   autocomplete=None, disabled=False,
                   label_visibility="visible", help=None,
                   cls: str = "", style: str = "", **props):
        """Single-line text input

        Args:
            type: Input type - "default" or "password"
            max_chars: Maximum number of characters
            placeholder: Placeholder text when empty
            autocomplete: HTML autocomplete attribute
            disabled: If True, widget is grayed out
            on_submit: Callback when Enter submits the current value
            label_visibility: "visible", "hidden", or "collapsed"
            help: Tooltip / help text shown below the input
        """
        _type = "password" if type == "password" else "text"
        extra = {}
        if _type != "text": extra["type"] = _type
        if max_chars is not None: extra["maxlength"] = max_chars
        if placeholder: extra["placeholder"] = placeholder
        if autocomplete: extra["autocomplete"] = autocomplete
        if disabled: extra["disabled"] = True
        if help: extra["hint"] = help
        return self._input_component("input", "wa-input", label, value, on_change, key,
                         on_submit=on_submit,
                                     cls=cls, style=style, label_visibility=label_visibility,
                                     **extra, **props)

    def slider(self, label, min_value=0, max_value=100, value=None, step=1,
               key=None, on_change=None, live_update=False,
               disabled=False, label_visibility="visible", help=None,
               cls: str = "", style: str = "", **props):
        """Slider widget

        Args:
            live_update: If True, value updates in real-time while dragging.
                         If False (default), value updates only when released.
            disabled: If True, widget is grayed out
            label_visibility: "visible", "hidden", or "collapsed"
            help: Tooltip / help text shown below the slider
        """
        if value is None: value = min_value
        extra = {}
        if disabled: extra["disabled"] = True
        if help: extra["hint"] = help
        return self._input_component("slider", "wa-slider", label, value, on_change, key,
                                     cls=cls, style=style, live_update=live_update,
                                     label_visibility=label_visibility,
                                     min=min_value, max=max_value, step=step,
                                     **extra, **props)

    def select_slider(self, label, options=None, value=None, key=None, on_change=None, cls: str = "", style: str = "", **props):
        """Slider widget with discrete values from a list
        
        Args:
            label: Display label
            options: List of option values (strings, numbers, etc.)
            value: Default value (must be in options list)
            key: Widget key for state management
            on_change: Callback when value changes
        """
        if options is None or len(options) == 0:
            return None

        cid = self._get_next_cid("select_slider")
        state_key = key or f"select_slider:{label}"
        default_val = value if value is not None else options[0]
        s = self.state(default_val, key=state_key)
        options_str = [str(o) for o in options]

        def action(v):
            idx = int(v)
            actual = options[idx] if 0 <= idx < len(options) else options[0]
            s.set(actual)
            if on_change:
                on_change(actual)

        def builder():
            token = rendering_ctx.set(cid)
            cv = s.value
            rendering_ctx.reset(token)

            try:
                current_idx = options.index(cv)
            except ValueError:
                current_idx = 0

            max_idx = len(options) - 1
            n = len(options)
            # The labels will be calculated in ticks_html instead
            current_label = html_lib.escape(str(cv))
            range_id = f"{cid}_range"

            if self.mode == 'lite':
                attrs_str = f'hx-post="/action/{cid}" hx-trigger="change" hx-swap="none" hx-vals="js:{{value: event.target.value}}"'
                listener_script = ""
            else:
                attrs_str = ""
                listener_script = f'''
                <script>
                (function() {{
                    var el = document.getElementById('{range_id}');
                    var display = document.getElementById('{cid}_display');
                    var opts = {json.dumps(options_str)};
                    if (el && !el.hasAttribute('data-ws-listener')) {{
                        el.setAttribute('data-ws-listener', 'true');
                        el.addEventListener('input', function() {{
                            if (display) display.textContent = opts[parseInt(el.value)];
                        }});
                        el.addEventListener('change', function() {{
                            window.sendAction('{cid}', el.value);
                        }});
                    }}
                }})();
                </script>
                '''

            props_str = ' '.join(f'{k}="{v}"' for k, v in props.items() if v is not None and v is not False)

            # 5. Position labels precisely using relative/absolute positioning
            # A standard Web Awesome slider thumb is typically 15px-16px.
            # It travels from ~8px from the left to ~8px from the right.
            ticks_html = []
            if max_idx > 0:
                for i, o in enumerate(options):
                    percent = (i / max_idx) * 100
                    # Position explicitly on the track taking thumb size into account
                    ticks_html.append(
                        f'<span style="position:absolute; left:calc({percent}% - {percent / 100 * 16}px + 8px); '
                        f'transform:translateX(-50%); font-size:0.75rem; opacity:0.7; pointer-events:none;">'
                        f'{html_lib.escape(str(o))}</span>'
                    )
            else:
                ticks_html.append(
                    f'<span style="position:absolute; left:50%; transform:translateX(-50%); '
                    f'font-size:0.75rem; opacity:0.7;">{html_lib.escape(str(options[0]))}</span>'
                )
            ticks = ''.join(ticks_html)

            # 6. HTML Construction
            html_content = f'''
                <label style="display:block; font-size:0.875rem; font-weight:500; margin-bottom:0.25rem;">{html_lib.escape(str(label))}</label>
                <wa-slider id="{range_id}" min="0" max="{max_idx}" step="1" value="{current_idx}" tooltip="none" {attrs_str} {props_str}></wa-slider>
                <div style="position:relative; width:100%; height:1rem; margin-top:0.15rem;">
                    {ticks}
                </div>
                <div id="{cid}_display" style="text-align:center; font-weight:600; margin-top:0.25rem; font-size:0.875rem;">{current_label}</div>
            {listener_script}
            '''
            _wd = self._get_widget_defaults("select_slider")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            # Add default margin bottom
            base_style = "margin-bottom:1rem;"
            _fs = merge_style(base_style, _wd.get("style", ""))
            _fs = merge_style(_fs, style)
            
            return Component("div", id=cid, class_=_fc or None, style=_fs or None, content=html_content)
        self._register_component(cid, builder, action=action)
        return s

    def checkbox(self, label, value=False, key=None, on_change=None,
                  disabled=False, label_visibility="visible", help=None,
                  cls: str = "", style: str = "", **props):
        """Checkbox widget

        Args:
            disabled: If True, widget is grayed out
            label_visibility: "visible", "hidden", or "collapsed"
            help: Tooltip / help text
        """
        cid = self._get_next_cid("checkbox")
        user_part_cls = props.pop("part_cls", None)
        
        state_key = key or f"checkbox:{label}"
        s = self.state(value, key=state_key)
        
        def action(v):
            real_val = str(v).lower() == 'true'
            s.set(real_val)
            if on_change: on_change(real_val)
        
        def builder():
            # Subscribe to own state - client-side will handle smart updates
            token = rendering_ctx.set(cid)
            cv = s.value
            rendering_ctx.reset(token)
            
            checked_attr = 'checked' if cv else ''
            props_str = ' '.join(f'{k}="{v}"' for k, v in props.items() if v is not None and v is not False)
            
            if self.mode == 'lite':
                attrs_str = f'hx-post="/action/{cid}" hx-trigger="change" hx-swap="none" hx-vals="js:{{value: event.target.checked}}"'
                listener_script = ""
            else:
                # WS mode: use addEventListener for Web Awesome custom events
                attrs_str = ""
                listener_script = f'''
                <script>
                (function() {{
                    const el = document.getElementById('{cid}');
                    if (el && !el.hasAttribute('data-ws-listener')) {{
                        el.setAttribute('data-ws-listener', 'true');
                        el.addEventListener('change', function(e) {{
                            window.sendAction('{cid}', el.checked);
                        }});
                    }}
                }})();
                </script>
                '''
            
            disabled_attr = 'disabled' if disabled else ''
            help_html = f'<br><span style="font-size:0.75rem;color:var(--vl-text-muted);">{html_lib.escape(str(help))}</span>' if help else ''
            _wd = self._get_widget_defaults("checkbox")
            default_host_cls, default_auto_part_cls = auto_split_widget_cls("checkbox", _wd.get("cls", ""))
            user_host_cls, user_auto_part_cls = auto_split_widget_cls("checkbox", cls)
            _fc = merge_cls(default_host_cls, user_host_cls)
            _fs = merge_style(_wd.get("style", ""), style)
            _part_cls = merge_part_cls(default_auto_part_cls, _wd.get("part_cls", {}), user_auto_part_cls, user_part_cls)
            part_attr = f' data-vl-part-cls="{html_lib.escape(serialize_part_cls(_part_cls), quote=True)}"' if _part_cls else ''
            part_bridge_script = self._part_bridge_script(f'wa-checkbox#{cid}[data-vl-part-cls]') if _part_cls else ''
            html = f'<wa-checkbox id="{cid}"{part_attr} {checked_attr} {disabled_attr} {attrs_str} {props_str}>{html_lib.escape(str(label))}{help_html}</wa-checkbox>{listener_script}{part_bridge_script}'
            return Component(None, id=cid, content=wrap_html(html, _fc, _fs))
        self._register_component(cid, builder, action=action)
        return s

    def radio(self, label, options, index=0, key=None, on_change=None,
              horizontal=False, captions=None,
              disabled=False, label_visibility="visible", help=None,
              cls: str = "", style: str = "", **props):
        """Radio button group

        Args:
            horizontal: If True, display options in a row
            captions: List of caption strings shown below each option
            disabled: If True, widget is grayed out
            label_visibility: "visible", "hidden", or "collapsed"
            help: Tooltip / help text
        """
        cid = self._get_next_cid("radio_group")
        user_part_cls = props.pop("part_cls", None)
        
        state_key = key or f"radio:{label}"
        default_val = options[index] if options else None
        s = self.state(default_val, key=state_key)
        
        def action(v):
            s.set(v)
            if on_change: on_change(v)
            
        def builder():
            token = rendering_ctx.set(cid)
            cv = s.value
            rendering_ctx.reset(token)

            _wd = self._get_widget_defaults("radio")
            default_host_cls, default_auto_part_cls = auto_split_widget_cls("radio", _wd.get("cls", ""))
            user_host_cls, user_auto_part_cls = auto_split_widget_cls("radio", cls)
            _fc = merge_cls(default_host_cls, user_host_cls)
            _fs = merge_style(_wd.get("style", ""), style)
            _part_cls = merge_part_cls(default_auto_part_cls, _wd.get("part_cls", {}), user_auto_part_cls, user_part_cls)
            radio_part_attr = f' data-vl-part-cls="{html_lib.escape(serialize_part_cls(_part_cls), quote=True)}"' if _part_cls else ''
            part_bridge_script = self._part_bridge_script(f'wa-radio-group#{cid} wa-radio[data-vl-part-cls]') if _part_cls else ''
            
            opts_html = ""
            for i_opt, opt in enumerate(options):
                sel = 'checked' if opt == cv else ''
                escaped_opt = html_lib.escape(str(opt), quote=True)
                caption_html = ''
                option_style = 'display:block;margin:0;'
                if captions and i_opt < len(captions) and captions[i_opt]:
                    caption_html = f'<br><span style="font-size:0.75rem;color:var(--vl-text-muted);font-weight:normal;">{html_lib.escape(str(captions[i_opt]))}</span>'
                    if horizontal:
                        option_style = 'display:inline-flex;align-items:flex-start;vertical-align:middle;margin:0;'
                elif horizontal:
                    option_style = 'display:inline-flex;align-items:center;vertical-align:middle;margin:0;'
                opts_html += f'<wa-radio value="{escaped_opt}" style="{option_style}"{radio_part_attr} {sel}>{escaped_opt}{caption_html}</wa-radio>'
            
            if self.mode == 'lite':
                attrs_str = f'hx-post="/action/{cid}" hx-trigger="change" hx-swap="none" name="value"'
                listener_script = ""
            else:
                # WS mode: use addEventListener for Web Awesome custom events
                attrs_str = ""
                listener_script = f'''
                <script>
                (function() {{
                    const el = document.getElementById('{cid}');
                    if (el && !el.hasAttribute('data-ws-listener')) {{
                        el.setAttribute('data-ws-listener', 'true');
                        el.addEventListener('change', function(e) {{
                            window.sendAction('{cid}', el.value);
                        }});
                    }}
                }})();
                </script>
                '''
            
            props_str = ' '.join(f'{k}="{v}"' for k, v in props.items() if v is not None and v is not False)
            escaped_cv = html_lib.escape(str(cv), quote=True)
            disabled_attr = 'disabled' if disabled else ''
            help_attr = f'hint="{html_lib.escape(str(help), quote=True)}"' if help else ''
            # Keep the default layout vertical and only opt into horizontal rows when requested.
            options_layout_style = 'display:flex;flex-direction:column;gap:0.5rem;'
            if horizontal:
                options_layout_style = 'display:flex;flex-direction:row;flex-wrap:wrap;gap:1rem;align-items:center;'
            html = f'<wa-radio-group id="{cid}" label="{label}" value="{escaped_cv}" {disabled_attr} {help_attr} {attrs_str} {props_str}><div style="{options_layout_style}">{opts_html}</div></wa-radio-group>{listener_script}{part_bridge_script}'
            return Component(None, id=cid, content=wrap_html(html, _fc, _fs))
            
        self._register_component(cid, builder, action=action)
        return s

    @staticmethod
    def _select_encode(v):
        """Encode a string for safe use as select option value attribute.
        
        Web Awesome wa-select treats the value attribute as a space-separated
        token list (like HTML class). Spaces in values break selection/matching.
        We percent-encode spaces (and %) to produce a single safe token.
        """
        s = str(v)
        s = s.replace('%', '%25')  # encode % first
        s = s.replace(' ', '%20')  # encode space
        return s

    @staticmethod
    def _select_decode(v):
        """Decode a select-safe value back to the original string."""
        s = str(v)
        s = s.replace('%20', ' ')
        s = s.replace('%25', '%')
        return s

    def selectbox(self, label, options, index=0, key=None, on_change=None,
                   placeholder=None, disabled=False,
                   label_visibility="visible", help=None,
                   cls: str = "", style: str = "", **props):
        """Single select dropdown

        Args:
            placeholder: Placeholder text when nothing is selected
            disabled: If True, widget is grayed out
            label_visibility: "visible", "hidden", or "collapsed"
            help: Tooltip / help text
        """
        cid = self._get_next_cid("select")
        user_part_cls = props.pop("part_cls", None)
        
        state_key = key or f"select:{label}"
        default_val = options[index] if options else None
        s = self.state(default_val, key=state_key)
        
        def action(v):
            decoded = InputWidgetsMixin._select_decode(v)
            s.set(decoded)
            if on_change: on_change(decoded)
            
        def builder():
            token = rendering_ctx.set(cid)
            cv = s.value
            rendering_ctx.reset(token)
            
            opts_html = ""
            for opt in options:
                encoded_opt = InputWidgetsMixin._select_encode(opt)
                escaped_encoded = html_lib.escape(encoded_opt, quote=True)
                escaped_display = html_lib.escape(str(opt), quote=True)
                sel = 'selected' if opt == cv else ''
                opts_html += f'<wa-option value="{escaped_encoded}" {sel}>{escaped_display}</wa-option>'
            
            encoded_cv = InputWidgetsMixin._select_encode(cv) if cv is not None else ''
            escaped_cv = html_lib.escape(encoded_cv, quote=True)
            escaped_label = html_lib.escape(str(label), quote=True)
            
            if self.mode == 'lite':
                attrs = {"hx-post": f"/action/{cid}", "hx-trigger": "change", "hx-swap": "none", "name": "value"}
                listener_script = ""
            else:
                # WS mode: use native change events from Web Awesome
                attrs = {}
                desired_json = json.dumps(encoded_cv, ensure_ascii=False)
                listener_script = f'''
                <script>
                (function() {{
                    const el = document.getElementById('{cid}');
                    const desiredValue = {desired_json};
                    if (el) {{
                        function syncValue() {{
                            if (el.value !== desiredValue) el.value = desiredValue;
                        }}
                        
                        syncValue();
                        
                        if (el.updateComplete) {{
                            el.updateComplete.then(syncValue);
                        }}
                        
                        requestAnimationFrame(function() {{
                            syncValue();
                            setTimeout(syncValue, 150);
                        }});
                        
                        if (!el.hasAttribute('data-ws-listener')) {{
                            el.setAttribute('data-ws-listener', 'true');
                            el.addEventListener('change', function(e) {{
                                window.sendAction('{cid}', el.value);
                            }});
                        }}
                    }}
                }})();
                </script>
                '''
            
            select_html = f'<wa-select id="{cid}" label="{escaped_label}" value="{escaped_cv}" appearance="outlined"'
            extra_attrs = {}
            if placeholder: extra_attrs['placeholder'] = placeholder
            if disabled: extra_attrs['disabled'] = True
            if help: extra_attrs['hint'] = help
            for k, v in {**attrs, **extra_attrs, **props}.items():
                if v is True:
                    select_html += f' {k}'
                elif v is not False and v is not None:
                    select_html += f' {k}="{v}"'
            select_html += f'>{opts_html}</wa-select>{listener_script}'
            
            _wd = self._get_widget_defaults("selectbox")
            default_host_cls, default_auto_part_cls = auto_split_widget_cls("selectbox", _wd.get("cls", ""))
            user_host_cls, user_auto_part_cls = auto_split_widget_cls("selectbox", cls)
            _fc = merge_cls(default_host_cls, user_host_cls)
            _fs = merge_style(_wd.get("style", ""), style)
            _part_cls = merge_part_cls(default_auto_part_cls, _wd.get("part_cls", {}), user_auto_part_cls, user_part_cls)
            part_bridge_script = ""
            if _part_cls:
                part_attr = f' data-vl-part-cls="{html_lib.escape(serialize_part_cls(_part_cls), quote=True)}"'
                select_html = select_html.replace(f'<wa-select id="{cid}"', f'<wa-select id="{cid}"{part_attr}', 1)
                part_bridge_script = f'''<script>(function() {{
                    let attempts = 0;
                    const run = function() {{
                        attempts += 1;
                        const el = document.getElementById('{cid}');
                        if (el && el.shadowRoot && window.applyPartStyles) {{
                            window.applyPartStyles(el);
                            return;
                        }}
                        if (attempts < 20) setTimeout(run, 80);
                    }};
                    run();
                }})();</script>'''
            return Component(None, id=cid, content=wrap_html(select_html + part_bridge_script, _fc, _fs))
            
        self._register_component(cid, builder, action=action)
        return s

    def multiselect(self, label, options, default=None, key=None, on_change=None,
                     max_selections=None, placeholder=None, disabled=False,
                     label_visibility="visible", help=None,
                     cls: str = "", style: str = "", **props):
        """Multi-select dropdown

        Args:
            max_selections: Maximum number of selections allowed
            placeholder: Placeholder text when nothing is selected
            disabled: If True, widget is grayed out
            label_visibility: "visible", "hidden", or "collapsed"
            help: Tooltip / help text
        """
        cid = self._get_next_cid("multiselect")
        user_part_cls = props.pop("part_cls", None)
        
        state_key = key or f"multiselect:{label}"
        default_val = default or []
        s = self.state(default_val, key=state_key)
        
        def action(v):
            if isinstance(v, str):
                selected = [InputWidgetsMixin._select_decode(x.strip()) for x in v.split(',') if x.strip()]
            elif isinstance(v, list):
                selected = [InputWidgetsMixin._select_decode(x) for x in v]
            else:
                selected = []
            s.set(selected)
            if on_change: on_change(selected)
        
        def builder():
            token = rendering_ctx.set(cid)
            cv = s.value
            rendering_ctx.reset(token)
            
            opts_html = ""
            for opt in options:
                encoded_opt = InputWidgetsMixin._select_encode(opt)
                escaped_encoded = html_lib.escape(encoded_opt, quote=True)
                escaped_display = html_lib.escape(str(opt), quote=True)
                sel = 'selected' if opt in cv else ''
                opts_html += f'<wa-option value="{escaped_encoded}" {sel}>{escaped_display}</wa-option>'
            
            listener_script = ""
            if self.mode == 'ws':
                encoded_cv = [InputWidgetsMixin._select_encode(x) for x in cv] if cv else []
                desired_json = json.dumps(encoded_cv, ensure_ascii=False)
                listener_script = f'''
                <script>
                (function() {{
                    const el = document.getElementById('{cid}');
                    const desiredValue = {desired_json};
                    if (el) {{
                        function syncValue() {{
                            const current = Array.isArray(el.value) ? el.value.join(',') : '';
                            const desired = desiredValue.join(',');
                            if (current !== desired) el.value = desiredValue;
                        }}
                        
                        syncValue();
                        
                        if (el.updateComplete) {{
                            el.updateComplete.then(syncValue);
                        }}
                        
                        requestAnimationFrame(function() {{
                            syncValue();
                            setTimeout(syncValue, 150);
                        }});
                        
                        if (!el.hasAttribute('data-ws-listener')) {{
                            el.setAttribute('data-ws-listener', 'true');
                            el.addEventListener('change', function(e) {{
                                const vals = Array.isArray(el.value) ? el.value : (el.value ? [el.value] : []);
                                window.sendAction('{cid}', vals.join(','));
                            }});
                        }}
                    }}
                }})();
                </script>
                '''

            _wd = self._get_widget_defaults("multiselect")
            default_host_cls, default_auto_part_cls = auto_split_widget_cls("multiselect", _wd.get("cls", ""))
            user_host_cls, user_auto_part_cls = auto_split_widget_cls("multiselect", cls)
            _fc = merge_cls(default_host_cls, user_host_cls)
            _fs = merge_style(_wd.get("style", ""), style)
            _part_cls = merge_part_cls(default_auto_part_cls, _wd.get("part_cls", {}), user_auto_part_cls, user_part_cls)
            # wa-select: cls/style applied via wrapper since this is a Web Awesome component
            # label escaping handled by Component.render(); opts_html is raw so manually escaped above
            _ms_extra = {}
            if placeholder: _ms_extra['placeholder'] = placeholder
            if disabled: _ms_extra['disabled'] = True
            if help: _ms_extra['hint'] = help
            if max_selections: _ms_extra['max-options-visible'] = max_selections
            if _part_cls:
                _ms_extra["data_vl_part_cls"] = serialize_part_cls(_part_cls)
            inner = Component("wa-select", id=cid, label=label, content=opts_html, multiple=True, with_clear=True, appearance="outlined", **_ms_extra)
            inner_html = inner.render() + listener_script
            if _part_cls:
                inner_html += self._part_bridge_script(f'wa-select#{cid}[data-vl-part-cls]')
            if _fc or _fs:
                return Component(None, id=f"{cid}_wrap", content=wrap_html(inner_html, _fc, _fs))
            return Component(None, id=cid, content=inner_html)
        
        self._register_component(cid, builder, action=action)
        
        # Add initialization script for lite mode
        if self.mode == 'lite':
            init_script_cid = f"{cid}_init"
            def script_builder():
                script = f'''
                <script>
                (function() {{
                    function initSelect() {{
                        const el = document.getElementById('{cid}');
                        if (!el) {{
                            setTimeout(initSelect, 50);
                            return;
                        }}
                        if (!el.hasAttribute('data-listener-added')) {{
                            el.setAttribute('data-listener-added', 'true');
                            el.addEventListener('change', function(e) {{
                                const values = Array.isArray(el.value) ? el.value : [];
                                const valueStr = values.join(',');
                                htmx.ajax('POST', '/action/{cid}', {{
                                    values: {{ value: valueStr }},
                                    swap: 'none'
                                }});
                            }});
                        }}
                    }}
                    initSelect();
                }})();
                </script>
                '''
                return Component("div", id=init_script_cid, style="display:none", content=script)
            
            self.static_builders[init_script_cid] = script_builder
            if layout_ctx.get() == "sidebar":
                if init_script_cid not in self.static_sidebar_order:
                    self.static_sidebar_order.append(init_script_cid)
            else:
                if init_script_cid not in self.static_order:
                    self.static_order.append(init_script_cid)
        
        return s

    def text_area(self, label, value="", height=None, key=None, on_change=None,
                   max_chars=None, placeholder="", disabled=False,
                   label_visibility="visible", help=None,
                   cls: str = "", style: str = "", **props):
        """Multi-line text input

        Args:
            height: Streamlit-style height. ``None`` keeps the default multiline
                    size, integers are treated as pixels, ``"content"`` grows to
                    fit content, and ``"stretch"`` stretches with its container.
                    Use ``rows=...`` for explicit row counts.
            max_chars: Maximum number of characters
            placeholder: Placeholder text when empty
            disabled: If True, widget is grayed out
            label_visibility: "visible", "hidden", or "collapsed"
            help: Tooltip / help text
        """
        cid = self._get_next_cid("textarea")
        user_part_cls = props.pop("part_cls", None)
        
        state_key = key or f"textarea:{label}"
        s = self.state(value, key=state_key)
        
        def action(v):
            s.set(v)
            if on_change: on_change(v)
        
        def builder():
            # Create local shallow copies of cls/style to avoid shadowing/unbound errors
            _cls = cls
            _style = style
            local_props = dict(props)

            token = rendering_ctx.set(cid)
            cv = s.value
            rendering_ctx.reset(token)

            text_value = "" if cv is None else str(cv)
            content_lines = text_value.count("\n") + 1 if text_value else 1
            min_pixel_height = 68 if label_visibility == "collapsed" else 98
            effective_rows = 3
            explicit_height_px = None
            height_mode = None

            rows_value = local_props.pop("rows", None)
            if rows_value is not None:
                try:
                    effective_rows = max(1, int(float(str(rows_value).strip().replace("rows", ""))))
                except ValueError:
                    effective_rows = 3

            resize_prop = local_props.pop("resize", None)
            if height is None:
                pass
            elif isinstance(height, (int, float)):
                explicit_height_px = max(min_pixel_height, int(float(height)))
            else:
                height_str = str(height).strip()
                height_lower = height_str.lower()

                if height_lower in {"content", "stretch"}:
                    height_mode = height_lower
                    if rows_value is None:
                        effective_rows = max(3, min(12, content_lines))
                elif height_lower.endswith("px"):
                    try:
                        explicit_height_px = max(min_pixel_height, int(float(height_lower[:-2].strip())))
                    except ValueError:
                        explicit_height_px = None
                elif height_lower.endswith("rows"):
                    if rows_value is None:
                        try:
                            effective_rows = max(1, int(float(height_lower[:-4].strip())))
                        except ValueError:
                            effective_rows = 3
                else:
                    try:
                        explicit_height_px = max(min_pixel_height, int(float(height_lower)))
                    except ValueError:
                        explicit_height_px = None

            textarea_resize = resize_prop if resize_prop is not None else ("auto" if height_mode in {"content", "stretch"} else "vertical")

            if self.mode == 'lite':
                attrs = {"hx-post": f"/action/{cid}", "hx-trigger": "input delay:50ms", "hx-swap": "none", "name": "value"}
                listener_script = ""
            else:
                # WS mode: use addEventListener for Web Awesome custom events
                attrs = {}
                desired_json = json.dumps(cv, ensure_ascii=False)
                resize_sync = ""
                if textarea_resize == "auto":
                    resize_sync = '''
                            if (typeof el.handleValueChange === 'function') el.handleValueChange();
                            if (typeof el.setTextareaDimensions === 'function') el.setTextareaDimensions();
                    '''
                listener_script = f'''
                <script>
                (function() {{
                    const el = document.getElementById('{cid}');
                    const desiredValue = {desired_json};
                    if (el) {{
                        const syncTextarea = function() {{
                            if (el.value !== desiredValue) el.value = desiredValue;
{resize_sync}
                        }};

                        syncTextarea();

                        if (el.updateComplete) {{
                            el.updateComplete.then(syncTextarea);
                        }}

                        requestAnimationFrame(function() {{
                            syncTextarea();
                            setTimeout(syncTextarea, 150);
                        }});

                        if (!el.hasAttribute('data-ws-listener')) {{
                            el.setAttribute('data-ws-listener', 'true');
                            el.addEventListener('input', function(e) {{
                                window.sendAction('{cid}', el.value);
                            }});
                        }}
                    }}
                }})();
                </script>
                '''
            
            textarea_props = {"resize": textarea_resize, "rows": effective_rows}

            # Web Awesome's auto resize can still collapse empty textareas to a single line
            # before the component fully measures itself, especially in initially hidden tabs.
            # Give the host element a stable baseline size that follows Streamlit-style height semantics.
            min_height_rem = max(4.75, 1.35 * effective_rows + 1.2)
            existing_inner_style = local_props.pop("style", "")
            if explicit_height_px is not None:
                textarea_style = merge_style(existing_inner_style, f"--wa-form-control-height: {explicit_height_px}px;")
            elif height_mode == "stretch":
                textarea_style = merge_style(existing_inner_style, f"min-height: {min_pixel_height}px;", "height: 100%;")
            else:
                textarea_style = merge_style(existing_inner_style, f"min-height: {min_height_rem:.2f}rem;")
            textarea_props["style"] = textarea_style

            if max_chars is not None: textarea_props["maxlength"] = max_chars
            if placeholder: textarea_props["placeholder"] = placeholder
            if disabled: textarea_props["disabled"] = True
            if help: textarea_props["hint"] = help
            html = f'<wa-textarea id="{cid}" label="{label}" value="{cv}" appearance="outlined"'
            for k, v in {**attrs, **textarea_props, **local_props}.items():
                if v is True: html += f' {k}'
                elif v is not False and v is not None: html += f' {k}="{v}"'
            html += f'></wa-textarea>{listener_script}'
            
            _wd = self._get_widget_defaults("text_area")
            default_host_cls, default_auto_part_cls = auto_split_widget_cls("text_area", _wd.get("cls", ""))
            user_host_cls, user_auto_part_cls = auto_split_widget_cls("text_area", _cls)
            _fc = merge_cls(default_host_cls, user_host_cls)
            _fs = merge_style(_wd.get("style", ""), _style)
            _part_cls = merge_part_cls(default_auto_part_cls, _wd.get("part_cls", {}), user_auto_part_cls, user_part_cls)
            part_bridge_script = ""
            if _part_cls:
                part_attr = f' data-vl-part-cls="{html_lib.escape(serialize_part_cls(_part_cls), quote=True)}"'
                html = html.replace(f'<wa-textarea id="{cid}"', f'<wa-textarea id="{cid}"{part_attr}', 1)
                part_bridge_script = f'''<script>(function() {{
                    let attempts = 0;
                    const run = function() {{
                        attempts += 1;
                        const el = document.getElementById('{cid}');
                        if (el && el.shadowRoot && window.applyPartStyles) {{
                            window.applyPartStyles(el);
                            return;
                        }}
                        if (attempts < 20) setTimeout(run, 80);
                    }};
                    run();
                }})();</script>'''
            return Component(None, id=cid, content=wrap_html(html + part_bridge_script, _fc, _fs))
        
        self._register_component(cid, builder, action=action)
        return s

    def number_input(self, label, value=0, min_value=None, max_value=None, step=1,
                      key=None, on_change=None,
                      placeholder="", disabled=False,
                      label_visibility="visible", help=None,
                      cls: str = "", style: str = "", **props):
        """Numeric input

        Args:
            placeholder: Placeholder text when empty
            disabled: If True, widget is grayed out
            label_visibility: "visible", "hidden", or "collapsed"
            help: Tooltip / help text
        """
        cid = self._get_next_cid("number")
        user_part_cls = props.pop("part_cls", None)
        
        state_key = key or f"number:{label}"
        s = self.state(value, key=state_key)
        
        def action(v):
            try:
                num_val = float(v) if '.' in str(v) else int(v)
                s.set(num_val)
                if on_change: on_change(num_val)
            except (ValueError, TypeError):
                pass
        
        def builder():
            token = rendering_ctx.set(cid)
            cv = s.value
            rendering_ctx.reset(token)
            
            if self.mode == 'lite':
                attrs = {"hx-post": f"/action/{cid}", "hx-trigger": "input delay:50ms", "hx-swap": "none", "name": "value"}
                listener_script = ""
            else:
                # WS mode: use addEventListener
                attrs = {}
                listener_script = f'''
                <script>
                (function() {{
                    const el = document.getElementById('{cid}');
                    if (el && !el.hasAttribute('data-ws-listener')) {{
                        el.setAttribute('data-ws-listener', 'true');
                        el.addEventListener('input', function(e) {{
                            window.sendAction('{cid}', el.value);
                        }});
                    }}
                }})();
                </script>
                '''
            
            num_props = {"type": "number"}
            if min_value is not None: num_props["min"] = min_value
            if max_value is not None: num_props["max"] = max_value
            if step is not None: num_props["step"] = step
            if placeholder: num_props["placeholder"] = placeholder
            if disabled: num_props["disabled"] = True
            if help: num_props["hint"] = help
            
            html = f'<wa-input id="{cid}" label="{label}" value="{cv}" appearance="outlined"'
            for k, v in {**attrs, **num_props, **props}.items():
                if v is True: html += f' {k}'
                elif v is not False and v is not None: html += f' {k}="{v}"'
            html += f'></wa-input>{listener_script}'
            
            _wd = self._get_widget_defaults("number_input")
            default_host_cls, default_auto_part_cls = auto_split_widget_cls("number_input", _wd.get("cls", ""))
            user_host_cls, user_auto_part_cls = auto_split_widget_cls("number_input", cls)
            _fc = merge_cls(default_host_cls, user_host_cls)
            _fs = merge_style(_wd.get("style", ""), style)
            _part_cls = merge_part_cls(default_auto_part_cls, _wd.get("part_cls", {}), user_auto_part_cls, user_part_cls)
            if _part_cls:
                part_attr = f' data-vl-part-cls="{html_lib.escape(serialize_part_cls(_part_cls), quote=True)}"'
                html = html.replace(f'<wa-input id="{cid}"', f'<wa-input id="{cid}"{part_attr}', 1)
                html += self._part_bridge_script(f'wa-input#{cid}[data-vl-part-cls]')
            return Component(None, id=cid, content=wrap_html(html, _fc, _fs))
        
        self._register_component(cid, builder, action=action)
        return s

    def file_uploader(self, label, type=None, accept=None, accept_multiple_files=False, multiple=False,
                       key=None, on_change=None, help=None, disabled=False,
                       label_visibility="visible",
                       cls: str = "", style: str = "", **props):
        """File upload widget

        Args:
            type: Accepted file types (Streamlit compat alias for accept)
            accept: Accepted file types (e.g. "image/*", ".csv,.xlsx")
            accept_multiple_files: If True, allow multiple files (Streamlit compat)
            multiple: If True, allow multiple files
            disabled: If True, widget is grayed out
            label_visibility: "visible", "hidden", or "collapsed"
        """
        # Streamlit compat: 'type' maps to 'accept'
        if type is not None and accept is None:
            if isinstance(type, list): accept = ','.join(type)
            else: accept = type
        # Streamlit compat: accept_multiple_files
        if accept_multiple_files: multiple = True
        cid = self._get_next_cid("file")
        
        state_key = key or f"file:{label}"
        s = self.state(None, key=state_key)
        
        def action(v):
            if v:
                try:
                    # v might be a JSON string if from Lite mode
                    if isinstance(v, str) and v.startswith('{'):
                         try:
                             data = json.loads(v)
                         except:
                             data = v
                    else:
                        data = v
                    
                    if isinstance(data, dict):
                        if "content" in data:
                            # Single file
                            uf = UploadedFile(data.get("name"), data.get("type"), data.get("size"), data.get("content"))
                            s.set(uf)
                            if on_change: on_change(uf)
                            return
                        elif "files" in data:
                             # Multiple files
                             files = []
                             for f_data in data["files"]:
                                 files.append(UploadedFile(f_data.get("name"), f_data.get("type"), f_data.get("size"), f_data.get("content")))
                             s.set(files)
                             if on_change: on_change(files)
                             return
                except Exception as e:
                    print(f"File upload error: {e}")
            
            s.set(None)
            if on_change: on_change(None)
        
        def builder():
            token = rendering_ctx.set(cid)
            cv = s.value
            rendering_ctx.reset(token)
            
            # Build file info display
            if cv:
                if isinstance(cv, list):
                    file_info = f"Uploaded {len(cv)} file(s)"
                else:
                    size_kb = cv.size / 1024
                    size_str = f"{size_kb:.1f}KB" if size_kb < 1024 else f"{size_kb/1024:.1f}MB"
                    file_info = f"Uploaded {cv.name} ({size_str})"
            else:
                file_info = ""
            
            accept_str = accept if accept else "*"
            help_html = f'<div style="font-size:0.75rem;color:var(--vl-text-muted);margin-top:0.25rem;">{help}</div>' if help else ""
            
            html = f'''
            <div class="file-uploader" style="margin-bottom:1rem;">
                <label style="display:block;margin-bottom:0.5rem;font-weight:500;color:var(--vl-text);">{label}</label>
                <input type="file" id="{cid}_input" accept="{accept_str}" {'multiple' if multiple else ''} 
                       style="display:block;padding:0.5rem;border:1px solid var(--vl-border);border-radius:0.25rem;background:var(--vl-bg-card);color:var(--vl-text);width:100%;font-family:inherit;cursor:pointer;" />
                {help_html}
                <div id="{cid}_info" style="margin-top:0.5rem;font-size:0.875rem;color:var(--vl-text-muted);">{file_info}</div>
            </div>
            <script>
            (function() {{
                const input = document.getElementById('{cid}_input');
                const infoDiv = document.getElementById('{cid}_info');
                
                if (input && !input.hasAttribute('data-listener-added')) {{
                    input.setAttribute('data-listener-added', 'true');
                    
                    input.addEventListener('change', function(e) {{
                        const files = e.target.files;
                        if (files && files.length > 0) {{
                            infoDiv.textContent = 'Uploading...';
                            
                            const fileArray = Array.from(files);
                            const promises = fileArray.map(file => {{
                                return new Promise((resolve, reject) => {{
                                    const reader = new FileReader();
                                    reader.onload = function(ev) {{
                                        resolve({{
                                            name: file.name,
                                            type: file.type,
                                            size: file.size,
                                            content: ev.target.result
                                        }});
                                    }};
                                    reader.onerror = function(err) {{
                                        reject(err);
                                    }};
                                    reader.readAsDataURL(file);
                                }});
                            }});
                            
                            Promise.all(promises).then(function(results) {{
                                let payload;
                                if ({'true' if multiple else 'false'}) {{
                                    payload = {{files: results}};
                                }} else {{
                                    payload = results[0];
                                }}
                                
                                // Update UI immediately
                                if ({'true' if multiple else 'false'}) {{
                                    infoDiv.textContent = 'Uploaded ' + results.length + ' file(s)';
                                }} else {{
                                    const file = results[0];
                                    const sizeKB = (file.size / 1024).toFixed(1);
                                    infoDiv.textContent = 'Uploaded ' + file.name + ' (' + sizeKB + ' KB)';
                                }}
                                
                                // Send to backend
                                if (window.sendAction) {{
                                    // WebSocket mode
                                    window.sendAction('{cid}', payload);
                                }} else if (window.htmx) {{
                                    // HTMX mode
                                    htmx.ajax('POST', '/action/{cid}', {{
                                        values: {{ value: JSON.stringify(payload) }},
                                        swap: 'none'
                                    }});
                                }}
                            }}).catch(function(err) {{
                                infoDiv.textContent = 'Upload failed';
                                console.error('File upload error:', err);
                            }});
                        }}
                    }});
                }}
            }})();
            </script>
            '''
            _wd = self._get_widget_defaults("file_uploader")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html, class_=_fc or None, style=_fs or None)
        
        self._register_component(cid, builder, action=action)
        return s

    def toggle(self, label, value=False, key=None, on_change=None,
               disabled=False, label_visibility="visible", help=None,
               cls: str = "", style: str = "", **props):
        """Toggle switch widget

        Args:
            disabled: If True, widget is grayed out
            label_visibility: "visible", "hidden", or "collapsed"
            help: Tooltip / help text
        """
        cid = self._get_next_cid("toggle")
        user_part_cls = props.pop("part_cls", None)
        
        state_key = key or f"toggle:{label}"
        s = self.state(value, key=state_key)
        
        def action(v):
            real_val = str(v).lower() == 'true'
            s.set(real_val)
            if on_change: on_change(real_val)
        
        def builder():
            # Subscribe to own state - client-side will handle smart updates
            token = rendering_ctx.set(cid)
            cv = s.value
            rendering_ctx.reset(token)
            
            checked_attr = 'checked' if cv else ''
            props_str = ' '.join(f'{k}="{v}"' for k, v in props.items() if v is not None and v is not False)
            
            if self.mode == 'lite':
                attrs_str = f'hx-post="/action/{cid}" hx-trigger="change" hx-swap="none" hx-vals="js:{{value: event.target.checked}}"'
                listener_script = ""
            else:
                # WS mode: use addEventListener for Web Awesome custom events
                attrs_str = ""
                listener_script = f'''
                <script>
                (function() {{
                    const el = document.getElementById('{cid}');
                    if (el && !el.hasAttribute('data-ws-listener')) {{
                        el.setAttribute('data-ws-listener', 'true');
                        el.addEventListener('change', function(e) {{
                            window.sendAction('{cid}', el.checked);
                        }});
                    }}
                }})();
                </script>
                '''
            
            disabled_attr = 'disabled' if disabled else ''
            help_html = f'<br><span style="font-size:0.75rem;color:var(--vl-text-muted);">{html_lib.escape(str(help))}</span>' if help else ''
            _wd = self._get_widget_defaults("toggle")
            default_host_cls, default_auto_part_cls = auto_split_widget_cls("toggle", _wd.get("cls", ""))
            user_host_cls, user_auto_part_cls = auto_split_widget_cls("toggle", cls)
            _fc = merge_cls(default_host_cls, user_host_cls)
            _fs = merge_style(_wd.get("style", ""), style)
            _part_cls = merge_part_cls(default_auto_part_cls, _wd.get("part_cls", {}), user_auto_part_cls, user_part_cls)
            part_attr = f' data-vl-part-cls="{html_lib.escape(serialize_part_cls(_part_cls), quote=True)}"' if _part_cls else ''
            part_bridge_script = self._part_bridge_script(f'wa-switch#{cid}[data-vl-part-cls]') if _part_cls else ''
            html = f'<wa-switch id="{cid}"{part_attr} {checked_attr} {disabled_attr} {attrs_str} {props_str}>{label}{help_html}</wa-switch>{listener_script}{part_bridge_script}'
            return Component(None, id=cid, content=wrap_html(html, _fc, _fs))
        self._register_component(cid, builder, action=action)
        return s

    def color_picker(self, label="Pick a color", value="#000000", key=None, on_change=None,
                      disabled=False, label_visibility="visible",
                      cls: str = "", style: str = "", **props):
        """Color picker widget

        Args:
            disabled: If True, widget is grayed out
            label_visibility: "visible", "hidden", or "collapsed"
        """
        cid = self._get_next_cid("color")
        
        state_key = key or f"color:{label}"
        s = self.state(value, key=state_key)
        
        def action(v):
            s.set(v)
            if on_change: on_change(v)
        
        def builder():
            token = rendering_ctx.set(cid)
            cv = s.value
            rendering_ctx.reset(token)
            
            if self.mode == 'lite':
                attrs = {"hx-post": f"/action/{cid}", "hx-trigger": "change", "hx-swap": "none", "name": "value"}
            else:
                attrs = {"onchange": f"window.sendAction('{cid}', this.value)"}
            
            inner = Component("wa-color-picker", id=cid, label=label, value=cv, appearance="outlined", **attrs, **props)
            _wd = self._get_widget_defaults("color_picker")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            if _fc or _fs:
                return Component("div", id=f"{cid}_wrap", content=inner.render(), class_=_fc or None, style=_fs or None)
            return inner
        
        self._register_component(cid, builder, action=action)
        return s

    def date_input(self, label="Select date", value=None, key=None, on_change=None, cls: str = "", style: str = "", **props):
        """Date picker widget"""
        import datetime
        cid = self._get_next_cid("date")
        
        state_key = key or f"date:{label}"
        default_val = value if value else datetime.date.today().isoformat()
        s = self.state(default_val, key=state_key)
        
        def action(v):
            s.set(v)
            if on_change: on_change(v)
        
        def builder():
            token = rendering_ctx.set(cid)
            cv = s.value
            rendering_ctx.reset(token)
            
            if self.mode == 'lite':
                attrs = {"hx-post": f"/action/{cid}", "hx-trigger": "change", "hx-swap": "none", "name": "value"}
            else:
                attrs = {"onchange": f"window.sendAction('{cid}', this.value)"}
            
            html = f'''
            <div style="margin-bottom: 0.5rem;">
                <label style="display:block;margin-bottom:0.5rem;font-weight:500;color:var(--vl-text);">{label}</label>
                <input type="date" id="{cid}_input" value="{cv}" 
                       style="width:100%;padding:0.5rem;border:1px solid var(--vl-border);border-radius:0.5rem;background:var(--vl-bg-card);color:var(--vl-text);font-family:inherit;"
                       {' '.join(f'{k}="{v}"' for k,v in attrs.items())} />
            </div>
            '''
            _wd = self._get_widget_defaults("date_input")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html, class_=_fc or None, style=_fs or None)
        
        self._register_component(cid, builder, action=action)
        return s

    def time_input(self, label="Select time", value=None, key=None, on_change=None, cls: str = "", style: str = "", **props):
        """Time picker widget"""
        import datetime
        cid = self._get_next_cid("time")
        
        state_key = key or f"time:{label}"
        default_val = value if value else datetime.datetime.now().strftime("%H:%M")
        s = self.state(default_val, key=state_key)
        
        def action(v):
            s.set(v)
            if on_change: on_change(v)
        
        def builder():
            token = rendering_ctx.set(cid)
            cv = s.value
            rendering_ctx.reset(token)
            
            if self.mode == 'lite':
                attrs = {"hx-post": f"/action/{cid}", "hx-trigger": "change", "hx-swap": "none", "name": "value"}
            else:
                attrs = {"onchange": f"window.sendAction('{cid}', this.value)"}
            
            html = f'''
            <div style="margin-bottom: 0.5rem;">
                <label style="display:block;margin-bottom:0.5rem;font-weight:500;color:var(--vl-text);">{label}</label>
                <input type="time" id="{cid}_input" value="{cv}" 
                       style="width:100%;padding:0.5rem;border:1px solid var(--vl-border);border-radius:0.5rem;background:var(--vl-bg-card);color:var(--vl-text);font-family:inherit;"
                       {' '.join(f'{k}="{v}"' for k,v in attrs.items())} />
            </div>
            '''
            _wd = self._get_widget_defaults("time_input")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html, class_=_fc or None, style=_fs or None)
        
        self._register_component(cid, builder, action=action)
        return s

    def datetime_input(self, label="Select date and time", value=None, key=None, on_change=None, cls: str = "", style: str = "", **props):
        """DateTime picker widget"""
        import datetime
        cid = self._get_next_cid("datetime")
        
        state_key = key or f"datetime:{label}"
        default_val = value if value else datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
        s = self.state(default_val, key=state_key)
        
        def action(v):
            s.set(v)
            if on_change: on_change(v)
        
        def builder():
            token = rendering_ctx.set(cid)
            cv = s.value
            rendering_ctx.reset(token)
            
            if self.mode == 'lite':
                attrs = {"hx-post": f"/action/{cid}", "hx-trigger": "change", "hx-swap": "none", "name": "value"}
            else:
                attrs = {"onchange": f"window.sendAction('{cid}', this.value)"}
            
            html = f'''
            <div style="margin-bottom: 0.5rem;">
                <label style="display:block;margin-bottom:0.5rem;font-weight:500;color:var(--vl-text);">{label}</label>
                <input type="datetime-local" id="{cid}_input" value="{cv}" 
                       style="width:100%;padding:0.5rem;border:1px solid var(--vl-border);border-radius:0.5rem;background:var(--vl-bg-card);color:var(--vl-text);font-family:inherit;"
                       {' '.join(f'{k}="{v}"' for k,v in attrs.items())} />
            </div>
            '''
            _wd = self._get_widget_defaults("datetime_input")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html, class_=_fc or None, style=_fs or None)
        
        self._register_component(cid, builder, action=action)
        return s

    def _input_component(self, type_name, tag_name, label, value, on_change, key=None, on_submit=None, cls: str = "", style: str = "", live_update=False, label_visibility="visible", **props):
        """Generic input component builder"""
        cid = self._get_next_cid(type_name)
        user_part_cls = props.pop("part_cls", None)
        
        state_key = key or f"{type_name}:{label}"
        s = self.state(value, key=state_key)
        
        def action(v):
            payload = v
            if isinstance(v, str):
                stripped = v.strip()
                if stripped.startswith("{") or stripped.startswith("["):
                    try:
                        payload = json.loads(stripped)
                    except Exception:
                        payload = v

            submitted = isinstance(payload, dict) and payload.get("eventType") == "submit"
            if submitted:
                v = payload.get("value", "")
            else:
                v = payload

            if type_name == 'slider': 
                v = float(v) if '.' in str(v) else int(v)
            s.set(v)
            if submitted:
                if on_submit:
                    on_submit(v)
                elif on_change:
                    on_change(v)
            elif on_change:
                on_change(v)
        
        # Web Awesome form controls emit native input/change events.
        input_event = 'input' if live_update else 'change'
        
        def builder():
            token = rendering_ctx.set(cid)
            cv = s.value
            rendering_ctx.reset(token)
            submit_on_enter = type_name == "input" and bool(on_submit)
            submit_on_enter_js = "true" if submit_on_enter else "false"
            
            if self.mode == 'lite':
                attrs_str = f'hx-post="/action/{cid}" hx-trigger="{input_event}" hx-swap="none" name="value"'
                listener_script = f'''
                <script>
                (function() {{
                    const el = document.getElementById('{cid}');
                    if (!el) return;
                    const shouldSkipEcho = function() {{
                        if (!Object.prototype.hasOwnProperty.call(el, '_vlSkipNextInputEventValue')) return false;
                        const skipValue = el._vlSkipNextInputEventValue;
                        delete el._vlSkipNextInputEventValue;
                        return el.value === skipValue;
                    }};

                    if (!el.hasAttribute('data-vl-echo-guard')) {{
                        el.setAttribute('data-vl-echo-guard', 'true');
                        el.addEventListener('{input_event}', function(event) {{
                            if (!shouldSkipEcho()) return;
                            event.preventDefault();
                            event.stopImmediatePropagation();
                        }}, true);
                    }}

                    const bindSubmitOnEnter = function(attempts) {{
                        if (!{submit_on_enter_js}) return;
                        const inner = el.shadowRoot ? el.shadowRoot.querySelector('input, textarea') : null;
                        const target = inner || (attempts >= 10 ? el : null);
                        if (!target) {{
                            setTimeout(function() {{ bindSubmitOnEnter(attempts + 1); }}, 80);
                            return;
                        }}
                        if (target.hasAttribute('data-vl-submit-listener')) return;
                        target.setAttribute('data-vl-submit-listener', 'true');
                        const allowFocusedUpdateTree = function() {{
                            if (!window._vlAllowNextFocusedUpdate) return;
                            let current = el;
                            while (current) {{
                                if (current.id) {{
                                    window._vlAllowNextFocusedUpdate(current.id);
                                }}
                                current = current.parentElement;
                            }}
                        }};
                        target.addEventListener('keydown', function(event) {{
                            if (event.key !== 'Enter') return;
                            event.preventDefault();
                            el._vlSkipNextInputEventValue = el.value;
                            allowFocusedUpdateTree();
                            const payload = JSON.stringify({{ eventType: 'submit', value: el.value }});
                            htmx.ajax('POST', '/action/{cid}', {{
                                values: {{ value: payload, _vl_lite_stream_dirty: 'true' }},
                                swap: 'none'
                            }});
                        }});
                    }};

                    bindSubmitOnEnter(0);
                }})();
                </script>
                '''
            else:
                # WS mode: use addEventListener for Web Awesome custom events
                attrs_str = ""
                listener_script = f'''
                <script>
                (function() {{
                    const el = document.getElementById('{cid}');
                    const shouldSkipEcho = function() {{
                        if (!el || !Object.prototype.hasOwnProperty.call(el, '_vlSkipNextInputEventValue')) return false;
                        const skipValue = el._vlSkipNextInputEventValue;
                        delete el._vlSkipNextInputEventValue;
                        return el.value === skipValue;
                    }};

                    if (el && !el.hasAttribute('data-ws-listener')) {{
                        el.setAttribute('data-ws-listener', 'true');
                        el.addEventListener('{input_event}', function(e) {{
                            if (shouldSkipEcho()) return;
                            window.sendAction('{cid}', el.value);
                        }});
                    }}

                    const bindSubmitOnEnter = function(attempts) {{
                        if (!el || !{submit_on_enter_js}) return;
                        const inner = el.shadowRoot ? el.shadowRoot.querySelector('input, textarea') : null;
                        const target = inner || (attempts >= 10 ? el : null);
                        if (!target) {{
                            setTimeout(function() {{ bindSubmitOnEnter(attempts + 1); }}, 80);
                            return;
                        }}
                        if (target.hasAttribute('data-vl-submit-listener')) return;
                        target.setAttribute('data-vl-submit-listener', 'true');
                        const allowFocusedUpdateTree = function() {{
                            if (!window._vlAllowNextFocusedUpdate) return;
                            let current = el;
                            while (current) {{
                                if (current.id) {{
                                    window._vlAllowNextFocusedUpdate(current.id);
                                }}
                                current = current.parentElement;
                            }}
                        }};
                        target.addEventListener('keydown', function(event) {{
                            if (event.key !== 'Enter') return;
                            event.preventDefault();
                            el._vlSkipNextInputEventValue = el.value;
                            allowFocusedUpdateTree();
                            window.sendAction('{cid}', {{ eventType: 'submit', value: el.value }});
                        }});
                    }};

                    bindSubmitOnEnter(0);
                }})();
                </script>
                '''
            
            # Build props - handle boolean attrs & hyphenated names (e.g. help-text)
            parts = []
            for k, v in props.items():
                if v is None or v is False:
                    continue
                if v is True:
                    parts.append(k)
                else:
                    parts.append(f'{k}="{v}"')
            props_str = ' '.join(parts)
            escaped_cv = html_lib.escape(str(cv), quote=True)
            # label_visibility support
            _lbl = label
            if label_visibility == "hidden":
                _lbl = ""
            elif label_visibility == "collapsed":
                _lbl = ""
            html = f'<{tag_name} id="{cid}" label="{_lbl}" value="{escaped_cv}" appearance="outlined" {attrs_str} {props_str}></{tag_name}>{listener_script}'
            
            _wd = self._get_widget_defaults(type_name)
            default_host_cls, default_auto_part_cls = auto_split_widget_cls(type_name, _wd.get("cls", ""))
            user_host_cls, user_auto_part_cls = auto_split_widget_cls(type_name, cls)
            _fc = merge_cls(default_host_cls, user_host_cls)
            _fs = merge_style(_wd.get("style", ""), style)
            _part_cls = merge_part_cls(default_auto_part_cls, _wd.get("part_cls", {}), user_auto_part_cls, user_part_cls)
            part_bridge_script = ""
            if _part_cls:
                part_attr = f' data-vl-part-cls="{html_lib.escape(serialize_part_cls(_part_cls), quote=True)}"'
                html = html.replace(f'<{tag_name} id="{cid}"', f'<{tag_name} id="{cid}"{part_attr}', 1)
                part_bridge_script = f'''<script>(function() {{
                    let attempts = 0;
                    const run = function() {{
                        attempts += 1;
                        const el = document.getElementById('{cid}');
                        if (el && el.shadowRoot && window.applyPartStyles) {{
                            window.applyPartStyles(el);
                            return;
                        }}
                        if (attempts < 20) setTimeout(run, 80);
                    }};
                    run();
                }})();</script>'''
            return Component(None, id=cid, content=wrap_html(html + part_bridge_script, _fc, _fs))
        self._register_component(cid, builder, action=action)
        return s
