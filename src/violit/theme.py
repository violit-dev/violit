class Theme:
    """Theme management class"""
    PRESETS = {
        'dark': {
            'mode': 'dark',
            'primary': '#a78bfa',      # Purple
            'secondary': '#f472b6',    # Pink
            'success': '#22c55e',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'bg': '#09090b',
            'bg_card': '#18181b',
            'border': '#27272a',
            'text': '#fafafa',
            'text_muted': '#a1a1aa',
            'radius': '0.75rem',
            'input_border_radius_small': '0.375rem',
            'input_border_radius_medium': '0.75rem',
            'input_border_radius_large': '1.0rem',
        },
        'light': {
            'mode': 'light',
            'primary': '#7c3aed',
            'secondary': '#ec4899',
            'success': '#16a34a',
            'warning': '#ea580c',
            'danger': '#dc2626',
            'bg': '#ffffff',
            'bg_card': '#f9fafb',
            'border': '#e5e7eb',
            'text': '#0f172a',
            'text_muted': '#64748b',
            'radius': '0.75rem',
            'input_border_radius_small': '0.375rem',
            'input_border_radius_medium': '0.75rem',
            'input_border_radius_large': '1.0rem',
        },
        'ocean': {
            'mode': 'dark',
            'primary': '#06b6d4',      # Cyan
            'secondary': '#3b82f6',    # Blue
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'bg': '#0c1222',
            'bg_card': '#1e293b',
            'border': '#334155',
            'text': '#f1f5f9',
            'text_muted': '#94a3b8',
            'radius': '0.75rem',
            'input_border_radius_small': '0.375rem',
            'input_border_radius_medium': '0.75rem',
            'input_border_radius_large': '1.0rem',
        },
        'sunset': {
            'mode': 'dark',
            'primary': '#f97316',      # Orange
            'secondary': '#ec4899',    # Pink
            'success': '#22c55e',
            'warning': '#fbbf24',
            'danger': '#ef4444',
            'bg': '#1c1917',
            'bg_card': '#292524',
            'border': '#44403c',
            'text': '#fafaf9',
            'text_muted': '#a8a29e',
            'radius': '0.75rem',
            'input_border_radius_small': '0.375rem',
            'input_border_radius_medium': '0.75rem',
            'input_border_radius_large': '1.0rem',
        },
        'forest': {
            'mode': 'dark',
            'primary': '#22c55e',      # Green
            'secondary': '#84cc16',    # Lime
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'bg': '#0a0f0a',
            'bg_card': '#14532d',
            'border': '#166534',
            'text': '#f0fdf4',
            'text_muted': '#86efac',
            'radius': '0.75rem',
            'input_border_radius_small': '0.375rem',
            'input_border_radius_medium': '0.75rem',
            'input_border_radius_large': '1.0rem',
        },
        'cyberpunk': {
            'mode': 'dark',
            'primary': '#00ffea',      # Neon Cyan
            'secondary': '#ff00ff',    # Neon Magenta
            'success': '#00ff00',
            'warning': '#ffff00',
            'danger': '#ff0000',
            'bg': '#050510',           # Deep Black/Blue
            'bg_card': '#0a0a1f',
            'border': '#00ffea',       # Cyan borders
            'text': '#ffffff',
            'text_muted': '#008f82',
            'radius': '0px',           # Sharp edges
            'input_border_radius_small': '0px',
            'input_border_radius_medium': '0px',
            'input_border_radius_large': '0px',
        },
        'pastel': {
            'mode': 'light',
            'primary': '#b8c0ff',      # Pastel Blue/Purple
            'secondary': '#ffc8dd',    # Pastel Pink
            'success': '#99e2b4',
            'warning': '#faedcb',
            'danger': '#ffadad',
            'bg': '#fff0f3',           # Very light pinkish
            'bg_card': '#ffffff',
            'border': '#ffe5ec',
            'text': '#4a4e69',
            'text_muted': '#9a8c98',
            'radius': '1.5rem',        # Extra rounded
            'input_border_radius_small': '0.75rem',
            'input_border_radius_medium': '1.5rem',
            'input_border_radius_large': '2rem',
        },
        'retro': {
            'mode': 'light',
            'primary': '#d97706',      # Amber
            'secondary': '#92400e',    # Brown
            'success': '#15803d',
            'warning': '#b45309',
            'danger': '#b91c1c',
            'bg': '#fef3c7',           # Warm Beige
            'bg_card': '#fffbeb',
            'border': '#78350f',
            'text': '#451a03',
            'text_muted': '#92400e',
            'radius': '2px',           # Blocky
            'input_border_radius_small': '1px',
            'input_border_radius_medium': '2px',
            'input_border_radius_large': '3px',
        },
        'dracula': {
            'mode': 'dark',
            'primary': '#bd93f9',
            'secondary': '#ff79c6',
            'success': '#50fa7b',
            'warning': '#ffb86c',
            'danger': '#ff5555',
            'bg': '#282a36',
            'bg_card': '#44475a',
            'border': '#6272a4',
            'text': '#f8f8f2',
            'text_muted': '#6272a4',
            'radius': '0.5rem',
            'input_border_radius_small': '0.25rem',
            'input_border_radius_medium': '0.5rem',
            'input_border_radius_large': '0.75rem',
        },
        'monokai': {
            'mode': 'dark',
            'primary': '#a6e22e',      # Green
            'secondary': '#f92672',    # Pink
            'success': '#a6e22e',
            'warning': '#fd971f',
            'danger': '#f92672',
            'bg': '#272822',
            'bg_card': '#3e3d32',
            'border': '#75715e',
            'text': '#f8f8f2',
            'text_muted': '#75715e',
            'radius': '0.25rem',
            'input_border_radius_small': '0.125rem',
            'input_border_radius_medium': '0.25rem',
            'input_border_radius_large': '0.375rem',
        },
        'ant': {
            'mode': 'light',
            'primary': '#1890ff',      # Ant Blue
            'secondary': '#722ed1',    # Ant Purple
            'success': '#52c41a',
            'warning': '#faad14',
            'danger': '#f5222d',
            'bg': '#f0f2f5',           # Ant Light Gray BG
            'bg_card': '#ffffff',
            'border': '#d9d9d9',
            'text': '#000000',
            'text_muted': '#00000073', # 45% alpha
            'radius': '2px',           # Slightly rounded
            'input_border_radius_small': '2px',
            'input_border_radius_medium': '2px',
            'input_border_radius_large': '2px',
        },
        'bootstrap': {
            'mode': 'light',
            'primary': '#0d6efd',      # BS Blue
            'secondary': '#6c757d',    # BS Gray
            'success': '#198754',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'bg': '#ffffff',
            'bg_card': '#f8f9fa',      # Light
            'border': '#dee2e6',
            'text': '#212529',
            'text_muted': '#6c757d',
            'radius': '0.375rem',      # BS rounded
            'input_border_radius_small': '0.25rem',
            'input_border_radius_medium': '0.375rem',
            'input_border_radius_large': '0.5rem',
        },
        'material': {
            'mode': 'light',
            'primary': '#6750a4',      # M3 Purple
            'secondary': '#625b71',
            'success': '#468b58',
            'warning': '#7e5700',
            'danger': '#ba1a1a',
            'bg': '#fffbfe',           # M3 Surface
            'bg_card': '#f7f2fa',      # M3 Surface Variant
            'border': '#79747e',
            'text': '#1c1b1f',
            'text_muted': '#49454f',
            'radius': '1.5rem',        # M3 generally very rounded
            'input_border_radius_small': '0.75rem',
            'input_border_radius_medium': '1.5rem',
            'input_border_radius_large': '1.75rem',
        },
        'glass': {
            'mode': 'light',
            'primary': '#007aff',      # Apple Blue
            'secondary': '#5856d6',    # Apple Purple
            'success': '#34c759',
            'warning': '#ff9500',
            'danger': '#ff3b30',
            'bg': '#f5f5f7',           # Apple Gray BG
            'bg_card': '#ffffffcc',    # Translucent White
            'border': '#d1d1d6',
            'text': '#1d1d1f',
            'text_muted': '#86868b',
            'radius': '16px',          # Apple-like rounded
            'input_border_radius_small': '8px',
            'input_border_radius_medium': '12px',
            'input_border_radius_large': '16px',
        },
        'nord': {
            'mode': 'dark',
            'primary': '#88c0d0',      # Nord Frost
            'secondary': '#81a1c1',
            'success': '#a3be8c',
            'warning': '#ebcb8b',
            'danger': '#bf616a',
            'bg': '#2e3440',           # Nord Dark
            'bg_card': '#3b4252',
            'border': '#434c5e',
            'text': '#eceff4',
            'text_muted': '#d8dee9',
            'radius': '0.25rem',
            'input_border_radius_small': '0.125rem',
            'input_border_radius_medium': '0.25rem',
            'input_border_radius_large': '0.375rem',
        },
        # === NEW ADVANCED THEMES ===
        'neo_brutalism': {
            'mode': 'light',
            'primary': '#000000',
            'secondary': '#ff00ff',
            'success': '#00ff00',
            'warning': '#ffff00',
            'danger': '#ff0000',
            'bg': '#f0f0f0',
            'bg_card': '#ffffff',
            'border': '#000000',
            'text': '#000000',
            'text_muted': '#444444',
            'radius': '0px',
            'input_border_radius_small': '0px',
            'input_border_radius_medium': '0px',
            'input_border_radius_large': '0px',
            'extra_css': """
                body { font-family: 'Courier New', monospace; font-weight: bold; }
                .card { border: 3px solid black !important; box-shadow: 5px 5px 0px 0px black !important; }
                sl-button::part(base) { border: 3px solid black !important; box-shadow: 4px 4px 0px 0px black !important; transition: transform 0.1s !important; }
                sl-button::part(base):active { transform: translate(2px, 2px) !important; box-shadow: 2px 2px 0px 0px black !important; }
                h1, h2, h3 { text-transform: uppercase; border-bottom: 3px solid black; display: inline-block; padding-bottom: 5px; }
            """
        },
        'soft_neu': {
            'mode': 'light',
            'primary': '#e0e5ec', # Monochromatic
            'secondary': '#a3b1c6',
            'success': '#e0e5ec', # Using shape instead of color mostly
            'warning': '#e0e5ec',
            'danger': '#e0e5ec',
            'bg': '#e0e5ec',
            'bg_card': '#e0e5ec',
            'border': '#transparent',
            'text': '#4a5568',
            'text_muted': '#a0aec0',
            'radius': '20px',
            'input_border_radius_small': '10px',
            'input_border_radius_medium': '15px',
            'input_border_radius_large': '20px',
            'extra_css': """
                .card { 
                    border: none !important;
                    background: #e0e5ec !important;
                    box-shadow: 9px 9px 16px rgb(163,177,198,0.6), -9px -9px 16px rgba(255,255,255, 0.5) !important; 
                }
                sl-button::part(base) {
                    border: none !important;
                    background: #e0e5ec !important;
                    color: #4a5568 !important;
                    box-shadow: 6px 6px 10px 0 rgba(163,177,198, 0.7), -6px -6px 10px 0 rgba(255,255,255, 0.8) !important;
                    transition: all 0.2s ease;
                }
                sl-button::part(base):active {
                    box-shadow: inset 6px 6px 10px 0 rgba(163,177,198, 0.7), inset -6px -6px 10px 0 rgba(255,255,255, 0.8) !important;
                }
                sl-input::part(base) {
                    background: #e0e5ec !important;
                    box-shadow: inset 6px 6px 10px 0 rgba(163,177,198, 0.7), inset -6px -6px 10px 0 rgba(255,255,255, 0.8) !important;
                    border: none !important;
                }
            """
        },
        'cyber_hud': {
            'mode': 'dark',
            'primary': '#0ff',
            'secondary': '#f0f',
            'success': '#0f0',
            'warning': '#ff0',
            'danger': '#f00',
            'bg': '#000000',
            'bg_card': '#050a10',
            'border': '#0ff',
            'text': '#0ff',
            'text_muted': '#008888',
            'radius': '0px',
            'input_border_radius_small': '0px',
            'input_border_radius_medium': '0px',
            'input_border_radius_large': '0px',
            'extra_css': """
                body { 
                    background-image: linear-gradient(rgba(0, 255, 255, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 255, 255, 0.05) 1px, transparent 1px);
                    background-size: 20px 20px;
                }
                .card {
                    border: 1px solid #0ff !important;
                    box-shadow: 0 0 10px #0ff, inset 0 0 20px rgba(0,255,255,0.1) !important;
                    clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
                }
                sl-button::part(base) {
                    border: 1px solid #0ff !important;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                    clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
                }
                sl-button::part(base):hover {
                    background: #0ff !important;
                    color: #000 !important;
                    box-shadow: 0 0 20px #0ff !important;
                }
            """
        },
        'hand_drawn': {
            'mode': 'light',
            'primary': '#2c3e50',
            'secondary': '#e67e22',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#c0392b',
            'bg': '#fffefa', # Paper color
            'bg_card': '#ffffff',
            'border': '#2c3e50',
            'text': '#2c3e50',
            'text_muted': '#7f8c8d',
            'radius': '255px 15px 225px 15px / 15px 225px 15px 255px',
            'input_border_radius_small': '255px 15px 225px 15px / 15px 225px 15px 255px',
            'input_border_radius_medium': '255px 15px 225px 15px / 15px 225px 15px 255px',
            'input_border_radius_large': '255px 15px 225px 15px / 15px 225px 15px 255px',
            'extra_css': """
                body { font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif; }
                .card {
                    border: 2px solid #2c3e50 !important;
                    border-radius: 255px 15px 225px 15px / 15px 225px 15px 255px !important;
                    box-shadow: 2px 3px 15px rgba(0,0,0,0.1) !important;
                }
                sl-button::part(base) {
                    border: 2px solid #2c3e50 !important;
                    border-radius: 255px 15px 225px 15px / 15px 225px 15px 255px !important;
                }
                sl-input::part(base) {
                    border: 2px solid #2c3e50 !important;
                    border-radius: 255px 15px 225px 15px / 15px 225px 15px 255px !important;
                }
             """
        },
        'terminal': {
            'mode': 'dark',
            'primary': '#00ff00',
            'secondary': '#00cc00', 
            'success': '#00ff00',
            'warning': '#ffff00',
            'danger': '#ff0000',
            'bg': '#0a0a0a',
            'bg_card': '#000000',
            'border': '#00ff00',
            'text': '#00ff00',
            'text_muted': '#008800',
            'radius': '0px',
            'input_border_radius_small': '0px',
            'input_border_radius_medium': '0px',
            'input_border_radius_large': '0px',
            'extra_css': """
                body { font-family: 'Courier New', monospace; }
                .card { border: 1px dashed #00ff00 !important; }
                sl-button::part(base) { 
                    border: 1px solid #00ff00 !important; 
                    background: black !important;
                    color: #00ff00 !important;
                }
                sl-button::part(base):hover { 
                    background: #00ff00 !important; 
                    color: black !important;
                }
                * { text-shadow: 0 0 2px #00ff00; }
            """
        },
        'win95': {
            'mode': 'light',
            'primary': '#000080',
            'secondary': '#808080',
            'success': '#008000',
            'warning': '#808000',
            'danger': '#ff0000',
            'bg': '#008080', # Teal desktop
            'bg_card': '#c0c0c0',
            'border': '#dfdfdf',
            'text': '#000000',
            'text_muted': '#808080',
            'radius': '0px',
            'input_border_radius_small': '0px',
            'input_border_radius_medium': '0px',
            'input_border_radius_large': '0px',
            'extra_css': """
                body { font-family: 'Tahoma', 'MS Sans Serif', sans-serif; }
                .card, sl-button::part(base) {
                    background: #c0c0c0 !important;
                    border-top: 2px solid #ffffff !important;
                    border-left: 2px solid #ffffff !important;
                    border-right: 2px solid #000000 !important;
                    border-bottom: 2px solid #000000 !important;
                    box-shadow: 1px 1px 0px 0px #000 inset, -1px -1px 0px 0px #fff inset !important;
                }
                sl-button::part(base):active {
                     border-top: 2px solid #000000 !important;
                    border-left: 2px solid #000000 !important;
                    border-right: 2px solid #ffffff !important;
                    border-bottom: 2px solid #ffffff !important;
                }
            """
        },
        'bauhaus': {
            'mode': 'light',
            'primary': '#d02224', # Red
            'secondary': '#1669b7', # Blue
            'success': '#f9bc2c', # Yellow
            'warning': '#f9bc2c',
            'danger': '#d02224',
            'bg': '#f5f5f5',
            'bg_card': '#ffffff',
            'border': '#000000',
            'text': '#111111',
            'text_muted': '#555555',
            'radius': '0px', 
            'input_border_radius_small': '0px',
            'input_border_radius_medium': '0px',
            'input_border_radius_large': '0px',
            'extra_css': """
                .card {
                    border: none !important;
                    box-shadow: 10px 10px 0 #1669b7, 20px 20px 0 #d02224 !important;
                    transition: transform 0.2s;
                }
                .card:hover { transform: translate(-2px, -2px); }
                sl-button::part(base) {
                    border-radius: 9999px !important; /* Circle/Pill */
                    border: none !important;
                    box-shadow: 4px 4px 0 #000000 !important;
                }
                h1 { color: #d02224; }
                h2 { color: #1669b7; }
                h3 { color: #f9bc2c; text-shadow: 1px 1px 0 #000; }
            """
        },
        'vaporwave': {
            'mode': 'dark',
            'primary': '#ff71ce', # Neon Pink
            'secondary': '#01cdfe', # Neon Cyan
            'success': '#05ffa1',
            'warning': '#b967ff',
            'danger': '#ff71ce',
            'bg': '#2b2144',
            'bg_card': '#1a1429',
            'border': '#b967ff',
            'text': '#fffb96', # Yellowish
            'text_muted': '#b967ff',
            'radius': '0px',
            'input_border_radius_small': '0px',
            'input_border_radius_medium': '0px',
            'input_border_radius_large': '0px',
            'extra_css': """
                body {
                    background: linear-gradient(180deg, #2b2144 0%, #000000 100%);
                    min-height: 100vh;
                }
                .card {
                    background: rgba(26, 20, 41, 0.8) !important;
                    border: 2px solid #01cdfe !important;
                    box-shadow: 0 0 15px #b967ff, inset 0 0 15px #b967ff !important;
                }
                sl-button::part(base) {
                    background: linear-gradient(45deg, #ff71ce, #01cdfe) !important;
                    color: white !important;
                    border: none !important;
                    text-transform: uppercase;
                    font-style: italic;
                }
                h1, h2, h3 { 
                    background: linear-gradient(to right, #ff71ce, #01cdfe);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    filter: drop-shadow(2px 2px 0px rgba(0,0,0,0.5));
                }
            """
        },
        'blueprint': {
            'mode': 'dark',
            'primary': '#ffffff',
            'secondary': '#ffffff',
            'success': '#ffffff',
            'warning': '#ffffff',
            'danger': '#ffffff',
            'bg': '#0044bb', # Blueprint Blue
            'bg_card': 'transparent',
            'border': '#ffffff',
            'text': '#ffffff',
            'text_muted': '#aaccff',
            'radius': '0px',
            'input_border_radius_small': '0px',
            'input_border_radius_medium': '0px',
            'input_border_radius_large': '0px',
            'extra_css': """
                body {
                    background-image: 
                        linear-gradient(rgba(255,255,255,0.3) 1px, transparent 1px),
                        linear-gradient(90deg, rgba(255,255,255,0.3) 1px, transparent 1px);
                    background-size: 20px 20px;
                }
                .card {
                    border: 2px solid white !important;
                    background: rgba(0, 60, 180, 0.5) !important;
                }
                sl-button::part(base) {
                    background: transparent !important;
                    border: 2px solid white !important;
                    color: white !important;
                }
                sl-button::part(base):hover {
                    background: rgba(255,255,255,0.2) !important;
                }
                * { font-family: 'Courier New', monospace !important; }
            """
        },
        'rgb_gamer': {
            'mode': 'dark',
            'primary': '#ff0000',
            'secondary': '#00ff00',
            'success': '#0000ff',
            'warning': '#ffff00',
            'danger': '#ff0000',
            'bg': '#000000',
            'bg_card': '#111111',
            'border': '#333333',
            'text': '#ffffff',
            'text_muted': '#888888',
            'radius': '8px',
            'input_border_radius_small': '4px',
            'input_border_radius_medium': '8px',
            'input_border_radius_large': '12px',
            'extra_css': """
                @keyframes hue-rotate {
                    from { filter: hue-rotate(0deg); }
                    to { filter: hue-rotate(360deg); }
                }
                .card {
                    position: relative;
                    border: 2px solid red;
                    animation: hue-rotate 3s linear infinite;
                    box-shadow: 0 0 10px red;
                }
                sl-button::part(base) {
                    border: 2px solid red;
                    animation: hue-rotate 3s linear infinite reverse;
                }
            """
        },
         'editorial': {
            'mode': 'light',
            'primary': '#000000',
            'secondary': '#444444',
            'success': '#000000',
            'warning': '#000000',
            'danger': '#ff0000',
            'bg': '#ffffff',
            'bg_card': '#ffffff',
            'border': '#000000',
            'text': '#000000',
            'text_muted': '#666666',
            'radius': '0px',
            'input_border_radius_small': '0px',
            'input_border_radius_medium': '0px',
            'input_border_radius_large': '0px',
            'extra_css': """
                body { font-family: 'Times New Roman', serif; }
                h1, h2, h3 { font-family: 'Georgia', serif; font-style: italic; border-bottom: 4px double black; padding-bottom: 0.5rem; display: block; }
                .card {
                    border: none !important;
                    border-bottom: 1px solid black !important;
                    border-top: 1px solid black !important;
                    border-radius: 0 !important;
                    box-shadow: none !important;
                }
                sl-button::part(base) {
                    font-family: 'Times New Roman', serif;
                    text-transform: uppercase;
                    background: transparent !important;
                    color: black !important;
                    border: 1px solid black !important;
                    font-weight: bold;
                }
                sl-button::part(base):hover {
                    background: black !important;
                    color: white !important;
                }
            """
        },
        'claymorphism': {
            'mode': 'light',
            'primary': '#ff8c69', # Soft coral
            'secondary': '#6ab7ff', # Soft blue
            'success': '#81e698',
            'warning': '#ffd685',
            'danger': '#ff8c69',
            'bg': '#f0f4f8',
            'bg_card': '#ffffff',
            'border': '#ffffff',
            'text': '#5e6c7e',
            'text_muted': '#9aa5b1',
            'radius': '30px',
            'input_border_radius_small': '15px',
            'input_border_radius_medium': '30px',
            'input_border_radius_large': '45px',
            'extra_css': """
                .card {
                    border-radius: 30px !important;
                    border: none !important;
                    box-shadow: inset 10px 10px 20px #dbe4f0, inset -10px -10px 20px #ffffff, 10px 20px 30px rgba(166, 180, 200, 0.4) !important;
                    background: #f0f4f8 !important;
                }
                sl-button::part(base) {
                    border-radius: 20px !important;
                    border: none !important;
                    box-shadow: 8px 8px 16px #dbe4f0, -8px -8px 16px #ffffff !important;
                    color: white !important;
                    background: var(--sl-primary) !important;
                }
                sl-button::part(base):active {
                    box-shadow: inset 6px 6px 10px rgba(0,0,0,0.1), inset -6px -6px 10px rgba(255,255,255,0.8) !important;
                }
            """
        },
        'lg_innotek': {
            'mode': 'light',
            'primary': '#A50034',      # LG Red
            'secondary': '#6B6B6B',    # LG Gray
            'success': '#4b9b4b',
            'warning': '#ffb042',
            'danger': '#d91d3e',
            'bg': '#ffffff',
            'bg_card': '#f8f8f8',
            'border': '#e5e5e5',
            'text': '#1a1a1a',       # Black text
            'text_muted': '#767676',
            'radius': '4px',
            'input_border_radius_small': '2px',
            'input_border_radius_medium': '4px',
            'input_border_radius_large': '6px',
            'extra_css': """
                body { font-family: 'LG Smart', 'Segoe UI', sans-serif; }
                .card {
                    border-top: 3px solid #A50034 !important;
                    border-radius: 2px !important;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
                }
                sl-button::part(base) {
                    border-radius: 2px !important;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }
                h1, h2 { color: #1a1a1a; letter-spacing: -0.5px; }
                .gradient-text { 
                    background: linear-gradient(to right, #A50034, #D40045) !important; 
                    -webkit-background-clip: text !important;
                    -webkit-text-fill-color: transparent !important;
                }
            """
        },
        'light_2nd': {
            'mode': 'light',
            'primary': '#7C3AED', 
            'secondary': '#8B5CF6',
            'success': '#10B981',
            'warning': '#F59E0B',
            'danger': '#EF4444',
            'bg': '#FFFFFF',
            'bg_card': '#FFFFFF',
            'border': '#E4E4E7',
            'text': '#18181B',
            'text_muted': '#71717A',
            'radius': '6px',
            'input_border_radius_small': '4px',
            'input_border_radius_medium': '6px',
            'input_border_radius_large': '8px',
            'extra_css': """
                /* 
                   THEME: Modern Luxury (Restrained)
                   Concept: 'Silk & Glass' - Smooth, matte finishes with subtle light play.
                   No loud gradients, no flashing flashing animations.
                */

                body {
                    background-color: #FFFFFF;
                    /* Very subtle ambient light, barely visible */
                    background-image: radial-gradient(circle at 50% 0%, rgba(124, 58, 237, 0.03), transparent 40%);
                }
                
                /* Cards: Clean, bordered, soft shadow */
                .card {
                    background: #FFFFFF !important;
                    border: 1px solid #E4E4E7 !important;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
                    border-radius: 8px !important;
                    transition: box-shadow 0.2s ease, transform 0.2s ease;
                }
                .card:hover {
                    box-shadow: 0 8px 24px rgba(0,0,0,0.04) !important;
                    border-color: #D4D4D8 !important;
                }

                /* --- SOPHISTICATED BUTTONS --- */
                /* Matte finish, rich color, soft colored shadow */
                
                sl-button::part(base) {
                    background: #7C3AED !important; /* Solid Violet 600 */
                    border: 1px solid transparent !important; /* Clean edges */
                    
                    color: white !important;
                    font-weight: 500 !important; /* Medium weight is more premium than Bold */
                    letter-spacing: -0.01em;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                    
                    border-radius: 6px !important;
                    
                    /* The "Luxury" Touch: A soft, colored shadow glow */
                    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25) !important;
                    
                    transition: all 0.2s cubic-bezier(0.25, 1, 0.5, 1);
                }

                /* Hover: Subtle Deepening & Lift */
                sl-button::part(base):hover {
                    background: #6D28D9 !important; /* Violet 700 */
                    transform: translateY(-1px);
                    box-shadow: 0 6px 16px rgba(124, 58, 237, 0.35) !important;
                }

                /* Active: Precise Press */
                sl-button::part(base):active {
                    transform: translateY(0px) scale(0.98) !important;
                    background: #5B21B6 !important; /* Violet 800 */
                    box-shadow: 0 2px 4px rgba(124, 58, 237, 0.15) !important;
                }

                /* Remove all pseudo-element animations for cleaner look */
                sl-button::part(base)::before,
                sl-button::part(base)::after {
                    display: none !important;
                }

                /* Typography: High contrast, sharp */
                h1, h2, h3 {
                    color: #111827;
                    font-weight: 700;
                    letter-spacing: -0.02em;
                }
            """
        },
        'violit_light_jewel': {
            'mode': 'light',
            'primary': '#6D28D9',       # Royal Purple (Violet-700) — 로고의 가장 진한 보라
            'secondary': '#7C3AED',     # Violet-600
            'success': '#16A34A',       # Green-600
            'warning': '#EA580C',       # Orange-600
            'danger': '#DC2626',        # Red-600
            'bg': '#FFFFFF',            # 쨍한 흰색 (회색조 X)
            'bg_card': '#FFFFFF',       # 카드도 순백
            'border': '#E9E5F0',        # 보라끼 살짝 섞인 테두리
            'text': '#1C1127',          # 아주 짙은 보라-검정 텍스트
            'text_muted': '#6B5F7B',    # Muted 보라 회색
            'radius': '0.5rem',         # 과하지 않은 Radius
            'input_border_radius_small': '0.375rem',
            'input_border_radius_medium': '0.5rem',
            'input_border_radius_large': '0.625rem',
            'extra_css': """
                /*
                   THEME: Clean Crystal (violit_light_2nd)
                   Concept: Shadcn/Zinc 스타일 + Royal Purple 포인트
                   핵심: 1px 얇은 Border, Inter 폰트, 0.5rem Radius, 단색 버튼
                */

                /* --- @font-face: Inter (로컬 vendor) --- */
                @font-face {
                    font-family: 'Inter';
                    font-style: normal;
                    font-weight: 100 900;
                    font-display: swap;
                    src: url('/static/vendor/fonts/inter/inter-latin-ext.woff2') format('woff2');
                    unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF;
                }
                @font-face {
                    font-family: 'Inter';
                    font-style: normal;
                    font-weight: 100 900;
                    font-display: swap;
                    src: url('/static/vendor/fonts/inter/inter-latin.woff2') format('woff2');
                    unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
                }

                /* --- Global --- */
                body {
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
                    background-color: #FFFFFF;
                    color: #1C1127;
                    -webkit-font-smoothing: antialiased;
                    -moz-osx-font-smoothing: grayscale;
                    letter-spacing: -0.011em;
                    line-height: 1.6;
                }

                /* --- Cards: Material Elevation 1→3 on hover --- */
                .card {
                    background: #FFFFFF !important;
                    border: 1px solid #E9E5F0 !important;
                    border-radius: 0.5rem !important;
                    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04), 0 1px 2px -1px rgba(0, 0, 0, 0.04) !important;
                    transition: box-shadow 0.28s cubic-bezier(0.4, 0, 0.2, 1),
                                border-color 0.28s cubic-bezier(0.4, 0, 0.2, 1),
                                transform 0.28s cubic-bezier(0.4, 0, 0.2, 1);
                }
                .card:hover {
                    border-color: #DDD8E8 !important;
                    box-shadow: 0 3px 6px -1px rgba(0, 0, 0, 0.07),
                                0 6px 12px 0 rgba(0, 0, 0, 0.05),
                                0 2px 18px 0 rgba(0, 0, 0, 0.04) !important;
                    transform: translateY(-1px);
                }

                /* --- Buttons: Material Elevation + 단색 --- */
                sl-button::part(base) {
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
                    background: #6D28D9 !important;
                    border: 1px solid transparent !important;
                    color: #FFFFFF !important;
                    font-weight: 500 !important;
                    font-size: 0.875rem !important;
                    letter-spacing: -0.006em;
                    border-radius: 0.5rem !important;
                    box-shadow: 0 1px 3px rgba(109, 40, 217, 0.12), 0 1px 2px rgba(109, 40, 217, 0.08) !important;
                    transition: box-shadow 0.28s cubic-bezier(0.4, 0, 0.2, 1),
                                background-color 0.28s cubic-bezier(0.4, 0, 0.2, 1),
                                transform 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
                    caret-color: transparent !important;
                }
                /* Hover: Material Elevation 4 */
                sl-button::part(base):hover {
                    background: #6D28D9 !important;
                    box-shadow: 0 2px 4px -1px rgba(109, 40, 217, 0.2),
                                0 4px 5px 0 rgba(109, 40, 217, 0.14),
                                0 1px 10px 0 rgba(109, 40, 217, 0.12) !important;
                }
                /* Active: Material press */
                sl-button::part(base):active {
                    background: #5B21B6 !important;
                    box-shadow: 0 1px 2px rgba(109, 40, 217, 0.1) !important;
                    transform: scale(0.97);
                }

                /* --- Inputs: 깔끔한 1px 보더 --- */
                sl-input::part(base),
                sl-textarea::part(base),
                sl-select::part(combobox) {
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
                    background: #FFFFFF !important;
                    border: 1px solid #E9E5F0 !important;
                    border-radius: 0.5rem !important;
                    font-size: 0.875rem;
                    transition: border-color 0.15s ease, box-shadow 0.15s ease;
                }
                sl-input::part(base):focus-within,
                sl-textarea::part(base):focus-within,
                sl-select::part(combobox):focus-within {
                    border-color: #6D28D9 !important;
                    box-shadow: 0 0 0 3px rgba(109, 40, 217, 0.08) !important;
                    outline: none;
                }

                /* --- Typography: 짙은 보라-검정, Sharp --- */
                h1, h2, h3, h4, h5, h6 {
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
                    color: #1C1127;
                    font-weight: 600;
                    letter-spacing: -0.025em;
                    line-height: 1.3;
                }
                h1 { font-weight: 700; letter-spacing: -0.035em; }

                p, span, label, div {
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                }

                /* --- Links: Primary Purple --- */
                a {
                    color: #6D28D9;
                    text-decoration: none;
                    transition: color 0.15s ease;
                }
                a:hover {
                    color: #5B21B6;
                    text-decoration: underline;
                }

                /* --- Sidebar: 깨끗한 구분선 --- */
                #sidebar {
                    background: #FAFAFA !important;
                    border-right: 1px solid #E9E5F0 !important;
                }

                /* --- Sidebar Navigation: Subtle, Clean Style --- */
                /* Default state: transparent background, dark text */
                #sidebar sl-button::part(base) {
                    background: transparent !important;
                    color: #6B5F7B !important;
                    border: none !important;
                    box-shadow: none !important;
                    font-weight: 500 !important;
                }
                
                /* Hover: subtle purple tint */
                #sidebar sl-button::part(base):hover {
                    background: rgba(109, 40, 217, 0.06) !important;
                    color: #6D28D9 !important;
                    box-shadow: none !important;
                }
                
                /* Active (selected page): purple background + white text */
                #sidebar sl-button[variant="primary"]::part(base) {
                    background: #6D28D9 !important;
                    color: #FFFFFF !important;
                    box-shadow: 0 1px 3px rgba(109, 40, 217, 0.12), 0 1px 2px rgba(109, 40, 217, 0.08) !important;
                }
                
                #sidebar sl-button[variant="primary"]::part(base):hover {
                    background: #6D28D9 !important;
                    box-shadow: 0 2px 4px -1px rgba(109, 40, 217, 0.2),
                                0 4px 5px 0 rgba(109, 40, 217, 0.14),
                                0 1px 10px 0 rgba(109, 40, 217, 0.12) !important;
                }
                
                #sidebar sl-button[variant="primary"]::part(base):active {
                    background: #5B21B6 !important;
                    box-shadow: 0 1px 2px rgba(109, 40, 217, 0.1) !important;
                    transform: scale(0.97);
                }

                /* --- Table / Data: 미니멀 라인 --- */
                table {
                    border-collapse: collapse;
                }
                th, td {
                    border-bottom: 1px solid #E9E5F0;
                    padding: 0.625rem 0.75rem;
                    font-size: 0.875rem;
                }
                th {
                    font-weight: 600;
                    color: #1C1127;
                    text-align: left;
                }

                /* --- Badges / Tags: 미니멀 --- */
                sl-tag::part(base) {
                    border-radius: 0.375rem !important;
                    border: 1px solid #E9E5F0 !important;
                    font-size: 0.75rem;
                    font-weight: 500;
                }

                /* --- Scrollbar: 은은한 보라 --- */
                ::-webkit-scrollbar { width: 6px; height: 6px; }
                ::-webkit-scrollbar-track { background: transparent; }
                ::-webkit-scrollbar-thumb { background: #D4CFE0; border-radius: 3px; }
                ::-webkit-scrollbar-thumb:hover { background: #B0A6C4; }

                /* --- Selection: 보라 하이라이트 --- */
                ::selection {
                    background: rgba(109, 40, 217, 0.12);
                    color: #1C1127;
                }

                /* --- Material: Focus ring --- */
                sl-button:focus-visible::part(base) {
                    outline: 2px solid #6D28D9 !important;
                    outline-offset: 2px;
                }

                /* --- Material: Ripple overlay (global, survives DOM swaps) --- */
                #vl-ripple-overlay {
                    position: fixed;
                    inset: 0;
                    pointer-events: none;
                    z-index: 10000;
                }
                .vl-ripple-box {
                    position: fixed;
                    overflow: hidden;
                    pointer-events: none;
                    transition: background 0.2s cubic-bezier(0.4, 0, 0.2, 1);
                }
                .vl-rpl {
                    position: absolute;
                    border-radius: 50%;
                    pointer-events: none;
                    background: rgba(255, 255, 255, 0.14);
                    transform: scale(0);
                    opacity: 1;
                    transition: transform 0.65s cubic-bezier(0.2, 0, 0, 1),
                                opacity 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                }
                .vl-rpl.vl-fade {
                    opacity: 0;
                }
            """,
            'extra_js': """
(function() {
    var ac = new AbortController();
    var sig = ac.signal;
    var curBtn = null;
    var activeRipple = null;
    var activeBox = null;

    /* --- Global ripple overlay (lives in body, never destroyed by HTMX swaps) --- */
    var overlay = document.getElementById('vl-ripple-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'vl-ripple-overlay';
        document.body.appendChild(overlay);
    }

    function getBase(btn) {
        if (!btn || !btn.shadowRoot) return null;
        var base = btn.shadowRoot.querySelector('[part="base"]');
        if (!base) return null;
        base.style.position = 'relative';
        base.style.overflow = 'hidden';
        return base;
    }

    /* ============================================
       Mouse-following Glow (stays in Shadow DOM)
       ============================================ */
    document.addEventListener('mousemove', function(e) {
        var btn = e.target.closest('sl-button');
        if (curBtn && curBtn !== btn) {
            var pb = curBtn.shadowRoot && curBtn.shadowRoot.querySelector('[part="base"]');
            if (pb) { var g = pb.querySelector('.vl-glow'); if (g) g.style.opacity = '0'; }
            curBtn = null;
        }
        if (!btn) return;
        curBtn = btn;
        var base = getBase(btn);
        if (!base) return;
        var rect = base.getBoundingClientRect();
        var x = e.clientX - rect.left;
        var y = e.clientY - rect.top;
        var glow = base.querySelector('.vl-glow');
        if (!glow) {
            glow = document.createElement('span');
            glow.className = 'vl-glow';
            glow.style.cssText = 'position:absolute;inset:0;pointer-events:none;z-index:1;border-radius:inherit;transition:opacity 0.25s cubic-bezier(0.4,0,0.2,1);';
            base.appendChild(glow);
        }
        glow.style.background = 'radial-gradient(circle 120px at ' + x + 'px ' + y + 'px, rgba(255,255,255,0.2), transparent 70%)';
        glow.style.opacity = '1';
    }, {signal: sig});

    document.addEventListener('mouseleave', function() {
        if (curBtn) {
            var pb = curBtn.shadowRoot && curBtn.shadowRoot.querySelector('[part="base"]');
            if (pb) { var g = pb.querySelector('.vl-glow'); if (g) g.style.opacity = '0'; }
            curBtn = null;
        }
    }, {signal: sig});

    /* ============================================
       Material Ripple - Global Overlay Approach
       Ripple lives in a fixed-position overlay on
       document.body, completely outside any HTMX-
       swapped content. Even if the button DOM is
       replaced mid-animation, the ripple continues
       its full expand + fade cycle undisturbed.
       ============================================ */

    /* Phase 1 (pointerdown): Expand from click point */
    document.addEventListener('pointerdown', function(e) {
        var btn = e.target.closest('sl-button');
        if (!btn) return;
        var base = btn.shadowRoot && btn.shadowRoot.querySelector('[part="base"]');
        if (!base) return;

        /* Clear previous ripple if still running */
        if (activeBox && activeBox.parentNode) activeBox.remove();
        activeRipple = null;
        activeBox = null;

        var rect = base.getBoundingClientRect();
        var x = e.clientX - rect.left;
        var y = e.clientY - rect.top;

        /* Pythagorean distance to farthest corner */
        var dx = Math.max(x, rect.width - x);
        var dy = Math.max(y, rect.height - y);
        var radius = Math.sqrt(dx * dx + dy * dy) + 8;
        var dia = radius * 2;

        /* Container: fixed overlay matching button viewport position exactly */
        var box = document.createElement('div');
        box.className = 'vl-ripple-box';
        box.style.cssText = 'left:' + rect.left + 'px;top:' + rect.top + 'px;'
            + 'width:' + rect.width + 'px;height:' + rect.height + 'px;'
            + 'border-radius:' + (getComputedStyle(base).borderRadius || '0.5rem') + ';';

        /* Ripple circle */
        var r = document.createElement('span');
        r.className = 'vl-rpl';
        r.style.left = (x - radius) + 'px';
        r.style.top = (y - radius) + 'px';
        r.style.width = dia + 'px';
        r.style.height = dia + 'px';

        box.appendChild(r);
        overlay.appendChild(box);
        activeRipple = r;
        activeBox = box;

        /* Trigger expansion + press tint on next frame */
        requestAnimationFrame(function() {
            r.style.transform = 'scale(1)';
            /* Material state overlay tint (persists across DOM swaps) */
            box.style.background = 'rgba(0,0,0,0.08)';
        });
    }, {signal: sig});

    /* Phase 2 (pointerup): Release tint + fade ripple */
    function fadeRipple() {
        if (!activeRipple) return;
        var r = activeRipple;
        var box = activeBox;
        activeRipple = null;
        activeBox = null;
        /* Release tint */
        box.style.background = 'transparent';
        /* Fade ripple */
        r.classList.add('vl-fade');
        setTimeout(function() { if (box && box.parentNode) box.remove(); }, 600);
    }
    document.addEventListener('pointerup', fadeRipple, {signal: sig});
    document.addEventListener('pointercancel', fadeRipple, {signal: sig});

    /* ============================================
       Cleanup for theme switching
       ============================================ */
    window._vlThemeCleanup = function() {
        ac.abort();
        activeRipple = null;
        activeBox = null;
        curBtn = null;
        var ol = document.getElementById('vl-ripple-overlay');
        if (ol) ol.remove();
        document.querySelectorAll('sl-button').forEach(function(btn) {
            if (!btn.shadowRoot) return;
            var base = btn.shadowRoot.querySelector('[part="base"]');
            if (base) {
                var g = base.querySelector('.vl-glow');
                if (g) g.remove();
            }
        });
    };
})();
            """
        },
        'violit_dark': {
            'mode': 'dark',
            'primary': '#8B5CF6',
            'secondary': '#6D28D9',
            'success': '#34D399',
            'warning': '#FBBF24',
            'danger': '#F87171',
            'bg': '#1e1b4b',          # Ultra Deep Indigo
            'bg_card': '#312e81',     # Deep Indigo
            'border': '#4c1d95',      # Violet 900
            'text': '#ede9fe',        # Violet 50
            'text_muted': '#a78bfa',
            'radius': '3px',
            'input_border_radius_small': '2px',
            'input_border_radius_medium': '3px',
            'input_border_radius_large': '4px',
            'extra_css': """
                body {
                    background: radial-gradient(circle at 50% -20%, #4c1d95 0%, #1e1b4b 50%, #0f0a20 100%);
                }
                
                .card {
                    background: rgba(49, 46, 129, 0.4) !important;
                    backdrop-filter: blur(12px) !important;
                    border: 1px solid rgba(139, 92, 246, 0.3) !important;
                    box-shadow: 
                        0 0 20px rgba(139, 92, 246, 0.05),
                        inset 0 0 0 1px rgba(255, 255, 255, 0.05) !important;
                }

                /* Neon Facet Buttons */
                sl-button::part(base) {
                    background: transparent !important;
                    border: 1px solid #8B5CF6 !important;
                    color: #8B5CF6 !important;
                    border-radius: 2px !important;
                    box-shadow: 0 0 5px rgba(139, 92, 246, 0.2) !important;
                    transition: all 0.2s ease !important;
                    text-transform: uppercase;
                    font-weight: 700;
                    letter-spacing: 1px;
                }

                /* Hover: Fill with Light */
                sl-button::part(base):hover {
                    background: #8B5CF6 !important;
                    color: white !important;
                    box-shadow: 0 0 20px #8B5CF6, 0 0 40px rgba(139, 92, 246, 0.4) !important;
                    text-shadow: 0 1px 2px rgba(0,0,0,0.2);
                    transform: scale(1.02) !important;
                    border-color: transparent !important;
                }

                /* Active */
                sl-button::part(base):active {
                    transform: scale(0.95) !important;
                    box-shadow: 0 0 10px #8B5CF6 !important;
                }

                h1, h2, h3 {
                   color: #ede9fe;
                   text-shadow: 0 0 10px rgba(139, 92, 246, 0.5);
                }
                
                /* Inputs */
                sl-input::part(base) {
                    background: rgba(0,0,0,0.3) !important;
                    border: 1px solid #4c1d95 !important;
                }
                sl-input::part(base):focus-within {
                    border-color: #8B5CF6 !important;
                    box-shadow: 0 0 10px rgba(139, 92, 246, 0.2) !important;
                }
            """
        }
    }
    
    def __init__(self, preset: str = 'dark'):
        self.preset_name = preset
        self.current = self.PRESETS.get(preset, self.PRESETS['dark']).copy()
    
    def set_preset(self, preset: str):
        if preset in self.PRESETS:
            self.preset_name = preset
            self.current = self.PRESETS[preset].copy()
    
    def set_color(self, key: str, value: str):
        if key in self.current:
            self.current[key] = value
    
    def to_css_vars(self) -> str:
        """Convert to CSS variables"""
        return "\n".join([
            f"--sl-{k.replace('_', '-')}: {v};" 
            for k, v in self.current.items() if k not in ['mode', 'extra_css', 'extra_js']
        ])
    
    @property
    def mode(self) -> str:
        return self.current.get('mode', 'light')
        
    @property
    def extra_css(self) -> str:
        return self.current.get('extra_css', '')
    
    @property
    def extra_js(self) -> str:
        return self.current.get('extra_js', '')
    
    @property
    def theme_class(self) -> str:
        return f"sl-theme-{self.mode}"
