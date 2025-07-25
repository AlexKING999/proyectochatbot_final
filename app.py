import streamlit as st
import requests
import json
from datetime import datetime
import re
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Chatbot ISTA",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Configuration ---
API_BASE_URL = os.getenv('API_BASE_URL', 'https://ogh5izce1p8v.manus.space')

# --- Custom CSS (Updated Design with New Colors) ---
st.markdown("""
<style>
    /* Colores institucionales actualizados */
    :root {
        --primary-blue: #035AA6;      /* Azul principal */
        --secondary-blue: #033F73;    /* Azul secundario */
        --dark-blue: #033F73;         /* Azul oscuro */
        --accent-yellow: #F2B705;     /* Amarillo principal */
        --bright-yellow: #D9A404;     /* Amarillo brillante */
        --light-bg: #f8fafc;          /* Fondo claro */
        --white: #ffffff;
        --text-dark: #1e293b;
        --border-light: #e2e8f0;
    }

    /* Fondo principal con gradiente institucional */
    .stApp {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 50%, var(--accent-yellow) 100%);
        background-attachment: fixed;
        min-height: 100vh;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(248, 250, 252, 0.95);
        z-index: -1;
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(90deg, var(--primary-blue) 0%, var(--secondary-blue) 50%, var(--accent-yellow) 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(3, 90, 166, 0.4);
        border: 3px solid var(--accent-yellow);
    }
    
    .main-header h1 {
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 15px;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    /* Contenedor del logo mejorado */
    .header-logo-container {
        text-align: center;
        padding: 30px;
        margin-bottom: 30px;
        background: linear-gradient(135deg, var(--white) 0%, #f8fafc 100%);
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(3, 90, 166, 0.2);
        border: 4px solid var(--accent-yellow);
        position: relative;
        overflow: hidden;
    }
    
    .header-logo-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, var(--primary-blue) 0%, var(--accent-yellow) 100%);
    }
    
    /* Contenedor principal del chat */
    .chat-main-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    /* Área de conversación mejorada */
    .chat-conversation-area {
        background: var(--white);
        border-radius: 20px;
        border: 4px solid var(--accent-yellow);
        box-shadow: 0 12px 40px rgba(3, 90, 166, 0.25);
        margin-bottom: 25px;
        overflow: hidden;
        height: 550px;
        display: flex;
        flex-direction: column;
    }
    
    .chat-header {
        background: linear-gradient(90deg, var(--primary-blue) 0%, var(--accent-yellow) 100%);
        color: white;
        padding: 20px 30px;
        font-weight: bold;
        font-size: 1.2rem;
        border-bottom: 3px solid var(--bright-yellow);
        flex-shrink: 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    .chat-messages-container {
        flex: 1;
        overflow-y: auto;
        padding: 25px;
        background: var(--light-bg);
        scrollbar-width: thin;
        scrollbar-color: var(--accent-yellow) var(--light-bg);
    }
    
    /* Mensajes del chat */
    .user-message {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 10px 0 10px 50px;
        box-shadow: 0 4px 15px rgba(3, 90, 166, 0.3);
        border: 2px solid var(--accent-yellow);
        position: relative;
    }
    
    .user-message::before {
        content: "👤";
        position: absolute;
        left: -35px;
        top: 50%;
        transform: translateY(-50%);
        background: var(--accent-yellow);
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        border: 2px solid var(--primary-blue);
    }
    
    .bot-message {
        background: linear-gradient(135deg, var(--white) 0%, #f8fafc 100%);
        color: var(--text-dark);
        padding: 15px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 50px 10px 0;
        box-shadow: 0 4px 15px rgba(3, 90, 166, 0.2);
        border: 2px solid var(--primary-blue);
        position: relative;
    }
    
    .bot-message::before {
        content: "🤖";
        position: absolute;
        right: -35px;
        top: 50%;
        transform: translateY(-50%);
        background: var(--primary-blue);
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        border: 2px solid var(--accent-yellow);
    }
    
    /* Botones de acción rápida */
    .quick-action-button {
        background: linear-gradient(135deg, var(--accent-yellow) 0%, var(--bright-yellow) 100%);
        color: var(--dark-blue);
        border: 2px solid var(--primary-blue);
        border-radius: 15px;
        padding: 12px 20px;
        margin: 5px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(242, 183, 5, 0.3);
    }
    
    .quick-action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(242, 183, 5, 0.4);
        background: linear-gradient(135deg, var(--bright-yellow) 0%, var(--accent-yellow) 100%);
    }
    
    /* Sidebar mejorado */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--white) 0%, var(--light-bg) 100%);
        border-right: 4px solid var(--accent-yellow);
    }
    
    /* Input del chat */
    .stTextInput > div > div > input {
        border: 3px solid var(--primary-blue);
        border-radius: 15px;
        padding: 15px;
        font-size: 16px;
        background: var(--white);
        color: var(--text-dark);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-yellow);
        box-shadow: 0 0 0 3px rgba(242, 183, 5, 0.2);
    }
    
    /* Botón de envío */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
        color: white;
        border: 2px solid var(--accent-yellow);
        border-radius: 15px;
        padding: 12px 30px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(3, 90, 166, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(3, 90, 166, 0.4);
        background: linear-gradient(135deg, var(--secondary-blue) 0%, var(--primary-blue) 100%);
    }
    
    /* Información de contacto */
    .contact-info {
        background: linear-gradient(135deg, var(--white) 0%, #f8fafc 100%);
        border: 3px solid var(--primary-blue);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 8px 30px rgba(3, 90, 166, 0.2);
    }
    
    .contact-info h3 {
        color: var(--primary-blue);
        border-bottom: 3px solid var(--accent-yellow);
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    
    /* Métricas */
    .metric-container {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 3px solid var(--accent-yellow);
        box-shadow: 0 6px 20px rgba(3, 90, 166, 0.3);
    }
    
    /* Animaciones */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .chat-main-container {
            padding: 0 10px;
        }
        
        .user-message, .bot-message {
            margin-left: 20px;
            margin-right: 20px;
        }
        
        .user-message::before, .bot-message::before {
            display: none;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- API Functions ---
def check_api_health():
    """Verificar el estado de la API"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def send_message_to_api(message, session_id=None):
    """Enviar mensaje a la API del chatbot"""
    try:
        payload = {"message": message}
        if session_id:
            payload["session_id"] = session_id
            
        response = requests.post(
            f"{API_BASE_URL}/api/chat/message",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "error": f"Error HTTP {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_careers_from_api():
    """Obtener carreras desde la API"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/carreras", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "error": f"Error HTTP {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# --- Initialize Session State ---
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'api_connected' not in st.session_state:
    st.session_state.api_connected = check_api_health()

# --- Header ---
st.markdown("""
<div class="main-header fade-in-up">
    <h1>🎓 Chatbot ISTA</h1>
    <p style="font-size: 1.2rem; margin: 0;">Instituto Superior Tecnológico del Azuay</p>
    <p style="font-size: 1rem; margin-top: 10px; opacity: 0.9;">Tu asistente virtual para información académica</p>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("""
    <div class="header-logo-container fade-in-up">
        <h2 style="color: var(--primary-blue); margin-bottom: 20px;">🏛️ ISTA</h2>
        <p style="color: var(--text-dark); font-weight: 500;">Instituto Superior Tecnológico del Azuay</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Estado de conexión
    if st.session_state.api_connected:
        st.success("🟢 Conectado a la API")
    else:
        st.error("🔴 Sin conexión a la API")
        if st.button("🔄 Reconectar"):
            st.session_state.api_connected = check_api_health()
            st.rerun()
    
    st.markdown("---")
    
    # Acciones rápidas
    st.markdown("### 🚀 Acciones Rápidas")
    
    quick_actions = [
        ("🎓 Ver Carreras", "Quiero ver todas las carreras disponibles"),
        ("📋 Matrícula", "Información sobre matrícula"),
        ("📞 Contacto", "Información de contacto"),
        ("🎯 Modalidades", "Información sobre modalidades de estudio"),
        ("🕐 Horarios", "Información sobre horarios y jornadas"),
        ("💰 Costos", "Información sobre costos")
    ]
    
    for label, message in quick_actions:
        if st.button(label, key=f"quick_{label}", use_container_width=True):
            if st.session_state.api_connected:
                st.session_state.messages.append({"role": "user", "content": message, "timestamp": datetime.now()})
                st.rerun()
    
    st.markdown("---")
    
    # Información de contacto
    st.markdown("""
    <div class="contact-info">
        <h3>📞 Contacto</h3>
        <p><strong>Teléfono:</strong><br>+593 99 536 3076</p>
        <p><strong>Email:</strong><br>secretaria@tecazuay.edu.ec</p>
        <p><strong>Ubicación:</strong><br>Parque Industrial<br>Cuenca, Ecuador</p>
        <p><strong>Web:</strong><br>tecazuay.edu.ec</p>
        <p><strong>Redes:</strong><br>@tecdelazuay</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Limpiar conversación
    if st.button("🗑️ Limpiar Conversación", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = None
        st.rerun()

# --- Main Chat Interface ---
st.markdown('<div class="chat-main-container">', unsafe_allow_html=True)

# Área de conversación
st.markdown("""
<div class="chat-conversation-area">
    <div class="chat-header">
        💬 Conversación con el Asistente ISTA
    </div>
    <div class="chat-messages-container" id="chat-messages">
""", unsafe_allow_html=True)

# Mostrar mensajes
if not st.session_state.messages:
    st.markdown("""
    <div class="bot-message fade-in-up">
        ¡Hola! 👋 Soy tu asistente virtual del ISTA.<br><br>
        Puedo ayudarte con información sobre:<br>
        • 🎓 Nuestras carreras tecnológicas<br>
        • 📋 Proceso de matrícula<br>
        • 📞 Información de contacto<br>
        • 🎯 Modalidades de estudio<br>
        • 🕐 Horarios y jornadas<br><br>
        ¿En qué puedo ayudarte hoy?
    </div>
    """, unsafe_allow_html=True)

for message in st.session_state.messages:
    timestamp = message["timestamp"].strftime("%H:%M")
    if message["role"] == "user":
        st.markdown(f"""
        <div class="user-message fade-in-up">
            {message["content"]}
            <div style="font-size: 0.8rem; opacity: 0.7; margin-top: 8px;">Tú • {timestamp}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bot-message fade-in-up">
            {message["content"]}
            <div style="font-size: 0.8rem; opacity: 0.7; margin-top: 8px;">Asistente ISTA • {timestamp}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# Input del usuario
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input(
        "Escribe tu mensaje...",
        key="user_input",
        placeholder="Pregúntame sobre carreras, matrícula, horarios, etc.",
        label_visibility="collapsed"
    )

with col2:
    send_button = st.button("📤 Enviar", use_container_width=True)

# Procesar mensaje
if (send_button or user_input) and user_input.strip():
    if st.session_state.api_connected:
        # Agregar mensaje del usuario
        st.session_state.messages.append({
            "role": "user", 
            "content": user_input, 
            "timestamp": datetime.now()
        })
        
        # Enviar a la API
        with st.spinner("🤔 Pensando..."):
            response = send_message_to_api(user_input, st.session_state.session_id)
        
        if response.get("success"):
            # Actualizar session_id si es nuevo
            if response.get("session_id") and not st.session_state.session_id:
                st.session_state.session_id = response["session_id"]
            
            # Agregar respuesta del bot
            st.session_state.messages.append({
                "role": "assistant",
                "content": response["bot_response"],
                "timestamp": datetime.now()
            })
        else:
            # Error en la API
            error_msg = response.get("error", "Error desconocido")
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Lo siento, ha ocurrido un error: {error_msg}. Por favor, intenta más tarde.",
                "timestamp": datetime.now()
            })
        
        st.rerun()
    else:
        st.error("❌ No hay conexión con la API. Por favor, verifica la conexión.")

st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: var(--text-dark); opacity: 0.8;">
    <p>© 2024 Instituto Tecnológico del Azuay - Chatbot Inteligente</p>
    <p>Desarrollado con ❤️ para la comunidad educativa</p>
</div>
""", unsafe_allow_html=True)

# --- Auto-scroll JavaScript ---
st.markdown("""
<script>
function scrollToBottom() {
    var chatContainer = document.getElementById('chat-messages');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}
setTimeout(scrollToBottom, 100);
</script>
""", unsafe_allow_html=True)

