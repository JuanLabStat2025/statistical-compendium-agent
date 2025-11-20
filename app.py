from datetime import datetime
import logging
import streamlit as st
import time
from base64 import b64encode
import random

#from connections import get_lambda_client

def get_lambda_client():
    return

logger = logging.getLogger()
logger.setLevel(logging.INFO)
lambda_client = get_lambda_client()


avatar = {
    "user": "https://api.dicebear.com/7.x/notionists-neutral/svg?seed=Felix",
    "assistant": "https://assets-global.website-files.com/62b1b25a5edaf66f5056b068/62d1345ba688202d5bfa6776_aws-sagemaker-eyecatch-e1614129391121.png",
}


def response_generator():
    response = random.choice(
        [
            "Hola, ¿en qué puedo ayudarte?",
            "¡Hola! ¿Qué necesitas hoy?",
            "¡Bienvenido! ¿Por dónde empezamos?",
            "Hola, ¿qué tal? Estoy listo para ayudarte.",
            "Hola, gracias por contactarte. ¿Cómo puedo ayudarte?",
            "🤖 ¡Saludos humanos! ¿Cuál es la misión?",
            "👋 ¡Hola! Soy tu asistente. ¿Listo/a?",
            "🚀 ¡A despegar! ¿Qué consultamos?",
        ]
    )
    return response
    # for word in response.split():
    #     yield word + " "
    #     time.sleep(0.05)


def get_response(user_input, session_id):
    """
    Get response from genai Lambda
    """
    logger.info(f"session id: {session_id}")
    response = lambda_client.invoke_sync(
        payload={"body": {"query": user_input, "session_id": session_id}},
    )
    time.sleep(3)
    logger.info(response)
    response_output = response["response"]
    logger.info(f"response_output from genai lambda: {response_output}")
    return response_output


