from typing import Dict, List

# Assets
ASSETS_DIR: str = "./assets"
FONTS_DIR: str = f"{ASSETS_DIR}/fonts"
IMG_DIR: str = f"{ASSETS_DIR}/img"

# Fonts
FONT_KDAM_THMOR: str = f"{FONTS_DIR}/KdamThmorPro-Regular.ttf"
FONT_INTER: str = f"{FONTS_DIR}/Inter-VariableFont_opsz,wght.ttf"
FONT_ABEEZE: str = f"{FONTS_DIR}/ABeeZee-Italic.ttf"

# Images
IMG_MASCOTA: str = f"{IMG_DIR}/Mascota Labstat.png"
IMG_LOGO_INEI: str = f"{IMG_DIR}/Logotipo-INEI.png"
IMG_LOGO_LABSTAT: str = f"{IMG_DIR}/Logo de Labstat.png"
IMG_BACKGROUND: str = f"{IMG_DIR}/Placa circuito.png"

# Avatars
AVATAR: Dict[str, str] = {
    "user": "https://api.dicebear.com/7.x/notionists-neutral/svg?seed=Felix",
    "assistant": "https://assets-global.website-files.com/62b1b25a5edaf66f5056b068/62d1345ba688202d5bfa6776_aws-sagemaker-eyecatch-e1614129391121.png",
}

# Responses
GREETINGS: List[str] = [
    "Hola, ¿en qué puedo ayudarte?",
    "¡Hola! ¿Qué necesitas hoy?",
    "¡Bienvenido! ¿Por dónde empezamos?",
    "Hola, ¿qué tal? Estoy listo para ayudarte.",
    "Hola, gracias por contactarte. ¿Cómo puedo ayudarte?",
    "🤖 ¡Saludos humanos! ¿Cuál es la misión?",
    "👋 ¡Hola! Soy tu asistente. ¿Listo/a?",
    "🚀 ¡A despegar! ¿Qué consultamos?",
]
