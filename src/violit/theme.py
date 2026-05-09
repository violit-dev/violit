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
                wa-button::part(base) { border: 3px solid black !important; box-shadow: 4px 4px 0px 0px black !important; transition: transform 0.1s !important; }
                wa-button::part(base):active { transform: translate(2px, 2px) !important; box-shadow: 2px 2px 0px 0px black !important; }
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
                wa-button::part(base) {
                    border: none !important;
                    background: #e0e5ec !important;
                    color: #4a5568 !important;
                    box-shadow: 6px 6px 10px 0 rgba(163,177,198, 0.7), -6px -6px 10px 0 rgba(255,255,255, 0.8) !important;
                    transition: all 0.2s ease;
                }
                wa-button::part(base):active {
                    box-shadow: inset 6px 6px 10px 0 rgba(163,177,198, 0.7), inset -6px -6px 10px 0 rgba(255,255,255, 0.8) !important;
                }
                wa-input::part(base) {
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
                wa-button::part(base) {
                    border: 1px solid #0ff !important;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                    clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
                }
                wa-button::part(base):hover {
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
                wa-button::part(base) {
                    border: 2px solid #2c3e50 !important;
                    border-radius: 255px 15px 225px 15px / 15px 225px 15px 255px !important;
                }
                wa-input::part(base) {
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
                wa-button::part(base) {
                    border: 1px solid #00ff00 !important;
                    background: black !important;
                    color: #00ff00 !important;
                }
                wa-button::part(base):hover {
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
                .card, wa-button::part(base) {
                    background: #c0c0c0 !important;
                    border-top: 2px solid #ffffff !important;
                    border-left: 2px solid #ffffff !important;
                    border-right: 2px solid #000000 !important;
                    border-bottom: 2px solid #000000 !important;
                    box-shadow: 1px 1px 0px 0px #000 inset, -1px -1px 0px 0px #fff inset !important;
                }
                wa-button::part(base):active {
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
                wa-button::part(base) {
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
                wa-button::part(base) {
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
                wa-button::part(base) {
                    background: transparent !important;
                    border: 2px solid white !important;
                    color: white !important;
                }
                wa-button::part(base):hover {
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
                wa-button::part(base) {
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
                wa-button::part(base) {
                    font-family: 'Times New Roman', serif;
                    text-transform: uppercase;
                    background: transparent !important;
                    color: black !important;
                    border: 1px solid black !important;
                    font-weight: bold;
                }
                wa-button::part(base):hover {
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
                wa-button::part(base) {
                    border-radius: 20px !important;
                    border: none !important;
                    box-shadow: 8px 8px 16px #dbe4f0, -8px -8px 16px #ffffff !important;
                    color: white !important;
                    background: var(--vl-primary) !important;
                }
                wa-button::part(base):active {
                    box-shadow: inset 6px 6px 10px rgba(0,0,0,0.1), inset -6px -6px 10px rgba(255,255,255,0.8) !important;
                }
            """
        },
        'inno': {
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
                wa-button::part(base) {
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
                
                wa-button::part(base) {
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
                wa-button::part(base):hover {
                    background: #6D28D9 !important; /* Violet 700 */
                    transform: translateY(-1px);
                    box-shadow: 0 6px 16px rgba(124, 58, 237, 0.35) !important;
                }

                /* Active: Precise Press */
                wa-button::part(base):active {
                    transform: translateY(0px) scale(0.98) !important;
                    background: #5B21B6 !important; /* Violet 800 */
                    box-shadow: 0 2px 4px rgba(124, 58, 237, 0.15) !important;
                }

                /* Remove all pseudo-element animations for cleaner look */
                wa-button::part(base)::before,
                wa-button::part(base)::after {
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
            'primary': '#6D28D9',       # Royal purple anchor color
            'secondary': '#8B5CF6',     # Brighter jewel violet
            'success': '#0F9F6E',       # Emerald jewel accent
            'warning': '#C98512',       # Amber topaz accent
            'danger': '#C24164',        # Ruby accent
            'bg': '#FFFFFF',            # Bright white background
            'bg_card': '#FFFFFF',       # White card surface
            'border': '#E9E5F0',        # Soft purple-tinted border
            'text': '#1C1127',          # Deep purple-black text
            'text_muted': '#6B5F7B',    # Muted purple text
            'radius': '0.5rem',         # Balanced corner radius
            'input_border_radius_small': '0.375rem',
            'input_border_radius_medium': '0.5rem',
            'input_border_radius_large': '0.625rem',
            'extra_css': """
                /*
                   THEME: Clean Crystal (violit_light_2nd)
                   Concept: Shadcn/Zinc baseline with a royal purple accent
                   Key points: 1px border, Inter font, 0.5rem radius, white surfaces
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

                /* --- Cards: elevation level 1 on hover --- */
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

                /* --- Buttons: material elevation with white text --- */
                wa-button::part(base) {
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
                wa-button::part(base):hover {
                    background: #6D28D9 !important;
                    box-shadow: 0 2px 4px -1px rgba(109, 40, 217, 0.2),
                                0 4px 5px 0 rgba(109, 40, 217, 0.14),
                                0 1px 10px 0 rgba(109, 40, 217, 0.12) !important;
                }
                /* Active: Material press */
                wa-button::part(base):active {
                    background: #5B21B6 !important;
                    box-shadow: 0 1px 2px rgba(109, 40, 217, 0.1) !important;
                    transform: scale(0.97);
                }

                /* --- Semantic button variants: distinct but still jewel-toned --- */
                wa-button[variant='neutral'][appearance='outlined']::part(base) {
                    background: #F6F2FB !important;
                    border-color: #DDD3EE !important;
                    color: #4C3F63 !important;
                    box-shadow: 0 1px 2px rgba(76, 63, 99, 0.05), 0 0 0 1px rgba(221, 211, 238, 0.38) inset !important;
                }
                wa-button[variant='neutral'][appearance='outlined']::part(base):hover {
                    background: #EFE8F9 !important;
                    border-color: #D1C4E6 !important;
                    box-shadow: 0 2px 5px rgba(109, 40, 217, 0.08), 0 0 0 1px rgba(209, 196, 230, 0.5) inset !important;
                }
                wa-button[variant='neutral'][appearance='outlined']::part(base):active {
                    background: #E7DFF5 !important;
                    border-color: #C7B8E2 !important;
                    transform: scale(0.97);
                }

                wa-button[variant='neutral'][appearance='plain']::part(base) {
                    background: transparent !important;
                    border-color: transparent !important;
                    color: #6B5F7B !important;
                    box-shadow: none !important;
                }
                wa-button[variant='neutral'][appearance='plain']::part(base):hover {
                    background: rgba(109, 40, 217, 0.06) !important;
                    color: #6D28D9 !important;
                    box-shadow: none !important;
                }
                wa-button[variant='neutral'][appearance='plain']::part(base):active {
                    background: rgba(109, 40, 217, 0.1) !important;
                    color: #5B21B6 !important;
                    transform: scale(0.98);
                }

                wa-button[variant='success']::part(base) {
                    background: #E9F8F1 !important;
                    border-color: #B9E6D3 !important;
                    color: #0D7A56 !important;
                    box-shadow: 0 1px 2px rgba(15, 159, 110, 0.08), 0 0 0 1px rgba(15, 159, 110, 0.16) inset !important;
                }
                wa-button[variant='success']::part(base):hover {
                    background: #DBF2E7 !important;
                    border-color: #9EDCBF !important;
                    box-shadow: 0 3px 8px rgba(15, 159, 110, 0.14), 0 0 0 1px rgba(15, 159, 110, 0.18) inset !important;
                }
                wa-button[variant='success']::part(base):active {
                    background: #CEEAD9 !important;
                    border-color: #8FD3B1 !important;
                    transform: scale(0.97);
                }

                wa-button[variant='warning']::part(base) {
                    background: #FFF4E5 !important;
                    border-color: #F2D19B !important;
                    color: #A66208 !important;
                    box-shadow: 0 1px 2px rgba(201, 133, 18, 0.08), 0 0 0 1px rgba(201, 133, 18, 0.16) inset !important;
                }
                wa-button[variant='warning']::part(base):hover {
                    background: #FDEBCC !important;
                    border-color: #EABF73 !important;
                    box-shadow: 0 3px 8px rgba(201, 133, 18, 0.14), 0 0 0 1px rgba(201, 133, 18, 0.18) inset !important;
                }
                wa-button[variant='warning']::part(base):active {
                    background: #F8DFB2 !important;
                    border-color: #E0B05E !important;
                    transform: scale(0.97);
                }

                wa-button[variant='danger']::part(base) {
                    background: #FDECEF !important;
                    border-color: #F0B8C8 !important;
                    color: #A63A54 !important;
                    box-shadow: 0 1px 2px rgba(194, 65, 100, 0.08), 0 0 0 1px rgba(194, 65, 100, 0.16) inset !important;
                }
                wa-button[variant='danger']::part(base):hover {
                    background: #F9DDE5 !important;
                    border-color: #E79BB4 !important;
                    box-shadow: 0 3px 8px rgba(194, 65, 100, 0.14), 0 0 0 1px rgba(194, 65, 100, 0.18) inset !important;
                }
                wa-button[variant='danger']::part(base):active {
                    background: #F3CFDA !important;
                    border-color: #DB88A4 !important;
                    transform: scale(0.97);
                }

                /* --- Inputs: clean 1px border --- */
                wa-input::part(base),
                wa-textarea::part(base),
                wa-select::part(combobox) {
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
                    background: #FFFFFF !important;
                    border: 1px solid #E9E5F0 !important;
                    border-radius: 0.5rem !important;
                    font-size: 0.875rem;
                    transition: border-color 0.15s ease, box-shadow 0.15s ease;
                }
                wa-input::part(base):focus-within,
                wa-textarea::part(base):focus-within,
                wa-select::part(combobox):focus-within {
                    border-color: #6D28D9 !important;
                    box-shadow: 0 0 0 3px rgba(109, 40, 217, 0.08) !important;
                    outline: none;
                }
                wa-textarea::part(form-control-input) {
                    min-height: 6.25rem !important;
                }
                wa-textarea::part(textarea) {
                    min-height: 6.25rem !important;
                    line-height: 1.5 !important;
                    box-sizing: border-box !important;
                }

                /* --- Typography: sharp deep purple-black tone --- */
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

                /* --- Sidebar: clean separation --- */
                #sidebar {
                    background: #FAFAFA !important;
                    border-right: 1px solid #E9E5F0 !important;
                }

                /* --- Sidebar Navigation: Subtle, Clean Style --- */
                /* Default state: transparent background, dark text */
                #sidebar wa-button::part(base) {
                    background: transparent !important;
                    color: #6B5F7B !important;
                    border: none !important;
                    box-shadow: none !important;
                    font-weight: 500 !important;
                }
                
                /* Hover: subtle purple tint */
                #sidebar wa-button::part(base):hover {
                    background: rgba(109, 40, 217, 0.06) !important;
                    color: #6D28D9 !important;
                    box-shadow: none !important;
                }
                
                /* Active state follows the explicit nav selection marker, not a button variant. */
                #sidebar wa-button[data-nav-active="true"]::part(base) {
                    background: #6D28D9 !important;
                    color: #FFFFFF !important;
                    box-shadow: 0 1px 3px rgba(109, 40, 217, 0.12), 0 1px 2px rgba(109, 40, 217, 0.08) !important;
                }
                
                #sidebar wa-button[data-nav-active="true"]::part(base):hover {
                    background: #6D28D9 !important;
                    box-shadow: 0 2px 4px -1px rgba(109, 40, 217, 0.2),
                                0 4px 5px 0 rgba(109, 40, 217, 0.14),
                                0 1px 10px 0 rgba(109, 40, 217, 0.12) !important;
                }
                
                #sidebar wa-button[data-nav-active="true"]::part(base):active {
                    background: #5B21B6 !important;
                    box-shadow: 0 1px 2px rgba(109, 40, 217, 0.1) !important;
                    transform: scale(0.97);
                }

                /* --- Table / Data: minimal accent --- */
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
                wa-tag::part(base) {
                    border-radius: 0.375rem !important;
                    border: 1px solid #E9E5F0 !important;
                    font-size: 0.75rem;
                    font-weight: 500;
                }

                /* --- Scrollbar: subtle purple --- */
                ::-webkit-scrollbar { width: 6px; height: 6px; }
                ::-webkit-scrollbar-track { background: transparent; }
                ::-webkit-scrollbar-thumb { background: #D4CFE0; border-radius: 3px; }
                ::-webkit-scrollbar-thumb:hover { background: #B0A6C4; }

                /* --- Selection: light purple highlight --- */
                ::selection {
                    background: rgba(109, 40, 217, 0.12);
                    color: #1C1127;
                }

                /* --- Material: Focus ring --- */
                wa-button:focus-visible::part(base) {
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
        var btn = e.target.closest('wa-button');
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
        var btn = e.target.closest('wa-button');
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
        document.querySelectorAll('wa-button').forEach(function(btn) {
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
        'violit_edge_refined': {
            'mode': 'light',
            'primary': '#171717',
            'secondary': '#0a72ef',
            'success': '#0070f3',
            'warning': '#de1d8d',
            'danger': '#ff5b4f',
            'bg': '#ffffff',
            'bg_card': '#ffffff',
            'border': '#ebebeb',
            'text': '#171717',
            'text_muted': '#4d4d4d',
            'radius': '8px',
            'input_border_radius_small': '6px',
            'input_border_radius_medium': '8px',
            'input_border_radius_large': '12px',
            'extra_css': """
                body {
                    font-family: Inter, Arial, sans-serif !important;
                    font-feature-settings: 'liga' 1;
                    letter-spacing: -0.01em;
                    background:
                        radial-gradient(circle at 50% 0%, rgba(10, 114, 239, 0.08), transparent 34%),
                        #ffffff;
                }
                h1, h2, h3, h4, h5, h6 {
                    letter-spacing: -0.04em;
                    color: #171717;
                }
                .card {
                    background: #ffffff !important;
                    border: none !important;
                    border-radius: 12px !important;
                    box-shadow: rgba(0, 0, 0, 0.08) 0 0 0 1px, rgba(0, 0, 0, 0.04) 0 2px 2px, #fafafa 0 0 0 1px inset !important;
                }
                wa-button::part(base) {
                    border-radius: 6px !important;
                    border: none !important;
                    font-weight: 500 !important;
                    box-shadow: rgba(0, 0, 0, 0.08) 0 0 0 1px !important;
                }
                wa-button[variant='neutral']::part(base) {
                    background: #ffffff !important;
                    color: #171717 !important;
                }
                wa-input::part(base), wa-textarea::part(base), wa-select::part(combobox) {
                    border: none !important;
                    border-radius: 8px !important;
                    box-shadow: rgba(0, 0, 0, 0.08) 0 0 0 1px !important;
                }
            """
        },
        'violit_midnight_grid': {
            'mode': 'dark',
            'primary': '#5e6ad2',
            'secondary': '#828fff',
            'success': '#27a644',
            'warning': '#5e6ad2',
            'danger': '#5e69d1',
            'bg': '#010102',
            'bg_card': '#0f1011',
            'border': '#23252a',
            'text': '#f7f8f8',
            'text_muted': '#8a8f98',
            'radius': '12px',
            'input_border_radius_small': '8px',
            'input_border_radius_medium': '8px',
            'input_border_radius_large': '12px',
            'extra_css': """
                body {
                    font-family: Inter, 'SF Pro Display', system-ui, sans-serif !important;
                    background: #010102 !important;
                    color: #f7f8f8;
                    letter-spacing: -0.01em;
                }
                h1, h2, h3, h4, h5, h6 {
                    color: #f7f8f8;
                    letter-spacing: -0.04em;
                }
                .card {
                    background: #0f1011 !important;
                    border: 1px solid #23252a !important;
                    border-radius: 16px !important;
                    box-shadow: none !important;
                }
                wa-button::part(base) {
                    border-radius: 8px !important;
                    border: 1px solid #23252a !important;
                }
                wa-button[variant='neutral']::part(base) {
                    background: #0f1011 !important;
                    color: #f7f8f8 !important;
                }
                wa-input::part(base), wa-textarea::part(base), wa-select::part(combobox) {
                    background: #0f1011 !important;
                    border: 1px solid #2e3138 !important;
                    border-radius: 8px !important;
                }
                wa-input::part(base):focus-within, wa-textarea::part(base):focus-within, wa-select::part(combobox):focus-within {
                    box-shadow: 0 0 0 2px rgba(94, 106, 210, 0.35) !important;
                }
            """
        },
        'violit_mesh_light': {
            'mode': 'light',
            'primary': '#533afd',
            'secondary': '#0d253d',
            'success': '#665efd',
            'warning': '#f5e9d4',
            'danger': '#ea2261',
            'bg': '#ffffff',
            'bg_card': '#ffffff',
            'border': '#e3e8ee',
            'text': '#0d253d',
            'text_muted': '#64748d',
            'radius': '12px',
            'input_border_radius_small': '6px',
            'input_border_radius_medium': '6px',
            'input_border_radius_large': '12px',
            'extra_css': """
                body {
                    font-family: Inter, 'SF Pro Display', system-ui, sans-serif !important;
                    font-weight: 300;
                    font-feature-settings: 'ss01' 1;
                    color: #0d253d;
                    background:
                        radial-gradient(circle at 8% 0%, rgba(249, 107, 238, 0.22), transparent 26%),
                        radial-gradient(circle at 26% 4%, rgba(83, 58, 253, 0.18), transparent 22%),
                        radial-gradient(circle at 42% 0%, rgba(234, 34, 97, 0.16), transparent 18%),
                        radial-gradient(circle at 64% 0%, rgba(245, 233, 212, 0.90), transparent 20%),
                        linear-gradient(180deg, #ffffff 0%, #f6f9fc 28%, #ffffff 52%);
                }
                h1, h2, h3, h4, h5, h6 {
                    color: #0d253d;
                    font-weight: 300;
                    letter-spacing: -0.04em;
                }
                .card {
                    background: rgba(255, 255, 255, 0.94) !important;
                    border: 1px solid #e3e8ee !important;
                    border-radius: 12px !important;
                    box-shadow: rgba(0, 55, 112, 0.08) 0 8px 24px, rgba(0, 55, 112, 0.04) 0 2px 6px !important;
                }
                wa-button::part(base) {
                    border-radius: 9999px !important;
                    font-weight: 400 !important;
                    padding-inline: 16px !important;
                }
                wa-button[variant='neutral']::part(base) {
                    background: #ffffff !important;
                    color: #533afd !important;
                    border: 1px solid #533afd !important;
                }
                code, pre { font-feature-settings: 'tnum' 1; }
            """
        },
        'violit_warm_canvas': {
            'mode': 'light',
            'primary': '#cc785c',
            'secondary': '#181715',
            'success': '#5db872',
            'warning': '#e8a55a',
            'danger': '#c64545',
            'bg': '#faf9f5',
            'bg_card': '#efe9de',
            'border': '#e6dfd8',
            'text': '#141413',
            'text_muted': '#6c6a64',
            'radius': '12px',
            'input_border_radius_small': '8px',
            'input_border_radius_medium': '8px',
            'input_border_radius_large': '12px',
            'extra_css': """
                body {
                    font-family: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
                    background: #faf9f5 !important;
                    color: #141413;
                }
                h1, h2, h3, h4, h5, h6 {
                    font-family: 'Cormorant Garamond', Georgia, serif !important;
                    font-weight: 500;
                    color: #141413;
                    letter-spacing: -0.03em;
                }
                .card {
                    background: #efe9de !important;
                    border: 1px solid #e6dfd8 !important;
                    border-radius: 12px !important;
                    box-shadow: none !important;
                }
                wa-button::part(base) {
                    border-radius: 8px !important;
                    font-weight: 500 !important;
                }
                wa-button[variant='neutral']::part(base) {
                    background: #faf9f5 !important;
                    color: #141413 !important;
                    border: 1px solid #e6dfd8 !important;
                }
                wa-input::part(base), wa-textarea::part(base), wa-select::part(combobox) {
                    background: #faf9f5 !important;
                    border: 1px solid #e6dfd8 !important;
                    border-radius: 8px !important;
                }
                pre, code {
                    font-family: 'JetBrains Mono', 'SFMono-Regular', Consolas, monospace !important;
                }
            """
        },
        'violit_editorial_dark': {
            'mode': 'light',
            'primary': '#f54e00',
            'secondary': '#26251e',
            'success': '#1f8a65',
            'warning': '#c08532',
            'danger': '#cf2d56',
            'bg': '#f7f7f4',
            'bg_card': '#ffffff',
            'border': '#e6e5e0',
            'text': '#26251e',
            'text_muted': '#5a5852',
            'radius': '12px',
            'input_border_radius_small': '8px',
            'input_border_radius_medium': '8px',
            'input_border_radius_large': '12px',
            'extra_css': """
                body {
                    font-family: Inter, 'Helvetica Neue', Arial, sans-serif !important;
                    background: #f7f7f4 !important;
                    color: #26251e;
                }
                h1, h2, h3, h4, h5, h6 {
                    font-weight: 400 !important;
                    color: #26251e;
                    letter-spacing: -0.03em;
                }
                .card {
                    background: #ffffff !important;
                    border: 1px solid #e6e5e0 !important;
                    border-radius: 12px !important;
                    box-shadow: none !important;
                }
                wa-button::part(base) {
                    border-radius: 8px !important;
                    font-weight: 500 !important;
                }
                wa-button[variant='neutral']::part(base) {
                    background: #ffffff !important;
                    color: #26251e !important;
                    border: 1px solid #cfcdc4 !important;
                }
                wa-input::part(base), wa-textarea::part(base), wa-select::part(combobox) {
                    background: #ffffff !important;
                    border: 1px solid #cfcdc4 !important;
                    border-radius: 8px !important;
                }
                code, pre {
                    font-family: 'JetBrains Mono', Consolas, monospace !important;
                }
            """
        },
        'violit_docs_fresh': {
            'mode': 'light',
            'primary': '#0a0a0a',
            'secondary': '#00d4a4',
            'success': '#00d4a4',
            'warning': '#fb7a59',
            'danger': '#e5484d',
            'bg': '#ffffff',
            'bg_card': '#ffffff',
            'border': '#e5e7eb',
            'text': '#111827',
            'text_muted': '#667085',
            'radius': '12px',
            'input_border_radius_small': '8px',
            'input_border_radius_medium': '8px',
            'input_border_radius_large': '12px',
            'extra_css': """
                body {
                    font-family: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
                    background:
                        linear-gradient(180deg, rgba(197, 237, 255, 0.55) 0%, rgba(255, 250, 240, 0.72) 18%, #ffffff 36%);
                    color: #111827;
                }
                h1, h2, h3, h4, h5, h6 {
                    color: #111827;
                    letter-spacing: -0.03em;
                }
                .card {
                    background: #ffffff !important;
                    border: 1px solid #e5e7eb !important;
                    border-radius: 12px !important;
                    box-shadow: rgba(0, 0, 0, 0.04) 0 4px 12px !important;
                }
                wa-button::part(base) {
                    border-radius: 9999px !important;
                    font-weight: 500 !important;
                }
                wa-button[variant='success']::part(base) {
                    background: #00d4a4 !important;
                    color: #0a0a0a !important;
                }
                wa-button[variant='neutral']::part(base) {
                    background: #ffffff !important;
                    color: #111827 !important;
                    border: 1px solid #e5e7eb !important;
                }
                code, pre, .vl-mono {
                    font-family: 'JetBrains Mono', 'SFMono-Regular', Menlo, monospace !important;
                }
            """
        },
        'violit_command_panel': {
            'mode': 'dark',
            'primary': '#ffffff',
            'secondary': '#57c1ff',
            'success': '#59d499',
            'warning': '#ffc533',
            'danger': '#ff6161',
            'bg': '#07080a',
            'bg_card': '#0d0d0d',
            'border': '#242728',
            'text': '#f4f4f6',
            'text_muted': '#9c9c9d',
            'radius': '10px',
            'input_border_radius_small': '8px',
            'input_border_radius_medium': '8px',
            'input_border_radius_large': '16px',
            'extra_css': """
                body {
                    font-family: Inter, system-ui, sans-serif !important;
                    font-feature-settings: 'calt' 1, 'kern' 1, 'liga' 1, 'ss03' 1;
                    background:
                        linear-gradient(160deg, rgba(255, 87, 87, 0.16) 0%, rgba(161, 19, 26, 0.0) 14%),
                        #07080a;
                    color: #f4f4f6;
                }
                .card {
                    background: #0d0d0d !important;
                    border: 1px solid #242728 !important;
                    border-radius: 10px !important;
                    box-shadow: none !important;
                }
                wa-button::part(base) {
                    border-radius: 8px !important;
                    border: 1px solid #242728 !important;
                }
                wa-button[variant='neutral']::part(base) {
                    background: #101111 !important;
                    color: #ffffff !important;
                }
                wa-input::part(base), wa-textarea::part(base), wa-select::part(combobox) {
                    background: #101111 !important;
                    border: 1px solid #242728 !important;
                    border-radius: 8px !important;
                }
                code, pre { font-family: 'JetBrains Mono', Menlo, monospace !important; }
            """
        },
        'violit_gallery_clean': {
            'mode': 'light',
            'primary': '#0066cc',
            'secondary': '#2997ff',
            'success': '#0066cc',
            'warning': '#f5f5f7',
            'danger': '#0071e3',
            'bg': '#ffffff',
            'bg_card': '#f5f5f7',
            'border': '#e0e0e0',
            'text': '#1d1d1f',
            'text_muted': '#7a7a7a',
            'radius': '18px',
            'input_border_radius_small': '11px',
            'input_border_radius_medium': '11px',
            'input_border_radius_large': '18px',
            'extra_css': """
                body {
                    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif !important;
                    background: linear-gradient(180deg, #ffffff 0%, #f5f5f7 100%);
                    color: #1d1d1f;
                }
                h1, h2, h3, h4, h5, h6 {
                    letter-spacing: -0.03em;
                    color: #1d1d1f;
                }
                .card {
                    background: #ffffff !important;
                    border: 1px solid #e0e0e0 !important;
                    border-radius: 18px !important;
                    box-shadow: none !important;
                }
                wa-button::part(base) {
                    border-radius: 9999px !important;
                    font-weight: 400 !important;
                }
                wa-button[variant='neutral']::part(base) {
                    background: transparent !important;
                    color: #0066cc !important;
                    border: 1px solid #0066cc !important;
                }
                #sidebar {
                    background: rgba(245, 245, 247, 0.8) !important;
                    backdrop-filter: saturate(180%) blur(20px) !important;
                }
            """
        },
        'violit_blocks_play': {
            'mode': 'light',
            'primary': '#000000',
            'secondary': '#cf5ff0',
            'success': '#2fb344',
            'warning': '#d8f65b',
            'danger': '#ff4d9d',
            'bg': '#ffffff',
            'bg_card': '#ffffff',
            'border': '#ebebeb',
            'text': '#111111',
            'text_muted': '#111111',
            'radius': '24px',
            'input_border_radius_small': '8px',
            'input_border_radius_medium': '8px',
            'input_border_radius_large': '24px',
            'extra_css': """
                body {
                    font-family: Inter, system-ui, sans-serif !important;
                    background:
                        linear-gradient(180deg, #ffffff 0%, #ffffff 60%, #fff8db 60%, #fff8db 100%);
                    color: #111111;
                }
                h1, h2, h3, h4, h5, h6 {
                    letter-spacing: -0.03em;
                    color: #111111;
                }
                .card {
                    background: #ffffff !important;
                    border: 1px solid #ebebeb !important;
                    border-radius: 24px !important;
                    box-shadow: none !important;
                }
                wa-button::part(base) {
                    border-radius: 9999px !important;
                    font-weight: 500 !important;
                }
                wa-button[variant='neutral']::part(base) {
                    background: #ffffff !important;
                    color: #111111 !important;
                    border: none !important;
                }
                wa-badge::part(base) {
                    border-radius: 9999px !important;
                }
            """
        },
        'violit_living_coral': {
            'mode': 'light',
            'primary': '#ff385c',
            'secondary': '#222222',
            'success': '#ff385c',
            'warning': '#f7f7f7',
            'danger': '#e00b41',
            'bg': '#ffffff',
            'bg_card': '#ffffff',
            'border': '#dddddd',
            'text': '#222222',
            'text_muted': '#6a6a6a',
            'radius': '14px',
            'input_border_radius_small': '8px',
            'input_border_radius_medium': '8px',
            'input_border_radius_large': '14px',
            'extra_css': """
                body {
                    font-family: Inter, system-ui, sans-serif !important;
                    background: #ffffff !important;
                    color: #222222;
                }
                .card {
                    background: #ffffff !important;
                    border: 1px solid #dddddd !important;
                    border-radius: 14px !important;
                    box-shadow: rgba(0, 0, 0, 0.02) 0 0 0 1px, rgba(0, 0, 0, 0.04) 0 2px 6px, rgba(0, 0, 0, 0.1) 0 4px 8px !important;
                }
                wa-button::part(base) {
                    border-radius: 8px !important;
                    font-weight: 500 !important;
                }
                wa-button[variant='neutral']::part(base) {
                    background: #ffffff !important;
                    color: #222222 !important;
                    border: 1px solid #222222 !important;
                }
                wa-input::part(base), wa-textarea::part(base), wa-select::part(combobox) {
                    border-radius: 9999px !important;
                    border: 1px solid #dddddd !important;
                }
            """
        },
        'violit_fin_messenger': {
            'mode': 'light',
            'primary': '#111111',
            'secondary': '#ff5600',
            'success': '#27ae60',
            'warning': '#f5f1ec',
            'danger': '#ff5600',
            'bg': '#f5f1ec',
            'bg_card': '#ffffff',
            'border': '#d3cec6',
            'text': '#111111',
            'text_muted': '#626260',
            'radius': '12px',
            'input_border_radius_small': '8px',
            'input_border_radius_medium': '8px',
            'input_border_radius_large': '16px',
            'extra_css': """
                body {
                    font-family: Inter, system-ui, sans-serif !important;
                    background: #f5f1ec !important;
                    color: #111111;
                }
                h1, h2, h3, h4, h5, h6 {
                    color: #111111;
                    letter-spacing: -0.03em;
                    font-weight: 500;
                }
                .card {
                    background: #ffffff !important;
                    border: 1px solid #d3cec6 !important;
                    border-radius: 16px !important;
                    box-shadow: none !important;
                }
                wa-button::part(base) {
                    border-radius: 8px !important;
                    font-weight: 500 !important;
                }
                wa-button[variant='danger']::part(base) {
                    background: #ff5600 !important;
                    color: #ffffff !important;
                    border: none !important;
                }
                wa-button[variant='neutral']::part(base) {
                    background: #ffffff !important;
                    color: #111111 !important;
                    border: 1px solid #d3cec6 !important;
                }
            """
        },
        'violit_signal_green': {
            'mode': 'light',
            'primary': '#76b900',
            'secondary': '#000000',
            'success': '#3f8500',
            'warning': '#df6500',
            'danger': '#e52020',
            'bg': '#ffffff',
            'bg_card': '#f7f7f7',
            'border': '#cccccc',
            'text': '#000000',
            'text_muted': '#757575',
            'radius': '2px',
            'input_border_radius_small': '2px',
            'input_border_radius_medium': '2px',
            'input_border_radius_large': '2px',
            'extra_css': """
                body {
                    font-family: Inter, Arial, sans-serif !important;
                    background: linear-gradient(180deg, #ffffff 0%, #f7f7f7 100%);
                    color: #000000;
                }
                .card {
                    background: #ffffff !important;
                    border: 1px solid #cccccc !important;
                    border-radius: 2px !important;
                    box-shadow: none !important;
                    position: relative;
                }
                .card::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 12px;
                    height: 12px;
                    background: #76b900;
                }
                wa-button::part(base) {
                    border-radius: 2px !important;
                    font-weight: 700 !important;
                }
                wa-button[variant='neutral']::part(base) {
                    background: transparent !important;
                    color: #000000 !important;
                    border: 2px solid #76b900 !important;
                }
                wa-input::part(base), wa-textarea::part(base), wa-select::part(combobox) {
                    border-radius: 2px !important;
                    border: 1px solid #cccccc !important;
                }
            """
        },
        'violit_cloud_foundry': {
            'mode': 'light',
            'primary': '#171717',
            'secondary': '#5b7cff',
            'success': '#12b76a',
            'warning': '#f79009',
            'danger': '#f04438',
            'bg': '#ffffff',
            'bg_card': '#ffffff',
            'border': '#e5e7eb',
            'text': '#101828',
            'text_muted': '#667085',
            'radius': '12px',
            'input_border_radius_small': '10px',
            'input_border_radius_medium': '12px',
            'input_border_radius_large': '16px',
            'extra_css': """
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

                body {
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
                    color: #101828;
                    background:
                        radial-gradient(circle at 12% -6%, rgba(91, 124, 255, 0.18), transparent 30%),
                        radial-gradient(circle at 88% 0%, rgba(0, 212, 164, 0.14), transparent 24%),
                        linear-gradient(180deg, #ffffff 0%, #fbfdff 46%, #f8fbff 100%);
                    -webkit-font-smoothing: antialiased;
                    -moz-osx-font-smoothing: grayscale;
                    font-feature-settings: 'liga' 1, 'calt' 1;
                    letter-spacing: -0.011em;
                }

                h1, h2, h3, h4, h5, h6 {
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
                    color: #0f1728;
                    letter-spacing: -0.035em;
                }

                h1 { font-weight: 700; }
                h2, h3 { font-weight: 650; }

                p, span, label, div, li {
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                }

                code, pre, .vl-mono {
                    font-family: ui-monospace, 'SFMono-Regular', Menlo, Consolas, monospace !important;
                    font-feature-settings: 'liga' 1, 'tnum' 1;
                }

                a {
                    color: #2563eb;
                    text-decoration: none;
                }

                a:hover {
                    color: #1d4ed8;
                }

                .card {
                    background: rgba(255, 255, 255, 0.82) !important;
                    border: none !important;
                    border-radius: 20px !important;
                    backdrop-filter: blur(16px) !important;
                    box-shadow:
                        rgba(15, 23, 42, 0.08) 0 0 0 1px,
                        rgba(15, 23, 42, 0.06) 0 10px 30px -16px,
                        rgba(255, 255, 255, 0.92) 0 1px 0 inset !important;
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                }

                .card:hover {
                    transform: translateY(-2px);
                    box-shadow:
                        rgba(15, 23, 42, 0.08) 0 0 0 1px,
                        rgba(15, 23, 42, 0.10) 0 18px 42px -22px,
                        rgba(255, 255, 255, 0.94) 0 1px 0 inset !important;
                }

                wa-button::part(base) {
                    background: #171717 !important;
                    color: #ffffff !important;
                    border: none !important;
                    border-radius: 9999px !important;
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
                    font-size: 0.875rem !important;
                    font-weight: 500 !important;
                    letter-spacing: -0.01em;
                    box-shadow: rgba(15, 23, 42, 0.14) 0 10px 24px -16px !important;
                    transition: transform 0.18s ease, box-shadow 0.18s ease, background-color 0.18s ease !important;
                }

                wa-button::part(base):hover {
                    background: #0f1728 !important;
                    transform: translateY(-1px);
                    box-shadow: rgba(15, 23, 42, 0.18) 0 16px 28px -18px !important;
                }

                wa-button::part(base):active {
                    transform: translateY(0) scale(0.985);
                }

                wa-button[variant="neutral"]::part(base) {
                    background: rgba(255, 255, 255, 0.92) !important;
                    color: #101828 !important;
                    box-shadow:
                        rgba(15, 23, 42, 0.08) 0 0 0 1px,
                        rgba(15, 23, 42, 0.08) 0 8px 18px -16px !important;
                }

                wa-button[variant="success"]::part(base) {
                    background: #ecfdf3 !important;
                    color: #067647 !important;
                    box-shadow: rgba(18, 183, 106, 0.22) 0 0 0 1px inset !important;
                }

                wa-button[variant="warning"]::part(base) {
                    background: #fff7ed !important;
                    color: #b54708 !important;
                    box-shadow: rgba(247, 144, 9, 0.22) 0 0 0 1px inset !important;
                }

                wa-button[variant="danger"]::part(base) {
                    background: #fff1f3 !important;
                    color: #c01048 !important;
                    box-shadow: rgba(240, 68, 56, 0.18) 0 0 0 1px inset !important;
                }

                wa-button:focus-visible::part(base) {
                    outline: 2px solid rgba(10, 114, 239, 0.95) !important;
                    outline-offset: 2px;
                }

                wa-input::part(base),
                wa-textarea::part(base),
                wa-select::part(combobox) {
                    background: rgba(255, 255, 255, 0.96) !important;
                    border: 1px solid #dfe3ea !important;
                    border-radius: 14px !important;
                    box-shadow:
                        rgba(15, 23, 42, 0.05) 0 1px 1px,
                        rgba(255, 255, 255, 0.9) 0 1px 0 inset !important;
                    transition: border-color 0.18s ease, box-shadow 0.18s ease !important;
                }

                wa-input::part(base):focus-within,
                wa-textarea::part(base):focus-within,
                wa-select::part(combobox):focus-within {
                    border-color: #0a72ef !important;
                    box-shadow:
                        rgba(10, 114, 239, 0.14) 0 0 0 4px,
                        rgba(15, 23, 42, 0.05) 0 1px 1px !important;
                }

                wa-textarea::part(form-control-input),
                wa-textarea::part(textarea) {
                    min-height: 6.5rem !important;
                    line-height: 1.55 !important;
                }

                #sidebar {
                    background: linear-gradient(180deg, rgba(255, 255, 255, 0.92), rgba(248, 251, 255, 0.88)) !important;
                    border-right: 1px solid rgba(15, 23, 42, 0.08) !important;
                    backdrop-filter: blur(18px) !important;
                }

                #sidebar wa-button::part(base) {
                    background: transparent !important;
                    color: #667085 !important;
                    box-shadow: none !important;
                    border: none !important;
                    border-radius: 16px !important;
                }

                #sidebar wa-button::part(base):hover {
                    background: rgba(255, 255, 255, 0.72) !important;
                    color: #0f1728 !important;
                    box-shadow: rgba(15, 23, 42, 0.06) 0 0 0 1px !important;
                    transform: none;
                }

                #sidebar wa-button[data-nav-active="true"]::part(base) {
                    background: rgba(255, 255, 255, 0.94) !important;
                    color: #0f1728 !important;
                    box-shadow:
                        rgba(15, 23, 42, 0.08) 0 0 0 1px,
                        rgba(15, 23, 42, 0.08) 0 10px 26px -18px !important;
                }

                table {
                    border-collapse: collapse;
                }

                th, td {
                    border-bottom: 1px solid #edf1f6;
                    padding: 0.75rem 0.875rem;
                    font-size: 0.875rem;
                }

                th {
                    color: #344054;
                    font-weight: 600;
                    text-align: left;
                }

                ::selection {
                    background: rgba(91, 124, 255, 0.16);
                    color: #0f1728;
                }

                ::-webkit-scrollbar {
                    width: 8px;
                    height: 8px;
                }

                ::-webkit-scrollbar-thumb {
                    background: rgba(148, 163, 184, 0.65);
                    border-radius: 9999px;
                }

                ::-webkit-scrollbar-track {
                    background: transparent;
                }
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
                wa-button::part(base) {
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
                wa-button::part(base):hover {
                    background: #8B5CF6 !important;
                    color: white !important;
                    box-shadow: 0 0 20px #8B5CF6, 0 0 40px rgba(139, 92, 246, 0.4) !important;
                    text-shadow: 0 1px 2px rgba(0,0,0,0.2);
                    transform: scale(1.02) !important;
                    border-color: transparent !important;
                }

                /* Active */
                wa-button::part(base):active {
                    transform: scale(0.95) !important;
                    box-shadow: 0 0 10px #8B5CF6 !important;
                }

                h1, h2, h3 {
                   color: #ede9fe;
                   text-shadow: 0 0 10px rgba(139, 92, 246, 0.5);
                }
                
                /* Inputs */
                wa-input::part(base) {
                    background: rgba(0,0,0,0.3) !important;
                    border: 1px solid #4c1d95 !important;
                }
                wa-input::part(base):focus-within {
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
        css_vars = [
            f"--vl-{k.replace('_', '-')}: {v};"
            for k, v in self.current.items() if k not in ['mode', 'extra_css', 'extra_js']
        ]
        css_vars.extend([
            f"--wa-color-brand-fill-loud: {self.current['primary']};",
            f"--wa-color-brand-border-loud: {self.current['primary']};",
            f"--wa-color-brand-fill-normal: color-mix(in srgb, {self.current['primary']}, white 18%);",
            f"--wa-color-brand-on-loud: {self.current['bg']};",
            f"--wa-color-surface-default: {self.current['bg']};",
            f"--wa-color-surface-raised: {self.current['bg_card']};",
            f"--wa-color-surface-border: {self.current['border']};",
            f"--wa-color-text-normal: {self.current['text']};",
            f"--wa-color-text-quiet: {self.current['text_muted']};",
            f"--wa-form-control-background: {self.current['bg_card']};",
            f"--wa-form-control-resting-border-color: {self.current['border']};",
            f"--wa-form-control-value-color: {self.current['text']};",
            f"--wa-border-radius-s: {self.current['input_border_radius_small']};",
            f"--wa-border-radius-m: {self.current['input_border_radius_medium']};",
            f"--wa-border-radius-l: {self.current['input_border_radius_large']};",
            f"--wa-border-radius-xl: {self.current['radius']};",
        ])
        return "\n".join(css_vars)
    
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
        return f"wa-theme-default wa-{self.mode}"


def _premium_light_theme_css(font_stack, body_background, *, heading_font=None, heading_weight="650", card_radius="18px", button_radius="12px", sidebar_background=None, special_css=""):
    heading_font = heading_font or font_stack
    sidebar_background = sidebar_background or "linear-gradient(180deg, color-mix(in srgb, var(--vl-bg) 92%, white 8%), color-mix(in srgb, var(--vl-bg-card) 72%, white 28%))"
    css = """
                body {
                    font-family: __FONT__ !important;
                    color: var(--vl-text);
                    background: __BODY_BG__;
                    -webkit-font-smoothing: antialiased;
                    -moz-osx-font-smoothing: grayscale;
                    font-feature-settings: 'liga' 1, 'calt' 1;
                    letter-spacing: -0.011em;
                }

                h1, h2, h3, h4, h5, h6 {
                    font-family: __HEADING_FONT__ !important;
                    color: var(--vl-text);
                    font-weight: __HEADING_WEIGHT__;
                    letter-spacing: -0.035em;
                    line-height: 1.15;
                }

                h1 { letter-spacing: -0.045em; }

                .card {
                    background: color-mix(in srgb, var(--vl-bg-card) 88%, white 12%) !important;
                    border: 1px solid color-mix(in srgb, var(--vl-border) 84%, white 16%) !important;
                    border-radius: __CARD_RADIUS__ !important;
                    box-shadow:
                        rgba(15, 23, 42, 0.06) 0 12px 34px -24px,
                        rgba(15, 23, 42, 0.04) 0 1px 0 inset,
                        rgba(255, 255, 255, 0.84) 0 1px 0 inset !important;
                    backdrop-filter: blur(16px) saturate(115%) !important;
                    transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease !important;
                }

                .card:hover {
                    transform: translateY(-2px);
                    border-color: color-mix(in srgb, var(--vl-primary) 14%, var(--vl-border) 86%) !important;
                    box-shadow:
                        rgba(15, 23, 42, 0.09) 0 20px 44px -28px,
                        rgba(15, 23, 42, 0.04) 0 1px 0 inset,
                        rgba(255, 255, 255, 0.92) 0 1px 0 inset !important;
                }

                wa-button::part(base) {
                    background: linear-gradient(135deg, var(--vl-primary) 0%, color-mix(in srgb, var(--vl-primary) 72%, var(--vl-secondary) 28%) 100%) !important;
                    border: none !important;
                    color: #ffffff !important;
                    border-radius: __BUTTON_RADIUS__ !important;
                    font-family: __FONT__ !important;
                    font-weight: 600 !important;
                    letter-spacing: -0.01em;
                    box-shadow:
                        rgba(15, 23, 42, 0.10) 0 14px 28px -18px,
                        color-mix(in srgb, var(--vl-primary) 18%, white 82%) 0 1px 0 inset !important;
                    transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease !important;
                }

                wa-button::part(base):hover {
                    transform: translateY(-1px);
                    filter: saturate(1.06);
                    box-shadow:
                        rgba(15, 23, 42, 0.14) 0 18px 36px -20px,
                        color-mix(in srgb, var(--vl-primary) 20%, white 80%) 0 1px 0 inset !important;
                }

                wa-button::part(base):active {
                    transform: translateY(0) scale(0.985);
                    box-shadow: rgba(15, 23, 42, 0.08) 0 8px 18px -16px !important;
                }

                wa-button[variant='neutral'][appearance='outlined']::part(base) {
                    background: color-mix(in srgb, white 84%, var(--vl-bg-card) 16%) !important;
                    color: var(--vl-text) !important;
                    border: 1px solid color-mix(in srgb, var(--vl-border) 88%, white 12%) !important;
                    box-shadow: rgba(15, 23, 42, 0.05) 0 8px 22px -22px !important;
                }

                wa-button[variant='neutral'][appearance='outlined']::part(base):hover {
                    background: color-mix(in srgb, white 72%, var(--vl-primary) 6%, var(--vl-bg-card) 22%) !important;
                    color: var(--vl-primary) !important;
                    border-color: color-mix(in srgb, var(--vl-primary) 18%, var(--vl-border) 82%) !important;
                }

                wa-button[variant='neutral'][appearance='plain']::part(base) {
                    background: transparent !important;
                    color: var(--vl-text-muted) !important;
                    border: none !important;
                    box-shadow: none !important;
                }

                wa-button[variant='neutral'][appearance='plain']::part(base):hover {
                    background: color-mix(in srgb, var(--vl-primary) 8%, transparent) !important;
                    color: var(--vl-primary) !important;
                    box-shadow: none !important;
                }

                wa-button[variant='success']::part(base) {
                    background: color-mix(in srgb, var(--vl-success) 14%, white 86%) !important;
                    color: color-mix(in srgb, var(--vl-success) 78%, black 22%) !important;
                    border: 1px solid color-mix(in srgb, var(--vl-success) 26%, white 74%) !important;
                    box-shadow: rgba(15, 23, 42, 0.04) 0 8px 18px -18px !important;
                }

                wa-button[variant='warning']::part(base) {
                    background: color-mix(in srgb, var(--vl-warning) 18%, white 82%) !important;
                    color: color-mix(in srgb, var(--vl-warning) 82%, black 18%) !important;
                    border: 1px solid color-mix(in srgb, var(--vl-warning) 28%, white 72%) !important;
                    box-shadow: rgba(15, 23, 42, 0.04) 0 8px 18px -18px !important;
                }

                wa-button[variant='danger']::part(base) {
                    background: color-mix(in srgb, var(--vl-danger) 14%, white 86%) !important;
                    color: color-mix(in srgb, var(--vl-danger) 78%, black 22%) !important;
                    border: 1px solid color-mix(in srgb, var(--vl-danger) 26%, white 74%) !important;
                    box-shadow: rgba(15, 23, 42, 0.04) 0 8px 18px -18px !important;
                }

                wa-input::part(base),
                wa-textarea::part(base),
                wa-select::part(combobox) {
                    background: color-mix(in srgb, white 88%, var(--vl-bg-card) 12%) !important;
                    border: 1px solid color-mix(in srgb, var(--vl-border) 86%, white 14%) !important;
                    border-radius: calc(__BUTTON_RADIUS__ - 2px) !important;
                    box-shadow: rgba(15, 23, 42, 0.04) 0 1px 2px !important;
                    transition: border-color 0.18s ease, box-shadow 0.18s ease, transform 0.18s ease !important;
                }

                wa-input::part(base):focus-within,
                wa-textarea::part(base):focus-within,
                wa-select::part(combobox):focus-within {
                    border-color: color-mix(in srgb, var(--vl-primary) 58%, white 42%) !important;
                    box-shadow: color-mix(in srgb, var(--vl-primary) 16%, transparent) 0 0 0 4px !important;
                }

                #sidebar {
                    background: __SIDEBAR_BG__ !important;
                    border-right: 1px solid color-mix(in srgb, var(--vl-border) 76%, white 24%) !important;
                    backdrop-filter: blur(16px) saturate(116%) !important;
                }

                #sidebar wa-button::part(base) {
                    background: transparent !important;
                    color: var(--vl-text-muted) !important;
                    border: none !important;
                    box-shadow: none !important;
                    border-radius: calc(__BUTTON_RADIUS__ + 2px) !important;
                }

                #sidebar wa-button::part(base):hover {
                    background: color-mix(in srgb, var(--vl-primary) 8%, transparent) !important;
                    color: var(--vl-primary) !important;
                    box-shadow: none !important;
                    transform: none !important;
                }

                #sidebar wa-button[data-nav-active='true'][variant='brand']::part(base) {
                    background: linear-gradient(135deg, var(--vl-primary) 0%, color-mix(in srgb, var(--vl-primary) 72%, var(--vl-secondary) 28%) 100%) !important;
                    color: #ffffff !important;
                    box-shadow: rgba(15, 23, 42, 0.12) 0 12px 24px -18px !important;
                }

                #sidebar wa-button[data-nav-active='true']::part(base) {
                    background: color-mix(in srgb, var(--vl-primary) 12%, white 88%) !important;
                    color: var(--vl-primary) !important;
                    box-shadow: rgba(15, 23, 42, 0.05) 0 10px 20px -18px !important;
                }

                a {
                    color: var(--vl-primary);
                    text-decoration: none;
                }

                a:hover {
                    color: color-mix(in srgb, var(--vl-primary) 82%, black 18%);
                }

                ::selection {
                    background: color-mix(in srgb, var(--vl-primary) 16%, white 84%);
                    color: var(--vl-text);
                }

                __SPECIAL__
    """
    return (
        css.replace("__FONT__", font_stack)
        .replace("__BODY_BG__", body_background)
        .replace("__HEADING_FONT__", heading_font)
        .replace("__HEADING_WEIGHT__", heading_weight)
        .replace("__CARD_RADIUS__", card_radius)
        .replace("__BUTTON_RADIUS__", button_radius)
        .replace("__SIDEBAR_BG__", sidebar_background)
        .replace("__SPECIAL__", special_css.strip())
        .strip()
    )


def _premium_dark_theme_css(font_stack, body_background, *, heading_font=None, heading_weight="650", card_radius="18px", button_radius="12px", sidebar_background=None, special_css=""):
    heading_font = heading_font or font_stack
    sidebar_background = sidebar_background or "linear-gradient(180deg, color-mix(in srgb, var(--vl-bg) 86%, black 14%), color-mix(in srgb, var(--vl-bg-card) 82%, black 18%))"
    css = """
                body {
                    font-family: __FONT__ !important;
                    color: var(--vl-text);
                    background: __BODY_BG__;
                    -webkit-font-smoothing: antialiased;
                    -moz-osx-font-smoothing: grayscale;
                    font-feature-settings: 'liga' 1, 'calt' 1;
                    letter-spacing: -0.011em;
                }

                h1, h2, h3, h4, h5, h6 {
                    font-family: __HEADING_FONT__ !important;
                    color: var(--vl-text);
                    font-weight: __HEADING_WEIGHT__;
                    letter-spacing: -0.035em;
                    line-height: 1.14;
                }

                .card {
                    background: color-mix(in srgb, var(--vl-bg-card) 90%, black 10%) !important;
                    border: 1px solid color-mix(in srgb, var(--vl-border) 86%, white 14%) !important;
                    border-radius: __CARD_RADIUS__ !important;
                    box-shadow:
                        rgba(2, 6, 23, 0.36) 0 18px 42px -30px,
                        color-mix(in srgb, var(--vl-primary) 8%, transparent) 0 1px 0 inset !important;
                    backdrop-filter: blur(16px) saturate(118%) !important;
                    transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease !important;
                }

                .card:hover {
                    transform: translateY(-2px);
                    border-color: color-mix(in srgb, var(--vl-primary) 22%, var(--vl-border) 78%) !important;
                    box-shadow:
                        rgba(2, 6, 23, 0.42) 0 24px 54px -30px,
                        color-mix(in srgb, var(--vl-primary) 10%, transparent) 0 1px 0 inset !important;
                }

                wa-button::part(base) {
                    background: linear-gradient(135deg, var(--vl-primary) 0%, color-mix(in srgb, var(--vl-primary) 64%, var(--vl-secondary) 36%) 100%) !important;
                    border: 1px solid color-mix(in srgb, var(--vl-primary) 36%, black 64%) !important;
                    color: color-mix(in srgb, white 94%, var(--vl-bg) 6%) !important;
                    border-radius: __BUTTON_RADIUS__ !important;
                    font-family: __FONT__ !important;
                    font-weight: 600 !important;
                    letter-spacing: -0.01em;
                    box-shadow:
                        rgba(2, 6, 23, 0.30) 0 18px 36px -24px,
                        color-mix(in srgb, var(--vl-primary) 18%, transparent) 0 0 0 1px inset !important;
                    transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease !important;
                }

                wa-button::part(base):hover {
                    transform: translateY(-1px);
                    filter: saturate(1.08);
                    box-shadow:
                        rgba(2, 6, 23, 0.36) 0 22px 42px -24px,
                        color-mix(in srgb, var(--vl-primary) 24%, transparent) 0 0 0 1px inset !important;
                }

                wa-button::part(base):active {
                    transform: translateY(0) scale(0.985);
                    box-shadow: rgba(2, 6, 23, 0.26) 0 10px 24px -20px !important;
                }

                wa-button[variant='neutral'][appearance='outlined']::part(base) {
                    background: color-mix(in srgb, var(--vl-bg-card) 82%, black 18%) !important;
                    color: var(--vl-text) !important;
                    border: 1px solid color-mix(in srgb, var(--vl-border) 90%, white 10%) !important;
                    box-shadow: rgba(2, 6, 23, 0.20) 0 12px 24px -24px !important;
                }

                wa-button[variant='neutral'][appearance='outlined']::part(base):hover {
                    background: color-mix(in srgb, var(--vl-bg-card) 74%, var(--vl-primary) 8%, black 18%) !important;
                    color: color-mix(in srgb, var(--vl-text) 90%, white 10%) !important;
                    border-color: color-mix(in srgb, var(--vl-primary) 24%, var(--vl-border) 76%) !important;
                }

                wa-button[variant='neutral'][appearance='plain']::part(base) {
                    background: transparent !important;
                    color: var(--vl-text-muted) !important;
                    border: none !important;
                    box-shadow: none !important;
                }

                wa-button[variant='neutral'][appearance='plain']::part(base):hover {
                    background: color-mix(in srgb, var(--vl-primary) 10%, transparent) !important;
                    color: var(--vl-text) !important;
                    box-shadow: none !important;
                }

                wa-button[variant='success']::part(base) {
                    background: color-mix(in srgb, var(--vl-success) 22%, black 78%) !important;
                    color: color-mix(in srgb, var(--vl-success) 82%, white 18%) !important;
                    border: 1px solid color-mix(in srgb, var(--vl-success) 34%, black 66%) !important;
                }

                wa-button[variant='warning']::part(base) {
                    background: color-mix(in srgb, var(--vl-warning) 22%, black 78%) !important;
                    color: color-mix(in srgb, var(--vl-warning) 82%, white 18%) !important;
                    border: 1px solid color-mix(in srgb, var(--vl-warning) 34%, black 66%) !important;
                }

                wa-button[variant='danger']::part(base) {
                    background: color-mix(in srgb, var(--vl-danger) 22%, black 78%) !important;
                    color: color-mix(in srgb, var(--vl-danger) 82%, white 18%) !important;
                    border: 1px solid color-mix(in srgb, var(--vl-danger) 34%, black 66%) !important;
                }

                wa-input::part(base),
                wa-textarea::part(base),
                wa-select::part(combobox) {
                    background: color-mix(in srgb, var(--vl-bg-card) 82%, black 18%) !important;
                    color: var(--vl-text) !important;
                    border: 1px solid color-mix(in srgb, var(--vl-border) 88%, white 12%) !important;
                    border-radius: calc(__BUTTON_RADIUS__ - 2px) !important;
                    box-shadow: rgba(2, 6, 23, 0.18) 0 8px 18px -18px !important;
                }

                wa-input::part(base):focus-within,
                wa-textarea::part(base):focus-within,
                wa-select::part(combobox):focus-within {
                    border-color: color-mix(in srgb, var(--vl-primary) 58%, white 42%) !important;
                    box-shadow: color-mix(in srgb, var(--vl-primary) 18%, transparent) 0 0 0 4px !important;
                }

                #sidebar {
                    background: __SIDEBAR_BG__ !important;
                    border-right: 1px solid color-mix(in srgb, var(--vl-border) 82%, white 18%) !important;
                    backdrop-filter: blur(18px) saturate(115%) !important;
                }

                #sidebar wa-button::part(base) {
                    background: transparent !important;
                    color: var(--vl-text-muted) !important;
                    border: none !important;
                    box-shadow: none !important;
                    border-radius: calc(__BUTTON_RADIUS__ + 2px) !important;
                }

                #sidebar wa-button::part(base):hover {
                    background: color-mix(in srgb, var(--vl-primary) 10%, transparent) !important;
                    color: var(--vl-text) !important;
                    box-shadow: none !important;
                }

                #sidebar wa-button[data-nav-active='true'][variant='brand']::part(base) {
                    background: linear-gradient(135deg, var(--vl-primary) 0%, color-mix(in srgb, var(--vl-primary) 64%, var(--vl-secondary) 36%) 100%) !important;
                    color: color-mix(in srgb, white 94%, var(--vl-bg) 6%) !important;
                }

                #sidebar wa-button[data-nav-active='true']::part(base) {
                    background: color-mix(in srgb, var(--vl-primary) 12%, var(--vl-bg-card) 88%) !important;
                    color: color-mix(in srgb, var(--vl-text) 92%, white 8%) !important;
                    box-shadow: rgba(2, 6, 23, 0.18) 0 12px 24px -22px !important;
                }

                a {
                    color: color-mix(in srgb, var(--vl-primary) 84%, white 16%);
                    text-decoration: none;
                }

                a:hover {
                    color: color-mix(in srgb, var(--vl-primary) 72%, white 28%);
                }

                ::selection {
                    background: color-mix(in srgb, var(--vl-primary) 18%, transparent);
                    color: color-mix(in srgb, white 92%, var(--vl-text) 8%);
                }

                __SPECIAL__
    """
    return (
        css.replace("__FONT__", font_stack)
        .replace("__BODY_BG__", body_background)
        .replace("__HEADING_FONT__", heading_font)
        .replace("__HEADING_WEIGHT__", heading_weight)
        .replace("__CARD_RADIUS__", card_radius)
        .replace("__BUTTON_RADIUS__", button_radius)
        .replace("__SIDEBAR_BG__", sidebar_background)
        .replace("__SPECIAL__", special_css.strip())
        .strip()
    )


def _soft_surface_theme_css(font_stack, body_background, *, relief_dark, relief_light, radius="24px", special_css=""):
    css = """
                body {
                    font-family: __FONT__ !important;
                    background: __BODY_BG__;
                    color: var(--vl-text);
                    -webkit-font-smoothing: antialiased;
                    -moz-osx-font-smoothing: grayscale;
                }

                .card {
                    background: var(--vl-bg-card) !important;
                    border: none !important;
                    border-radius: __RADIUS__ !important;
                    box-shadow:
                        18px 18px 36px __RELIEF_DARK__,
                        -18px -18px 36px __RELIEF_LIGHT__ !important;
                }

                wa-button::part(base) {
                    background: linear-gradient(135deg, color-mix(in srgb, var(--vl-primary) 18%, white 82%), color-mix(in srgb, var(--vl-secondary) 18%, white 82%)) !important;
                    border: none !important;
                    color: var(--vl-text) !important;
                    border-radius: calc(__RADIUS__ - 8px) !important;
                    font-family: __FONT__ !important;
                    font-weight: 600 !important;
                    box-shadow:
                        10px 10px 22px __RELIEF_DARK__,
                        -10px -10px 22px __RELIEF_LIGHT__ !important;
                }

                wa-button::part(base):active {
                    box-shadow:
                        inset 10px 10px 18px __RELIEF_DARK__,
                        inset -10px -10px 18px __RELIEF_LIGHT__ !important;
                }

                wa-button[variant='success']::part(base),
                wa-button[variant='warning']::part(base),
                wa-button[variant='danger']::part(base) {
                    color: var(--vl-text) !important;
                }

                wa-input::part(base),
                wa-textarea::part(base),
                wa-select::part(combobox) {
                    background: var(--vl-bg-card) !important;
                    border: none !important;
                    border-radius: calc(__RADIUS__ - 10px) !important;
                    box-shadow:
                        inset 8px 8px 16px __RELIEF_DARK__,
                        inset -8px -8px 16px __RELIEF_LIGHT__ !important;
                }

                __SPECIAL__
    """
    return (
        css.replace("__FONT__", font_stack)
        .replace("__BODY_BG__", body_background)
        .replace("__RADIUS__", radius)
        .replace("__RELIEF_DARK__", relief_dark)
        .replace("__RELIEF_LIGHT__", relief_light)
        .replace("__SPECIAL__", special_css.strip())
        .strip()
    )


Theme.PRESETS['light'].update({
    'primary': '#6d28d9',
    'secondary': '#8b5cf6',
    'success': '#0f9f6e',
    'warning': '#c98512',
    'danger': '#c24164',
    'border': '#e8e2f1',
    'text': '#191225',
    'text_muted': '#655a75',
    'radius': '14px',
    'input_border_radius_small': '10px',
    'input_border_radius_medium': '12px',
    'input_border_radius_large': '16px',
    'extra_css': _premium_light_theme_css(
        "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "radial-gradient(circle at 10% -6%, rgba(139, 92, 246, 0.14), transparent 28%), radial-gradient(circle at 88% 0%, rgba(236, 72, 153, 0.10), transparent 24%), linear-gradient(180deg, #ffffff 0%, #fbfaff 100%)",
        card_radius='18px',
        button_radius='14px',
    ),
})

Theme.PRESETS['dark'].update({
    'primary': '#9b8cff',
    'secondary': '#f472b6',
    'success': '#36d399',
    'warning': '#f4b942',
    'danger': '#fb7185',
    'bg': '#0b0b12',
    'bg_card': '#141420',
    'border': '#2a2a3d',
    'text': '#f5f7fb',
    'text_muted': '#9aa0b3',
    'radius': '16px',
    'input_border_radius_small': '10px',
    'input_border_radius_medium': '12px',
    'input_border_radius_large': '16px',
    'extra_css': _premium_dark_theme_css(
        "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "radial-gradient(circle at 14% -10%, rgba(155, 140, 255, 0.18), transparent 30%), radial-gradient(circle at 88% 0%, rgba(244, 114, 182, 0.12), transparent 24%), linear-gradient(180deg, #0b0b12 0%, #10111a 100%)",
        card_radius='18px',
        button_radius='14px',
    ),
})

Theme.PRESETS['ocean'].update({
    'bg': '#081522',
    'bg_card': '#102235',
    'border': '#1f4664',
    'text': '#ecf7ff',
    'text_muted': '#8fb6cc',
    'radius': '18px',
    'extra_css': _premium_dark_theme_css(
        "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "radial-gradient(circle at 12% -8%, rgba(34, 211, 238, 0.18), transparent 28%), radial-gradient(circle at 82% 0%, rgba(59, 130, 246, 0.14), transparent 24%), linear-gradient(180deg, #081522 0%, #0d1b2d 100%)",
        card_radius='20px',
        button_radius='14px',
    ),
})

Theme.PRESETS['sunset'].update({
    'bg': '#17110f',
    'bg_card': '#241715',
    'border': '#4f332b',
    'text': '#fff5ef',
    'text_muted': '#d4b3a5',
    'radius': '18px',
    'extra_css': _premium_dark_theme_css(
        "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "radial-gradient(circle at 14% -8%, rgba(249, 115, 22, 0.22), transparent 30%), radial-gradient(circle at 86% 0%, rgba(236, 72, 153, 0.12), transparent 22%), linear-gradient(180deg, #17110f 0%, #241715 100%)",
        card_radius='18px',
        button_radius='14px',
        special_css="h1, h2, h3 { text-shadow: 0 12px 28px rgba(249, 115, 22, 0.12); }",
    ),
})

Theme.PRESETS['forest'].update({
    'bg': '#08100a',
    'bg_card': '#112117',
    'border': '#255235',
    'text': '#eefbf1',
    'text_muted': '#95c6a2',
    'radius': '18px',
    'extra_css': _premium_dark_theme_css(
        "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "radial-gradient(circle at 18% -8%, rgba(34, 197, 94, 0.18), transparent 30%), radial-gradient(circle at 88% 0%, rgba(132, 204, 22, 0.12), transparent 22%), linear-gradient(180deg, #08100a 0%, #0f1a12 100%)",
        card_radius='18px',
        button_radius='14px',
    ),
})

Theme.PRESETS['cyberpunk'].update({
    'radius': '6px',
    'input_border_radius_small': '4px',
    'input_border_radius_medium': '6px',
    'input_border_radius_large': '8px',
    'extra_css': _premium_dark_theme_css(
        "'Space Grotesk', Inter, system-ui, sans-serif",
        "radial-gradient(circle at 16% -10%, rgba(0, 255, 234, 0.22), transparent 24%), radial-gradient(circle at 84% 0%, rgba(255, 0, 255, 0.18), transparent 22%), linear-gradient(180deg, #040512 0%, #090b1f 100%)",
        card_radius='10px',
        button_radius='8px',
        special_css="""
                body { background-image: linear-gradient(rgba(0, 255, 234, 0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 0, 255, 0.04) 1px, transparent 1px), radial-gradient(circle at 16% -10%, rgba(0, 255, 234, 0.22), transparent 24%), radial-gradient(circle at 84% 0%, rgba(255, 0, 255, 0.18), transparent 22%), linear-gradient(180deg, #040512 0%, #090b1f 100%); background-size: 32px 32px, 32px 32px, auto, auto, auto; }
                .card, wa-button::part(base), wa-input::part(base), wa-textarea::part(base), wa-select::part(combobox) { clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px); }
            """,
    ),
})

Theme.PRESETS['pastel'].update({
    'text': '#514d68',
    'text_muted': '#8d8395',
    'extra_css': _premium_light_theme_css(
        "'Nunito', Inter, 'Segoe UI', sans-serif",
        "radial-gradient(circle at 10% 0%, rgba(184, 192, 255, 0.32), transparent 30%), radial-gradient(circle at 88% 4%, rgba(255, 200, 221, 0.34), transparent 30%), linear-gradient(180deg, #fff4f8 0%, #fffdfd 100%)",
        card_radius='28px',
        button_radius='9999px',
        heading_weight='700',
        special_css="body { letter-spacing: -0.006em; } .card { box-shadow: rgba(164, 174, 197, 0.10) 0 18px 34px -28px, rgba(255, 255, 255, 0.94) 0 1px 0 inset !important; }",
    ),
})

Theme.PRESETS['retro'].update({
    'extra_css': _premium_light_theme_css(
        "'Fraunces', Georgia, serif",
        "linear-gradient(180deg, #fff7dd 0%, #fffbef 100%)",
        heading_font="'Fraunces', Georgia, serif",
        heading_weight='600',
        card_radius='14px',
        button_radius='10px',
        special_css="body::before { content: ''; position: fixed; inset: 0; pointer-events: none; opacity: 0.22; background-image: radial-gradient(rgba(146, 64, 14, 0.08) 0.6px, transparent 0.6px); background-size: 12px 12px; } wa-button::part(base) { text-transform: uppercase; letter-spacing: 0.08em; }",
    ),
})

Theme.PRESETS['dracula'].update({
    'radius': '16px',
    'input_border_radius_small': '10px',
    'input_border_radius_medium': '12px',
    'input_border_radius_large': '16px',
    'extra_css': _premium_dark_theme_css(
        "'Inter', system-ui, sans-serif",
        "radial-gradient(circle at 12% -10%, rgba(189, 147, 249, 0.20), transparent 28%), radial-gradient(circle at 90% 0%, rgba(255, 121, 198, 0.14), transparent 22%), linear-gradient(180deg, #282a36 0%, #232530 100%)",
        card_radius='18px',
        button_radius='14px',
    ),
})

Theme.PRESETS['monokai'].update({
    'radius': '14px',
    'input_border_radius_small': '10px',
    'input_border_radius_medium': '12px',
    'input_border_radius_large': '14px',
    'extra_css': _premium_dark_theme_css(
        "'JetBrains Mono', 'SFMono-Regular', Consolas, monospace",
        "radial-gradient(circle at 12% -10%, rgba(166, 226, 46, 0.18), transparent 28%), radial-gradient(circle at 86% 0%, rgba(249, 38, 114, 0.14), transparent 22%), linear-gradient(180deg, #272822 0%, #23241e 100%)",
        card_radius='16px',
        button_radius='12px',
        special_css="code, pre { font-family: 'JetBrains Mono', 'SFMono-Regular', Consolas, monospace !important; }",
    ),
})

Theme.PRESETS['ant'].update({
    'radius': '10px',
    'input_border_radius_small': '8px',
    'input_border_radius_medium': '10px',
    'input_border_radius_large': '12px',
    'extra_css': _premium_light_theme_css(
        "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "linear-gradient(180deg, #f4f6fb 0%, #ffffff 100%)",
        card_radius='14px',
        button_radius='10px',
        special_css="wa-button::part(base) { font-weight: 550 !important; }",
    ),
})

Theme.PRESETS['bootstrap'].update({
    'radius': '10px',
    'input_border_radius_small': '8px',
    'input_border_radius_medium': '10px',
    'input_border_radius_large': '12px',
    'extra_css': _premium_light_theme_css(
        "Inter, 'Segoe UI', sans-serif",
        "linear-gradient(180deg, #ffffff 0%, #f7f9fc 100%)",
        card_radius='14px',
        button_radius='10px',
    ),
})

Theme.PRESETS['material'].update({
    'radius': '24px',
    'input_border_radius_small': '12px',
    'input_border_radius_medium': '16px',
    'input_border_radius_large': '20px',
    'extra_css': _premium_light_theme_css(
        "'Inter', 'Roboto Flex', 'Segoe UI', sans-serif",
        "radial-gradient(circle at 12% 0%, rgba(103, 80, 164, 0.12), transparent 28%), linear-gradient(180deg, #fffbfe 0%, #f9f4fc 100%)",
        card_radius='24px',
        button_radius='18px',
        special_css="wa-button::part(base) { letter-spacing: 0 !important; }",
    ),
})

Theme.PRESETS['glass'].update({
    'extra_css': _premium_light_theme_css(
        "'SF Pro Text', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "radial-gradient(circle at 14% 0%, rgba(0, 122, 255, 0.16), transparent 26%), radial-gradient(circle at 88% 0%, rgba(88, 86, 214, 0.14), transparent 24%), linear-gradient(180deg, #f4f6fb 0%, #eef3fb 100%)",
        card_radius='22px',
        button_radius='9999px',
        special_css=".card { backdrop-filter: blur(22px) saturate(130%) !important; background: rgba(255, 255, 255, 0.62) !important; } #sidebar { backdrop-filter: blur(22px) saturate(130%) !important; }",
    ),
})

Theme.PRESETS['nord'].update({
    'radius': '16px',
    'input_border_radius_small': '10px',
    'input_border_radius_medium': '12px',
    'input_border_radius_large': '16px',
    'extra_css': _premium_dark_theme_css(
        "Inter, system-ui, sans-serif",
        "radial-gradient(circle at 12% -8%, rgba(136, 192, 208, 0.18), transparent 28%), radial-gradient(circle at 86% 0%, rgba(129, 161, 193, 0.14), transparent 24%), linear-gradient(180deg, #2e3440 0%, #252a34 100%)",
        card_radius='18px',
        button_radius='14px',
    ),
})

Theme.PRESETS['neo_brutalism'].update({
    'extra_css': """
                body { font-family: 'Space Grotesk', 'Arial Black', sans-serif !important; background: linear-gradient(180deg, #f5f5f5 0%, #ececec 100%); color: #000000; }
                h1, h2, h3, h4 { text-transform: uppercase; letter-spacing: -0.04em; }
                .card { background: #ffffff !important; border: 3px solid #000000 !important; border-radius: 18px !important; box-shadow: 14px 14px 0 rgba(0,0,0,0.92) !important; }
                .card:hover { transform: translate(-2px, -2px); box-shadow: 18px 18px 0 rgba(0,0,0,0.92) !important; }
                wa-button::part(base) { background: linear-gradient(135deg, #ffffff 0%, color-mix(in srgb, var(--vl-secondary) 16%, white 84%) 100%) !important; color: #000000 !important; border: 3px solid #000000 !important; border-radius: 16px !important; box-shadow: 8px 8px 0 rgba(0,0,0,0.96) !important; text-transform: uppercase; font-weight: 800 !important; letter-spacing: 0.04em; }
                wa-button::part(base):hover { transform: translate(-1px, -1px); }
                wa-button::part(base):active { transform: translate(3px, 3px) !important; box-shadow: 4px 4px 0 rgba(0,0,0,0.96) !important; }
                wa-input::part(base), wa-textarea::part(base), wa-select::part(combobox) { border: 3px solid #000000 !important; border-radius: 16px !important; box-shadow: 6px 6px 0 rgba(0,0,0,0.18) !important; }
            """.strip(),
})

Theme.PRESETS['soft_neu'].update({
    'text': '#465266',
    'text_muted': '#7c899d',
    'extra_css': _soft_surface_theme_css(
        "Inter, 'Segoe UI', sans-serif",
        "linear-gradient(180deg, #e8edf5 0%, #dde4ee 100%)",
        relief_dark='rgba(164, 177, 198, 0.36)',
        relief_light='rgba(255, 255, 255, 0.92)',
        radius='28px',
    ),
})

Theme.PRESETS['cyber_hud'].update({
    'radius': '8px',
    'input_border_radius_small': '6px',
    'input_border_radius_medium': '8px',
    'input_border_radius_large': '10px',
    'extra_css': _premium_dark_theme_css(
        "'Space Grotesk', 'JetBrains Mono', system-ui, sans-serif",
        "linear-gradient(rgba(0, 255, 255, 0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 255, 255, 0.04) 1px, transparent 1px), radial-gradient(circle at 16% -10%, rgba(0, 255, 255, 0.18), transparent 22%), linear-gradient(180deg, #000000 0%, #050a10 100%)",
        card_radius='12px',
        button_radius='8px',
        special_css="body { background-size: 20px 20px, 20px 20px, auto, auto; } .card, wa-button::part(base), wa-input::part(base), wa-textarea::part(base), wa-select::part(combobox) { clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px); }",
    ),
})

Theme.PRESETS['hand_drawn'].update({
    'extra_css': _premium_light_theme_css(
        "'Patrick Hand', 'Comic Sans MS', 'Segoe UI', sans-serif",
        "linear-gradient(180deg, #fffefa 0%, #fff8ef 100%)",
        heading_font="'Patrick Hand', 'Comic Sans MS', sans-serif",
        heading_weight='700',
        card_radius='28px 14px 26px 12px / 14px 22px 16px 28px',
        button_radius='24px 14px 22px 10px / 12px 20px 14px 24px',
        special_css=".card, wa-button::part(base), wa-input::part(base), wa-textarea::part(base), wa-select::part(combobox) { border-width: 2px !important; border-style: solid !important; }",
    ),
})

Theme.PRESETS['terminal'].update({
    'extra_css': _premium_dark_theme_css(
        "'JetBrains Mono', 'Courier New', monospace",
        "radial-gradient(circle at 50% -10%, rgba(0, 255, 0, 0.14), transparent 26%), linear-gradient(180deg, #050705 0%, #0a0a0a 100%)",
        card_radius='8px',
        button_radius='6px',
        special_css="body::after { content: ''; position: fixed; inset: 0; pointer-events: none; opacity: 0.08; background: repeating-linear-gradient(180deg, rgba(255,255,255,0.08) 0 1px, transparent 1px 3px); } * { text-shadow: 0 0 6px rgba(0,255,0,0.18); } wa-button[variant='neutral'][appearance='outlined']::part(base) { background: #050705 !important; }",
    ),
})

Theme.PRESETS['win95'].update({
    'extra_css': """
                body { font-family: Tahoma, 'MS Sans Serif', sans-serif !important; background: linear-gradient(180deg, #0b8a8a 0%, #067171 100%); color: #000000; }
                .card, wa-button::part(base), wa-input::part(base), wa-textarea::part(base), wa-select::part(combobox) { background: #c0c0c0 !important; border-top: 2px solid #ffffff !important; border-left: 2px solid #ffffff !important; border-right: 2px solid #3c3c3c !important; border-bottom: 2px solid #3c3c3c !important; box-shadow: 1px 1px 0 #808080 inset, -1px -1px 0 #dfdfdf inset !important; border-radius: 0 !important; }
                .card { padding-top: 0.25rem; }
                wa-button::part(base) { color: #000000 !important; font-weight: 700 !important; }
                wa-button::part(base):active { border-top: 2px solid #3c3c3c !important; border-left: 2px solid #3c3c3c !important; border-right: 2px solid #ffffff !important; border-bottom: 2px solid #ffffff !important; }
                h1, h2, h3 { font-weight: 700; text-shadow: 1px 1px 0 rgba(255,255,255,0.55); }
            """.strip(),
})

Theme.PRESETS['bauhaus'].update({
    'extra_css': _premium_light_theme_css(
        "'Space Grotesk', Inter, sans-serif",
        "linear-gradient(180deg, #f6f4f0 0%, #f1ede7 100%)",
        heading_font="'Space Grotesk', Inter, sans-serif",
        heading_weight='700',
        card_radius='10px',
        button_radius='9999px',
        special_css=".card { box-shadow: 10px 10px 0 color-mix(in srgb, var(--vl-secondary) 82%, white 18%), 20px 20px 0 color-mix(in srgb, var(--vl-primary) 82%, white 18%) !important; } h1, h2, h3 { text-transform: uppercase; } wa-button::part(base) { border: 2px solid #111 !important; color: #111 !important; background: color-mix(in srgb, var(--vl-warning) 34%, white 66%) !important; }",
    ),
})

Theme.PRESETS['vaporwave'].update({
    'extra_css': _premium_dark_theme_css(
        "'Space Grotesk', Inter, sans-serif",
        "radial-gradient(circle at 16% -10%, rgba(255, 113, 206, 0.22), transparent 26%), radial-gradient(circle at 84% 0%, rgba(1, 205, 254, 0.18), transparent 24%), linear-gradient(180deg, #2b2144 0%, #140d22 100%)",
        card_radius='18px',
        button_radius='14px',
        special_css="h1, h2, h3, h4 { background: linear-gradient(90deg, #ff71ce, #01cdfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; } .card { box-shadow: rgba(1, 205, 254, 0.14) 0 22px 48px -30px, rgba(185, 103, 255, 0.18) 0 0 0 1px inset !important; }",
    ),
})

Theme.PRESETS['blueprint'].update({
    'extra_css': _premium_dark_theme_css(
        "'IBM Plex Mono', 'Courier New', monospace",
        "linear-gradient(rgba(255,255,255,0.12) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.12) 1px, transparent 1px), linear-gradient(180deg, #0044bb 0%, #00318d 100%)",
        card_radius='10px',
        button_radius='8px',
        special_css="body { background-size: 24px 24px, 24px 24px, auto; } .card { background: rgba(0, 47, 140, 0.48) !important; } wa-button::part(base) { background: rgba(255,255,255,0.06) !important; border: 1px solid rgba(255,255,255,0.58) !important; color: white !important; }",
    ),
})

Theme.PRESETS['rgb_gamer'].update({
    'extra_css': _premium_dark_theme_css(
        "'Space Grotesk', Inter, sans-serif",
        "radial-gradient(circle at 14% -10%, rgba(255, 0, 0, 0.16), transparent 26%), radial-gradient(circle at 84% 0%, rgba(0, 255, 0, 0.14), transparent 22%), linear-gradient(180deg, #050505 0%, #101010 100%)",
        card_radius='16px',
        button_radius='12px',
        special_css="@keyframes vl-rgb-hue { from { filter: hue-rotate(0deg); } to { filter: hue-rotate(360deg); } } .card, wa-button::part(base) { animation: vl-rgb-hue 12s linear infinite; }",
    ),
})

Theme.PRESETS['editorial'].update({
    'extra_css': _premium_light_theme_css(
        "'Instrument Serif', 'Times New Roman', serif",
        "linear-gradient(180deg, #ffffff 0%, #fbfaf8 100%)",
        heading_font="'Cormorant Garamond', Georgia, serif",
        heading_weight='600',
        card_radius='6px',
        button_radius='8px',
        special_css="h1, h2, h3 { font-style: italic; border-bottom: 1px solid rgba(0,0,0,0.14); padding-bottom: 0.35rem; } wa-button[variant='neutral'][appearance='outlined']::part(base) { background: transparent !important; border-color: #111 !important; }",
    ),
})

Theme.PRESETS['claymorphism'].update({
    'extra_css': _soft_surface_theme_css(
        "'Inter', 'Segoe UI', sans-serif",
        "linear-gradient(180deg, #f4f7fb 0%, #ecf1f7 100%)",
        relief_dark='rgba(184, 196, 214, 0.40)',
        relief_light='rgba(255, 255, 255, 0.95)',
        radius='30px',
        special_css="wa-button::part(base) { color: white !important; background: linear-gradient(135deg, var(--vl-primary), color-mix(in srgb, var(--vl-primary) 72%, var(--vl-secondary) 28%)) !important; }",
    ),
})

Theme.PRESETS['inno'].update({
    'radius': '10px',
    'input_border_radius_small': '8px',
    'input_border_radius_medium': '10px',
    'input_border_radius_large': '12px',
    'extra_css': _premium_light_theme_css(
        "'Inter', 'Segoe UI', sans-serif",
        "radial-gradient(circle at 10% 0%, rgba(165, 0, 52, 0.08), transparent 24%), linear-gradient(180deg, #ffffff 0%, #faf9fb 100%)",
        card_radius='14px',
        button_radius='10px',
        special_css=".card { border-top: 3px solid #A50034 !important; } wa-button::part(base) { text-transform: uppercase; letter-spacing: 0.04em; }",
    ),
})

Theme.PRESETS['light_2nd'].update({
    'extra_css': _premium_light_theme_css(
        "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "radial-gradient(circle at 12% 0%, rgba(124, 58, 237, 0.10), transparent 28%), linear-gradient(180deg, #ffffff 0%, #fbfbff 100%)",
        card_radius='16px',
        button_radius='12px',
        special_css="body { font-feature-settings: 'liga' 1, 'kern' 1; }",
    ),
})

Theme.PRESETS['violit_dark'].update({
    'radius': '10px',
    'input_border_radius_small': '8px',
    'input_border_radius_medium': '10px',
    'input_border_radius_large': '12px',
    'extra_css': _premium_dark_theme_css(
        "'Space Grotesk', Inter, system-ui, sans-serif",
        "radial-gradient(circle at 16% -10%, rgba(139, 92, 246, 0.24), transparent 28%), radial-gradient(circle at 84% 0%, rgba(52, 211, 153, 0.14), transparent 20%), linear-gradient(180deg, #1e1b4b 0%, #0f0a20 100%)",
        card_radius='14px',
        button_radius='10px',
        special_css="h1, h2, h3 { text-shadow: 0 0 18px rgba(139, 92, 246, 0.24); } wa-button::part(base) { text-transform: uppercase; letter-spacing: 0.05em; }",
    ),
})