def header():
    """
    App Header setting
    """
    font_b64 = get_base64("./assets/fonts/KdamThmorPro-Regular.ttf")
    inter_b64 = get_base64("./assets/fonts/Inter-VariableFont_opsz,wght.ttf")
    abeeze_b64 = get_base64("./assets/fonts/ABeeZee-Italic.ttf")
    inei_logo_b64 = get_base64("./assets/img/Logotipo-INEI.png")
    st.markdown(
        """
    <style>
    [data-testid="stMainBlockContainer"] {
        padding-top: 1rem;      /* antes suele ser ~6rem */
        padding-bottom: 1rem;   /* ajusta si quieres */
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
    with st.sidebar:
        sidebar_header = f"""
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
        st.markdown(sidebar_header, unsafe_allow_html=True)
        st.markdown(
            f"""
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
        """,
            unsafe_allow_html=True,
        )
        st.markdown("""
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
        """, unsafe_allow_html=True)

        st.markdown('<div class="feedback-title">💬 Tu opinión importa</div> <br>', unsafe_allow_html=True)
        
        comentarios = st.text_area(
            "comentarios",
            placeholder="✍️ Cuéntanos tu experiencia, sugerencias o reporta algún problema...",
            height=120,
            max_chars=500,
            key="feedback_comments",
            label_visibility="collapsed"
        )
        if st.button("📤 Enviar feedback", use_container_width=True, type="primary"):
            if comentarios:
                # Validación básica de email
                pass
            else:
                st.warning("Por favor escribe tus comentarios")



        st.markdown('<div class="feedback-title">🔄 ¿Algún problema?', unsafe_allow_html=True)
        st.markdown("<div class='guia-disclaimer'>Resetea el chat para empezar de nuevo</div>", unsafe_allow_html=True)

        if st.button("Reset Chat", type="primary", width="stretch"):
            st.session_state.messages = [
                {"role": "assistant", "content": response_generator()}
            ]
            st.rerun()

    st.set_page_config(
        page_title="Numy Bot",
        page_icon=":computer:",
        layout="wide",
    )

    col1_1, col1_2 = st.columns([1, 12], vertical_alignment="top")
    with col1_1:
        inei_logo_html = f"""
        <style>
        .hero-inei-logo {{
            position: relative;
            top: 1px;
            left: 30px;
            height: 100px;
        }}
        </style>
        <img src="data:image/png;base64,{inei_logo_b64}" class="hero-inei-logo" />
        """
        st.markdown(inei_logo_html, unsafe_allow_html=True)
    with col1_2:
        badge_html = f"""
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
        st.markdown(badge_html, unsafe_allow_html=True)

    _, col1, _ = st.columns([1, 3, 1])
    font_b64 = get_base64("./assets/fonts/KdamThmorPro-Regular.ttf")
    with col1:
        col1_1, col1_2 = st.columns([1, 3], gap="small")
        with col1_1:
            st.image(
                "./assets/img/Mascota Labstat.png",
                width=140,
            )
        with col1_2:
            bot_title_html = f"""
            <style>
            .hero-title {{
                font-family: 'KdamThmorPro', sans-serif;
                font-weight: 400;
                font-style: normal;
                font-size: 42px;
                line-height: 100%;
                color: #000000;
                line-height: 140%;
            }}
            </style>
            <div class="hero-title">Numy: Tu asistente de Datos Estadísticos</div>
            """
            st.markdown(bot_title_html, unsafe_allow_html=True)

        buble_content_html = """
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
        st.write(buble_content_html, unsafe_allow_html=True)


def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = (
        """
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
    """
        % bin_str
    )
    st.markdown(page_bg_img, unsafe_allow_html=True)


def initialization():
    """
    Initialize sesstion_state variables
    """
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(datetime.now()).replace(" ", "_")
        st.session_state.messages = []

    if "temp" not in st.session_state:
        st.session_state.temp = ""

    if "cache" not in st.session_state:
        st.session_state.cache = {}

    if "chat_button" not in st.session_state:
        st.session_state.chat_button = False


def disable_chat_input():
    st.session_state.chat_button = True


def enable_chat_input():
    st.session_state.chat_button = False
    st.rerun()


def show_message():
    """
    Show user question and answers
    """
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=avatar[message["role"]]):
            st.markdown(message["content"])

    if user_input := st.chat_input(
        "¿Cómo puedo ayudarte hoy?",
        max_chars=150,
        width="stretch",
        disabled=st.session_state.chat_button,
        on_submit=disable_chat_input,
    ):
        st.session_state.chat_button = True
        session_id = st.session_state.session_id
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar=avatar["user"]):
            st.markdown(user_input)

        with st.spinner("Procesando tu información ...", show_time=True):
            assistant = st.chat_message("assistant", avatar=avatar["assistant"])
            response_output = get_response(user_input, session_id)
            answer = "**Respuesta**: \n\n" + response_output["body"]
            st.session_state.messages.append({"role": "assistant", "content": answer})
            assistant.write(answer)
        enable_chat_input()
    st.markdown("""<style>
    [data-testid="stChatInputTextArea"] {
        padding: 12px 0;
        min-height: 80px !important;
        font-size: 20px !important;
    }
    
    .stChatInput div {
        min-height: 80px !important;
        font-size: 16px !important;
    }
    </style>""", unsafe_allow_html=True)


def show_header(logo_path):
    bin_header = get_base64(logo_path)
    page_hd_image = f"""
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
    <div class="fixed-logo">
        <img src="data:image/png;base64,{bin_header}" alt="INEI"/>
    </div>"""
    st.markdown(page_hd_image, unsafe_allow_html=True)


def show_footer(logo_path):
    bin_footer = get_base64(logo_path)
    page_ft_image = f"""
    <style>
      .corner-badge{{
        position: fixed; right: 14px; bottom: 14px; z-index: 9999;
        display: inline-flex; align-items: center; gap: 8px;
        font-size: 18px; font-weight: 600;
      }}
      .corner-badge img{{
        height: 36px; width: auto; display: block;
    }}
    </style>
    <div class="corner-badge">
      <span>Power by:</span>
      <img src="data:image/png;base64,{bin_footer}" alt="LabStat">
    </div>
    """
    st.markdown(page_ft_image, unsafe_allow_html=True)


def main():
    """
    Streamlit APP
    """
    header()
    show_header("./assets/img/Logotipo-INEI.png")
    set_background("./assets/img/Placa circuito.png")
    initialization()
    show_message()
    show_footer("./assets/img/Logo de Labstat.png")


if __name__ == "__main__":
    main()
