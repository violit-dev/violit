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
            for k, v in self.current.items() if k not in ['mode', 'extra_css']
        ])
    
    @property
    def mode(self) -> str:
        return self.current.get('mode', 'light')
        
    @property
    def extra_css(self) -> str:
        return self.current.get('extra_css', '')
    
    @property
    def theme_class(self) -> str:
        return f"sl-theme-{self.mode}"
