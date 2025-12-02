def get_main_style() -> str:
    return """
    <style>
    [data-testid="stMainBlockContainer"] {
        padding-top: 1rem;      /* antes suele ser ~6rem */
        padding-bottom: 1rem;   /* ajusta si quieres */
    }
    </style>
    """

def get_sidebar_header_style(font_b64: str) -> str:
    return f"""
    <style>
    @font-face {{
        font-family: "KdamThmorPro";
        src: url(data:font/ttf;base64,{font_b64}) format("truetype");
        font-weight: 400;
        font-style: normal;
    }}
    .header_text {{
        font-family: "KdamThmorPro";
        font-size: 27px;
        font-style: normal;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
        text-align: center;
    }}
    </style>
    <div class="header_text">ℹ️ Nota importante</div>
    """

def get_sidebar_content_style(inter_b64: str) -> str:
    return f"""
    <style>
    @font-face {{
        font-family: "Inter";
        src: url(data:font/ttf;base64,{inter_b64}) format("truetype");
        font-weight: 400;
        font-style: normal;
    }}
    .guia-subtitle {{
        font-family: 'Inter-Italic', sans-serif;
        font-size: 18px;
        padding-left: 0.8rem;
        margin-bottom: 0.5rem;
    }}
    .guia-list {{
        font-family: "Inter";
        font-size: 25px;
        font-style: normal;
        padding-left: 0.8rem;
    }}
    .guia-disclaimer {{
        font-family: "Inter";
        font-style: normal;
        font-size: 16px;
        padding-left: 0.8rem;
        margin-bottom: 0.5rem;
    }}
    </style>
    <div class="guia-disclaimer">La información de este chatbot se genera mediante IA. Aunque se busca precisión, las respuestas pueden incluir errores u omisiones.</div>
    """

def get_feedback_style() -> str:
    return """
    <style>
    .feedback-container {
        margin-top: 30px;
        padding: 15px;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
    }
    .feedback-title {
        font-family: "KdamThmorPro";
        font-style: normal;
        font-size: 27px;
        color: white;
        text-align: center;
    }
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #2D3748 !important;
        border: 2px solid #6B46C1 !important;
        border-radius: 10px !important;
        font-size: 15px !important;
        padding: 12px !important;
    }
    .stTextArea textarea:focus {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2) !important;
    }
    .stTextArea textarea::placeholder {
        color: #999999 !important;
    }
    </style>
    """

def get_beta_badge_style(abeeze_b64: str) -> str:
    return f"""
    <style>
    @font-face {{
        font-family: "Abeeze";
        src: url(data:font/ttf;base64,{abeeze_b64}) format("truetype");
        font-weight: 400;
        font-style: normal;
    }}
    .beta-badge {{
        position: absolute;
        top: 24px;
        right: 40px;
        background: #D9D9D9;
        border-radius: 999px;
        padding: 8px 20px;
        font-family: 'Abeeze', sans-serif;
        font-weight: bold;
        font-size: 16px;
        color: #333333;
    }}
    </style>
    <div class="beta-badge">Versión beta de prueba</div>"""

def get_hero_title_style() -> str:
    return """
    <style>
    .hero-title {
        font-family: 'KdamThmorPro', sans-serif;
        font-weight: 400;
        font-style: normal;
        font-size: 42px;
        line-height: 100%;
        color: #000000;
        line-height: 140%;
    }
    </style>
    <div class="hero-title">Numy: Tu asistente de Datos Estadísticos</div>
    """

def get_chat_bubble_style() -> str:
    return """
    <style>
    .chat-bubble {
        background: #2196B5;
        color: white;
        padding: 20px 25px;
        border-radius: 15px;
        position: relative;
        max-width: 600px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Flecha superior */
    .chat-bubble::before {
        content: '';
        position: absolute;
        top: -10px;
        left: 50px;
        width: 0;
        height: 0;
        border-left: 15px solid transparent;
        border-right: 15px solid transparent;
        border-bottom: 15px solid #2196B5;
    }
    
    .chat-bubble-title {
        font-family: 'KdamThmorPro', sans-serif;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 8px;
    }
    
    .chat-bubble-subtitle {
        font-family: 'KdamThmorPro', sans-serif;
        font-size: 14px;
        opacity: 0.95;
    }
    </style>
    <div class="chat-bubble">
        <div class="chat-bubble-title">¿Cómo consultar?</div>
        <div class="chat-bubble-subtitle">Escribe en la casilla gris de abajo el tema o indicador de interés, seguido del año y la región o ciudad.<br>Ejemplo: PBI de Ica en el 2022</div>
    </div>
    """

def get_background_style(bin_str: str) -> str:
    return """
    <style>
    .st-emotion-cache-6px8kg {
    background-image: linear-gradient(
            rgba(255, 255, 255, 0.90),
            rgba(255, 255, 255, 0.90)
        ),
        url("data:image/png;base64,%s");;
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    }
    </style>
    """ % bin_str

def get_chat_input_style() -> str:
    return """<style>
    [data-testid="stChatInputTextArea"] {
        padding: 12px 0;
        min-height: 80px !important;
        font-size: 20px !important;
    }
    
    .stChatInput div {
        min-height: 80px !important;
        font-size: 16px !important;
        bottom: 10px !important;
    }
    </style>"""

def get_fixed_logo_style(bin_header: str) -> str:
    return f"""
    <style>
    .fixed-logo {{
        position: fixed;
        top: 20px;
        left: 250px;
        z-index: 999;
        background: white;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    .fixed-logo img {{
        height: 60px;  /* Ajusta el tamaño */
        width: auto;
    }}
    [data-testid="collapsedControl"] ~ div .fixed-logo {{
        left: 80px;
    }}
    </style>
    <div class="fixed-logo">
        <img src="data:image/png;base64,{bin_header}" alt="INEI"/>
    </div>"""

def get_footer_style(bin_inei: str, bin_footer: str) -> str:
    return f"""
    <style>
    .corner-badge{{
        position: fixed; right: 14px; bottom: 14px; z-index: 9999;
        display: inline-flex; align-items: center; gap: 8px;
        font-size: 16px; font-weight: 600;
    }}
    .corner-badge-inei{{
        height: 44px; width: auto; display: block;
    }}
    .corner-badge-labstat{{
        height: 30px; width: auto; display: block;
    }}
    </style>
    <div class="corner-badge">
      <img class="corner-badge-inei" src="data:image/png;base64,{bin_inei}" alt="INEI">
      <span>Power by:</span>
      <img class="corner-badge-labstat" src="data:image/png;base64,{bin_footer}" alt="LabStat">
    </div>
    """
