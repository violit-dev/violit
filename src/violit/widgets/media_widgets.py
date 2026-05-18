"""Media Widgets Mixin for Violit"""

from typing import Union, Optional
import base64
import mimetypes
import os
import urllib.parse
import uuid
from ..component import Component
from ..context import rendering_ctx, session_ctx, view_ctx
from ..state import get_session_store
from ..style_utils import merge_cls, merge_style


def _media_data_url(file_bytes: bytes, media_type: str) -> str:
    if not file_bytes:
        return ""
    encoded = base64.b64encode(file_bytes).decode("utf-8")
    return f"data:{media_type};base64,{encoded}"


def _guess_media_type(path: str, fallback: str) -> str:
    guessed, _ = mimetypes.guess_type(path)
    return guessed or fallback


def _media_public_url(app, path: str, media_type: str) -> str:
    if session_ctx.get() is None:
        try:
            with open(path, "rb") as handle:
                return _media_data_url(handle.read(), media_type)
        except Exception:
            return path

    resolved_path = os.path.abspath(path)
    store = get_session_store()
    registry = store.setdefault("_vl_media_sources", {})
    media_id = uuid.uuid4().hex
    registry[media_id] = {
        "path": resolved_path,
        "media_type": media_type,
        "name": os.path.basename(resolved_path) or "media",
    }
    url = app._public_path(f"/__violit_media/{media_id}")
    current_view_id = str(view_ctx.get() or "").strip()
    if not current_view_id:
        return url

    separator = "&" if "?" in url else "?"
    return f"{url}{separator}_vl_view_id={urllib.parse.quote(current_view_id, safe='')}"


def _resolve_local_media_src(app, source: str, fallback_media_type: str) -> str:
    if source.startswith(("http://", "https://", "data:", "blob:")):
        return source
    if not os.path.exists(source):
        return source

    media_type = _guess_media_type(source, fallback_media_type)
    return _media_public_url(app, source, media_type)


