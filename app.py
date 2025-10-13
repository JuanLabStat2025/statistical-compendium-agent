from datetime import datetime
import logging
import json
import streamlit as st
import time
import random

# from streamlit_chat import message
from connections import get_lambda_client


logger = logging.getLogger()
logger.setLevel(logging.INFO)
lambda_client = get_lambda_client()


def log(message):
    logger.info(message)


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
    print(f"session id: {session_id}")
    # print(f"payload: {payload}")
    # response_output = {
    #     "source": "system",
    #     "answer": user_input
    #     }
    response = lambda_client.invoke_sync(
        payload={"body": {"query": user_input, "session_id": session_id}},
    )
    print(response)
    response_output = response["response"]
    print(f"response_output from genai lambda: {response_output}")
    return response_output


def header():
    """
    App Header setting
    """
    with st.sidebar:
        st.header("📚 User Guide")
        st.markdown(
            """
        ### How to Use
        1. **Start Chatting**: Type your message in the input box at the bottom of the chat
        2. **Continua conversando**: El chatbot recuerda tu conversación The chatbot remembers your conversation
        3. **View History**: Scroll up to see your chat history

        ### Tips
        - Be specific with your questions
        - Ask follow-up questions for clarification
        - Use the reset button to start a fresh conversation

        ### Need Help?
        If you encounter any issues, try resetting the chat using the button below.
        """
        )

        if st.button("Reset Chat"):
            st.session_state.messages = [
                {"role": "assistant", "content": response_generator()}
            ]
            st.rerun()

    st.set_page_config(
        page_title="Sigma Bot",
        page_icon=":computer:",
        layout="centered",
    )

    # Creating two columns, logo on the left and title on the right
    col1, col2 = st.columns(
        [1, 3]
    )  # The ratio between columns can be adjusted as needed

    with col1:
        st.image(
            "https://localo.com/es/assets/img/definitions/what-is-bot.webp",
            width=150,
        )

    with col2:
        st.markdown("# Sigma Bot: Tu Asistente de Datos Estadísticos")

    st.write("#### Hazme una pregunta sobre algún indicador que quisieras saber")
    st.write("-----")


def initialization():
    """
    Initialize sesstion_state variables
    """
    # --- Initialize session_state ---
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(datetime.now()).replace(" ", "_")
        st.session_state.messages = []
        st.session_state.questions = []
        st.session_state.answers = []

    if "temp" not in st.session_state:
        st.session_state.temp = ""

    # Initialize cache in session state
    if "cache" not in st.session_state:
        st.session_state.cache = {}


def show_message():
    """
    Show user question and answers
    """
    # Start a new conversation
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=avatar[message["role"]]):
            st.markdown(message["content"])

    if user_input := st.chat_input("¿Cómo puedo ayudarte hoy"):
        session_id = st.session_state.session_id
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar=avatar["user"]):
            st.markdown(user_input)

        with st.spinner("Procesando tu información ...", show_time=True):
            assistant = st.chat_message("assistant", avatar=avatar["assistant"])
            # vertical_space = show_empty_container()
            # vertical_space.empty()
            response_output = get_response(user_input, session_id)
            # response = get_agent_response(streaming_response)
            answer = "**Respuesta**: \n\n" + response_output["body"]
            st.session_state.messages.append({"role": "assistant", "content": answer})
            assistant.write(answer)


def main():
    """
    Streamlit APP
    """
    # --- Section 1 ---
    header()
    # --- Section 2 ---
    initialization()
    # --- Section 3 ---
    show_message()


if __name__ == "__main__":
    main()
