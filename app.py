from datetime import datetime
import logging
import streamlit as st
import random
import json
from typing import Dict, Any

from connections import get_lambda_client_bedrock, get_lambda_client_feedback
import config
import styles
from utils import get_base64

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize Lambda clients
lambda_client_bedrock = get_lambda_client_bedrock("getAgentResponse")
lambda_client_feedback = get_lambda_client_feedback("SendFeedbackFunction")


def response_generator() -> str:
    """
    Generates a random greeting response.

    Returns:
        str: A random greeting message.
    """
    return random.choice(config.GREETINGS)


def get_response(user_input: str, session_id: str) -> Dict[str, Any]:
    """
    Get response from GenAI Lambda.

    Args:
        user_input (str): The user's query.
        session_id (str): The current session ID.

    Returns:
        Dict[str, Any]: The response containing the answer.
    """
    logger.info(f"session id: {session_id}")
    response = lambda_client_bedrock.invoke_sync(
        payload={"body": {"query": user_input, "session_id": session_id}},
    )
    logger.info(response)
    try:
        response_output = {"answer": json.loads(response["body"])["answer"]}
    except Exception as e:
        logger.error(f"Error parsing response: {e}")
        response_output = {
            "answer": "Hola, no entendí tu mensaje. ¡Puedes reformular mejor tu pregunta por favor!"
        }

    logger.info(f"response_output from genai lambda: {response_output}")
    return response_output


def header() -> None:
    """
    Sets up the application header and sidebar.
    """
    # Load fonts
    font_b64 = get_base64(config.FONT_KDAM_THMOR)
    inter_b64 = get_base64(config.FONT_INTER)

    # Main style
    st.markdown(styles.get_main_style(), unsafe_allow_html=True)

    with st.sidebar:
        # Sidebar Header
        st.markdown(styles.get_sidebar_header_style(font_b64), unsafe_allow_html=True)

        # Sidebar Content
        st.markdown(styles.get_sidebar_content_style(inter_b64), unsafe_allow_html=True)

        # Feedback Section
        st.markdown(styles.get_feedback_style(), unsafe_allow_html=True)
        st.markdown(
            '<div class="feedback-title">💬 Tu opinión importa</div> <br>',
            unsafe_allow_html=True,
        )

        comentarios = st.text_area(
            "comentarios",
            placeholder="✍️ Cuéntanos tu experiencia, sugerencias o reporta algún problema...",
            height=120,
            max_chars=500,
            key="feedback_comments",
            label_visibility="collapsed",
        )

        if st.button("📤 Enviar feedback", use_container_width=True, type="primary"):
            if comentarios:
                response = lambda_client_feedback.invoke_sync(
                    payload={
                        "body": {
                            "feedback": comentarios,
                            "session_id": st.session_state.session_id,
                        }
                    },
                )
                logger.info(json.dumps(response))
                if response.get("statusCode") == 200:
                    st.success("Feedback enviado correctamente", icon="✅")
                else:
                    st.error(
                        f"Error al enviar el feedback: {json.dumps(response)}",
                        icon="❌",
                    )
            else:
                st.warning("Por favor escribe tus comentarios", icon="⚠️")

        st.markdown(
            '<div class="feedback-title">🔄 ¿Algún problema?', unsafe_allow_html=True
        )
        st.markdown(
            "<div class='guia-disclaimer'>Resetea el chat para empezar de nuevo</div>",
            unsafe_allow_html=True,
        )

        if st.button("Reset Chat", type="primary", use_container_width=True):
            st.session_state.messages = [
                {"role": "assistant", "content": response_generator()}
            ]
            st.rerun()


def set_background(png_file: str) -> None:
    """
    Sets the background image of the application.

    Args:
        png_file (str): Path to the PNG image file.
    """
    bin_str = get_base64(png_file)
    st.markdown(styles.get_background_style(bin_str), unsafe_allow_html=True)


def initialization() -> None:
    """
    Initialize session_state variables.
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


def disable_chat_input() -> None:
    """
    Callback to disable chat input.
    """
    st.session_state.chat_button = True


def enable_chat_input() -> None:
    """
    Callback to enable chat input and rerun the app.
    """
    st.session_state.chat_button = False
    st.rerun()


def show_message() -> None:
    """
    Display user question and answers in the chat interface.
    """
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=config.AVATAR[message["role"]]):
            st.markdown(message["content"])

    if user_input := st.chat_input(
        "¿Cómo puedo ayudarte hoy?",
        max_chars=300,
        disabled=st.session_state.chat_button,
        on_submit=disable_chat_input,
    ):
        st.session_state.chat_button = True
        session_id = st.session_state.session_id
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar=config.AVATAR["user"]):
            st.markdown(user_input)

        with st.spinner("Procesando tu información ...", show_time=True):
            assistant = st.chat_message("assistant", avatar=config.AVATAR["assistant"])
            response_output = get_response(user_input, session_id)
            answer = "**Respuesta**: \n\n" + response_output["answer"]
            st.session_state.messages.append({"role": "assistant", "content": answer})
            assistant.write(answer)
        enable_chat_input()

    st.markdown(styles.get_chat_input_style(), unsafe_allow_html=True)


def show_footer(logo_path: str, inei_logo_path: str) -> None:
    """
    Display the footer with logos.

    Args:
        logo_path (str): Path to the LabStat logo.
        inei_logo_path (str): Path to the INEI logo.
    """
    bin_footer = get_base64(logo_path)
    bin_inei = get_base64(inei_logo_path)
    st.markdown(styles.get_footer_style(bin_inei, bin_footer), unsafe_allow_html=True)


def main() -> None:
    """
    Main function to run the Streamlit App.
    """
    # Page Configuration
    st.set_page_config(
        page_title="Numy Bot",
        page_icon=":computer:",
        layout="wide",
    )

    initialization()
    header()
    set_background(config.IMG_BACKGROUND)

    # Main Content Layout
    col1_1, col1_2 = st.columns([1, 12], vertical_alignment="top")
    with col1_1:
        pass

    with col1_2:
        abeeze_b64 = get_base64(config.FONT_ABEEZE)
        st.markdown(styles.get_beta_badge_style(abeeze_b64), unsafe_allow_html=True)

    _, col1, _ = st.columns([1, 3, 1])
    with col1:
        col1_1, col1_2 = st.columns([1, 3], gap="small")
        with col1_1:
            st.image(
                config.IMG_MASCOTA,
                width=140,
            )
        with col1_2:
            st.markdown(styles.get_hero_title_style(), unsafe_allow_html=True)

        st.write(styles.get_chat_bubble_style(), unsafe_allow_html=True)

    show_message()
    show_footer(config.IMG_LOGO_LABSTAT, config.IMG_LOGO_INEI)


if __name__ == "__main__":
    main()