class MediaWidgetsMixin:
    """Media widgets (image, audio, video)"""
    
    def image(self, image, caption=None, width=None, use_column_width=False, use_container_width=False, cls: str = "", style: str = "", key=None, **props):
        """Display image from various sources"""
        cid = self._resolve_widget_cid("image", key)
        
        def builder():
            # Handle different image sources
            img_src = ""
            
            if isinstance(image, str):
                img_src = _resolve_local_media_src(self, image, "image/png")
            elif hasattr(image, 'read'):
                # File-like object
                img_data = image.read()
                img_src = _media_data_url(img_data, "image/png")
            else:
                # Try numpy array (PIL Image, etc.)
                try:
                    from PIL import Image
                    import io
                    import numpy as np
                    
                    if isinstance(image, np.ndarray):
                        pil_img = Image.fromarray(image)
                    else:
                        pil_img = image
                    
                    buf = io.BytesIO()
                    pil_img.save(buf, format='PNG')
                    buf.seek(0)
                    img_src = _media_data_url(buf.read(), "image/png")
                except Exception:
                    img_src = str(image)
            
            # Build image HTML
            width_style = ""
            if use_container_width or use_column_width or width == "auto":
                width_style = "width: 100%;"
            elif width:
                width_style = f"width: {width if isinstance(width, str) else str(width) + 'px'};"
            
            caption_html = ""
            if caption:
                caption_html = f'<div style="text-align:center;margin-top:0.5rem;color:var(--vl-text-muted);font-size:0.875rem;">{caption}</div>'
            
            # Modal HTML for enlarged image
            modal_id = f"modal-{cid}"
            close_button_id = f"{modal_id}-close"
            modal_html = f'''
            <wa-dialog id="{modal_id}" without-header light-dismiss with-footer style="--width: 100%; position: fixed; z-index: 10000;">
                <div style="display: flex; justify-content: center; align-items: center; background: rgba(0,0,0,0.05); border-radius: 0.5rem; overflow: hidden; padding: 1rem;">
                    <img src="{img_src}" style="max-width: 100%; max-height: 70vh; object-fit: contain; box-shadow: 0 10px 25px rgba(0,0,0,0.2);" />
                </div>
                {caption_html}
                <div slot="footer" style="padding: 0; display: flex; justify-content: flex-end;">
                    <button id="{close_button_id}" type="button" style="background: linear-gradient(135deg, #7c3aed, #2563eb); color: white; border: none; border-radius: 0.85rem; padding: 0.75rem 1.2rem; font-weight: 700; cursor: pointer; box-shadow: 0 4px 14px rgba(124,58,237,0.2);">Close</button>
                </div>
                <style>
                    #{modal_id} {{
                        --vl-panel-background-color: white;
                    }}
                    #{modal_id}::part(panel) {{
                        max-width: 900px;
                        width: calc(100% - 40px);
                        border-radius: 1rem;
                    }}
                    #{modal_id}::part(overlay) {{
                        backdrop-filter: blur(8px);
                        background-color: rgba(0, 0, 0, 0.4);
                    }}
                    #{modal_id}::part(body) {{
                        padding: 1.5rem;
                    }}
                    /* Force the dialog to be contained within the main content area if possible, 
                       or at least push it away from the sidebar */
                    #{modal_id}::part(base) {{
                        margin-left: 0;
                        padding-left: 0;
                    }}
                    
                    @media (min-width: 769px) {{
                        /* On desktop, keep the dialog centered in the remaining space of the main area */
                        #{modal_id}::part(base) {{
                            padding-left: var(--vl-sidebar-width, 300px);
                        }}
                        /* If sidebar is collapsed, adjust padding */
                        .sidebar-collapsed #{modal_id}::part(base) {{
                            padding-left: 0;
                        }}
                    }}
                </style>
            </wa-dialog>
            <script>
                (() => {{
                    const dialog = document.getElementById('{modal_id}');
                    const closeButton = document.getElementById('{close_button_id}');
                    if (!dialog || !closeButton || closeButton.dataset.vlBound === 'true') return;
                    closeButton.dataset.vlBound = 'true';
                    closeButton.addEventListener('click', () => {{
                        if (typeof dialog.requestClose === 'function') {{
                            dialog.requestClose(closeButton);
                            return;
                        }}
                        if (dialog.dialog && typeof dialog.dialog.close === 'function') {{
                            dialog.dialog.close();
                            return;
                        }}
                        dialog.open = false;
                    }});
                }})();
            </script>
            '''

            html = f'''
            <div class="image-container" style="text-align:center;">
                <img src="{img_src}" loading="lazy" 
                     style="{width_style} height:auto; border-radius:0.5rem; cursor: zoom-in;" 
                     alt="{caption or ''}" 
                     onclick="document.getElementById('{modal_id}').show()" />
                {caption_html}
            </div>
            {modal_html}
            '''
            _wd = self._get_widget_defaults("image")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html, class_=_fc or None, style=_fs or None)
        
        self._register_component(cid, builder)

    def audio(self, audio, format="audio/mp3", start_time=0, loop=False, autoplay=False, end_time=None, sample_rate=None, cls: str = "", style: str = "", key=None, **props):
        """Display audio player"""
        cid = self._resolve_widget_cid("audio", key)
        
        def builder():
            # Handle different audio sources
            audio_src = ""
            
            if isinstance(audio, str):
                audio_src = _resolve_local_media_src(self, audio, format)
            elif hasattr(audio, 'read'):
                audio_data = audio.read()
                audio_src = _media_data_url(audio_data, format)
            else:
                # Numpy array (audio waveform)
                try:
                    import numpy as np
                    import scipy.io.wavfile as wavfile
                    import io
                    
                    buf = io.BytesIO()
                    wavfile.write(buf, 44100, audio)
                    buf.seek(0)
                    audio_src = _media_data_url(buf.read(), "audio/wav")
                except Exception:
                    audio_src = str(audio)
            
            # Audio attrs
            audio_attrs = ["controls"]
            if loop: audio_attrs.append("loop")
            if autoplay: audio_attrs.append("autoplay")

            html = f'''
            <audio {" ".join(audio_attrs)} style="width:100%;border-radius:0.5rem;">
                <source src="{audio_src}" type="{format}">
                Your browser does not support the audio element.
            </audio>
            '''
            _wd = self._get_widget_defaults("audio")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html, class_=_fc or None, style=_fs or None)
        
        self._register_component(cid, builder)

    def video(self, video, format="video/mp4", start_time=0, caption=None, width=None, use_column_width=False, autoplay=False, loop=False, muted=False, cls: str = "", style: str = "", key=None, **props):
        """Display video player with various controls and sources"""
        cid = self._resolve_widget_cid("video", key)
        
        def builder():
            # Handle different video sources
            video_src = ""
            
            if isinstance(video, str):
                video_src = _resolve_local_media_src(self, video, format)
            elif hasattr(video, 'read'):
                video_data = video.read()
                video_src = _media_data_url(video_data, format)
            else:
                video_src = str(video)
            
            # Handle start time
            if start_time > 0 and "#t=" not in video_src:
                video_src = f"{video_src}#t={start_time}"
            
            # Additional attributes
            attrs = ["controls"]
            if autoplay: attrs.append("autoplay")
            if loop: attrs.append("loop")
            if muted: attrs.append("muted")
            
            # Width styling
            width_style = ""
            if use_column_width or width == "auto":
                width_style = "width: 100%;"
            elif width:
                width_style = f"width: {width}px;"
            else:
                width_style = "width: 100%;" # Default to 100% for video

            caption_html = ""
            if caption:
                caption_html = f'<div style="text-align:center;margin-top:0.5rem;color:var(--vl-text-muted);font-size:0.875rem;">{caption}</div>'
            
            html = f'''
            <div class="video-container" style="text-align:center; position: relative;">
                <video {" ".join(attrs)} style="{width_style} height:auto; border-radius:12px; box-shadow: 0 4px 20px rgba(0,0,0,0.15); border: 1px solid var(--vl-border);">
                    <source src="{video_src}" type="{format}">
                    Your browser does not support the video element.
                </video>
                {caption_html}
            </div>
            '''
            _wd = self._get_widget_defaults("video")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html, class_=_fc or None, style=_fs or None)
        
        self._register_component(cid, builder)
