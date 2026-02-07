"""Media Widgets Mixin for Violit"""

from typing import Union, Optional
import base64
from ..component import Component
from ..context import rendering_ctx
from ..style_utils import merge_cls, merge_style


class MediaWidgetsMixin:
    """Media widgets (image, audio, video)"""
    
    def image(self, image, caption=None, width=None, use_column_width=False, cls: str = "", style: str = "", **props):
        """Display image from various sources"""
        cid = self._get_next_cid("image")
        
        def builder():
            # Handle different image sources
            img_src = ""
            
            if isinstance(image, str):
                # URL or file path
                if image.startswith(('http://', 'https://')):
                    img_src = image
                else:
                    # Local file - read and convert to base64
                    try:
                        import os
                        if os.path.exists(image):
                            with open(image, 'rb') as f:
                                img_data = f.read()
                                img_base64 = base64.b64encode(img_data).decode('utf-8')
                                # Detect image type
                                ext = os.path.splitext(image)[1].lower()
                                mime_types = {'.jpg': 'jpeg', '.jpeg': 'jpeg', '.png': 'png', '.gif': 'gif', '.webp': 'webp'}
                                mime = mime_types.get(ext, 'png')
                                img_src = f"data:image/{mime};base64,{img_base64}"
                    except Exception:
                        img_src = image  # Fallback to treating as URL
            elif hasattr(image, 'read'):
                # File-like object
                img_data = image.read()
                img_base64 = base64.b64encode(img_data).decode('utf-8')
                img_src = f"data:image/png;base64,{img_base64}"
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
                    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
                    img_src = f"data:image/png;base64,{img_base64}"
                except Exception:
                    img_src = str(image)
            
            # Build image HTML
            width_style = ""
            if use_column_width or width == "auto":
                width_style = "width: 100%;"
            elif width:
                width_style = f"width: {width}px;"
            
            caption_html = ""
            if caption:
                caption_html = f'<div style="text-align:center;margin-top:0.5rem;color:var(--sl-text-muted);font-size:0.875rem;">{caption}</div>'
            
            html = f'''
            <div class="image-container" style="text-align:center;">
                <img src="{img_src}" loading="lazy" style="{width_style} height:auto;border-radius:0.5rem;" alt="{caption or ''}" />
                {caption_html}
            </div>
            '''
            _wd = self._get_widget_defaults("image")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html, class_=_fc or None, style=_fs or None)
        
        self._register_component(cid, builder)

    def audio(self, audio, format="audio/mp3", start_time=0, cls: str = "", style: str = "", **props):
        """Display audio player"""
        cid = self._get_next_cid("audio")
        
        def builder():
            # Handle different audio sources
            audio_src = ""
            
            if isinstance(audio, str):
                if audio.startswith(('http://', 'https://')):
                    audio_src = audio
                else:
                    # Local file - read and convert to base64
                    try:
                        import os
                        if os.path.exists(audio):
                            with open(audio, 'rb') as f:
                                audio_data = f.read()
                                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                                audio_src = f"data:{format};base64,{audio_base64}"
                    except Exception:
                        audio_src = audio
            elif hasattr(audio, 'read'):
                audio_data = audio.read()
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                audio_src = f"data:{format};base64,{audio_base64}"
            else:
                # Numpy array (audio waveform)
                try:
                    import numpy as np
                    import scipy.io.wavfile as wavfile
                    import io
                    
                    buf = io.BytesIO()
                    wavfile.write(buf, 44100, audio)
                    buf.seek(0)
                    audio_base64 = base64.b64encode(buf.read()).decode('utf-8')
                    audio_src = f"data:audio/wav;base64,{audio_base64}"
                except Exception:
                    audio_src = str(audio)
            
            html = f'''
            <audio controls style="width:100%;border-radius:0.5rem;">
                <source src="{audio_src}" type="{format}">
                Your browser does not support the audio element.
            </audio>
            '''
            _wd = self._get_widget_defaults("audio")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html, class_=_fc or None, style=_fs or None)
        
        self._register_component(cid, builder)

    def video(self, video, format="video/mp4", start_time=0, cls: str = "", style: str = "", **props):
        """Display video player"""
        cid = self._get_next_cid("video")
        
        def builder():
            # Handle different video sources
            video_src = ""
            
            if isinstance(video, str):
                if video.startswith(('http://', 'https://')):
                    video_src = video
                else:
                    # Local file - read and convert to base64
                    try:
                        import os
                        if os.path.exists(video):
                            with open(video, 'rb') as f:
                                video_data = f.read()
                                video_base64 = base64.b64encode(video_data).decode('utf-8')
                                video_src = f"data:{format};base64,{video_base64}"
                    except Exception:
                        video_src = video
            elif hasattr(video, 'read'):
                video_data = video.read()
                video_base64 = base64.b64encode(video_data).decode('utf-8')
                video_src = f"data:{format};base64,{video_base64}"
            else:
                video_src = str(video)
            
            html = f'''
            <video controls style="width:100%;border-radius:0.5rem;">
                <source src="{video_src}" type="{format}">
                Your browser does not support the video element.
            </video>
            '''
            _wd = self._get_widget_defaults("video")
            _fc = merge_cls(_wd.get("cls", ""), cls)
            _fs = merge_style(_wd.get("style", ""), style)
            return Component("div", id=cid, content=html, class_=_fc or None, style=_fs or None)
        
        self._register_component(cid, builder)
