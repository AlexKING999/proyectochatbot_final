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
API_BASE_URL = os.getenv('API_BASE_URL', 'https://19hninc1mm99.manus.space')

# --- Custom CSS (Improved Design) ---
st.markdown("""
<style>
    /* Colores institucionales */
    :root {
        --primary-blue: #035AA6;
        --secondary-blue: #033F73;
        --accent-yellow: #F2B705;
        --bright-yellow: #D9A404;
        --light-bg: #f8fafc;
        --white: #ffffff;
        --text-dark: #1e293b;
        --border-light: #e2e8f0;
    }

    /* Fondo principal */
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
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 8px 30px rgba(3, 90, 166, 0.4);
        border: 2px solid var(--accent-yellow);
    }
    
    .main-header h1 {
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 10px;
        font-size: 2.2rem;
        font-weight: 700;
    }
    
    /* Contenedor del chat */
    .chat-container {
        background: var(--white);
        border-radius: 15px;
        border: 2px solid var(--accent-yellow);
        box-shadow: 0 10px 30px rgba(3, 90, 166, 0.25);
        margin-bottom: 20px;
        overflow: hidden;
        min-height: 500px;
    }
    
    .chat-header {
        background: linear-gradient(90deg, var(--primary-blue) 0%, var(--accent-yellow) 100%);
        color: white;
        padding: 15px 25px;
        font-weight: bold;
        font-size: 1.1rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    .chat-messages {
        padding: 20px;
        background: var(--light-bg);
        min-height: 400px;
        max-height: 500px;
        overflow-y: auto;
    }
    
    /* Mensajes del chat */
    .user-message {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 5px 18px;
        margin: 8px 0 8px 40px;
        box-shadow: 0 3px 12px rgba(3, 90, 166, 0.3);
        border: 1px solid var(--accent-yellow);
        position: relative;
        word-wrap: break-word;
    }
    
    .user-message::before {
        content: "👤";
        position: absolute;
        left: -30px;
        top: 50%;
        transform: translateY(-50%);
        background: var(--accent-yellow);
        border-radius: 50%;
        width: 25px;
        height: 25px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        border: 1px solid var(--primary-blue);
    }
    
    .bot-message {
        background: linear-gradient(135deg, var(--white) 0%, #f8fafc 100%);
        color: var(--text-dark);
        padding: 12px 18px;
        border-radius: 18px 18px 18px 5px;
        margin: 8px 40px 8px 0;
        box-shadow: 0 3px 12px rgba(3, 90, 166, 0.2);
        border: 1px solid var(--primary-blue);
        position: relative;
        word-wrap: break-word;
        line-height: 1.5;
    }
    
    .bot-message::before {
        content: "🤖";
        position: absolute;
        right: -30px;
        top: 50%;
        transform: translateY(-50%);
        background: var(--primary-blue);
        border-radius: 50%;
        width: 25px;
        height: 25px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        border: 1px solid var(--accent-yellow);
    }
    
    /* Sidebar mejorado */
    .sidebar-header {
        text-align: center;
        padding: 20px;
        margin-bottom: 20px;
        background: linear-gradient(135deg, var(--white) 0%, #f8fafc 100%);
        border-radius: 15px;
        box-shadow: 0 6px 20px rgba(3, 90, 166, 0.2);
        border: 2px solid var(--accent-yellow);
    }
    
    /* Botones de acción rápida */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-yellow) 0%, var(--bright-yellow) 100%);
        color: var(--text-dark);
        border: 1px solid var(--primary-blue);
        border-radius: 12px;
        padding: 10px 16px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 3px 12px rgba(242, 183, 5, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(242, 183, 5, 0.4);
        background: linear-gradient(135deg, var(--bright-yellow) 0%, var(--accent-yellow) 100%);
    }
    
    /* Input del chat */
    .stTextInput > div > div > input {
        border: 2px solid var(--primary-blue);
        border-radius: 12px;
        padding: 12px;
        font-size: 16px;
        background: var(--white);
        color: var(--text-dark);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-yellow);
        box-shadow: 0 0 0 2px rgba(242, 183, 5, 0.2);
    }
    
    /* Información de contacto */
    .contact-info {
        background: linear-gradient(135deg, var(--white) 0%, #f8fafc 100%);
        border: 2px solid var(--primary-blue);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 6px 20px rgba(3, 90, 166, 0.2);
    }
    
    .contact-info h3 {
        color: var(--primary-blue);
        border-bottom: 2px solid var(--accent-yellow);
        padding-bottom: 8px;
        margin-bottom: 12px;
    }
    
    /* Estado de conexión */
    .connection-status {
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 15px;
        text-align: center;
        font-weight: bold;
    }
    
    .connected {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .disconnected {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .user-message, .bot-message {
            margin-left: 15px;
            margin-right: 15px;
        }
        
        .user-message::before, .bot-message::before {
            display: none;
        }
    }
    
    /* Animaciones */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# --- API Functions ---
def check_api_health():
    """Verificar el estado de la API"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=5)
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
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
            timeout=15
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "error": f"Error HTTP {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def format_bot_response(response_text):
    """Formatear la respuesta del bot para mejor visualización"""
    # Convertir markdown básico a HTML
    response_text = response_text.replace("**", "")  # Remover markdown bold
    response_text = response_text.replace("*", "")   # Remover markdown italic
    
    # Mejorar formato de listas
    lines = response_text.split('\n')
    formatted_lines = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('•'):
            formatted_lines.append(f"  {line}")
        elif line.startswith('✅'):
            formatted_lines.append(f"  {line}")
        elif line.startswith('📌') or line.startswith('📋') or line.startswith('🎓'):
            formatted_lines.append(f"<strong>{line}</strong>")
        else:
            formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)

# --- Initialize Session State ---
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'api_connected' not in st.session_state:
    st.session_state.api_connected = check_api_health()

# --- Header ---
st.markdown("""
<div class="main-header fade-in">
    <h1>🎓 Chatbot ISTA</h1>
    <p style="font-size: 1.1rem; margin: 0;">Instituto Superior Tecnológico del Azuay</p>
    <p style="font-size: 0.9rem; margin-top: 8px; opacity: 0.9;">Tu asistente virtual para información académica</p>
</div>
""", unsafe_allow_html=True)

# --- Layout Principal ---
col1, col2 = st.columns([3, 1])

with col1:
    # Área de conversación
    st.markdown("""
    <div class="chat-container fade-in">
        <div class="chat-header">
            💬 Conversación con el Asistente ISTA
        </div>
        <div class="chat-messages" id="chat-messages">
    """, unsafe_allow_html=True)
    
    # Mostrar mensajes
    if not st.session_state.messages:
        st.markdown("""
        <div class="bot-message fade-in">
            ¡Hola! 👋 Soy tu asistente virtual del ISTA.<br><br>
            Puedo ayudarte con información sobre:<br>
            🎓 Nuestras carreras tecnológicas<br>
            📋 Proceso de matrícula<br>
            📞 Información de contacto<br>
            🎯 Modalidades de estudio<br>
            🕐 Horarios y jornadas<br><br>
            ¿En qué puedo ayudarte hoy?
        </div>
        """, unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        timestamp = message["timestamp"].strftime("%H:%M")
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message fade-in">
                {message["content"]}
                <div style="font-size: 0.75rem; opacity: 0.7; margin-top: 6px;">Tú • {timestamp}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            formatted_content = format_bot_response(message["content"])
            st.markdown(f"""
            <div class="bot-message fade-in">
                {formatted_content}
                <div style="font-size: 0.75rem; opacity: 0.7; margin-top: 6px;">Asistente ISTA • {timestamp}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Input del usuario
    col_input, col_send = st.columns([4, 1])
    
    with col_input:
        user_input = st.text_input(
            "Escribe tu mensaje...",
            key="user_input",
            placeholder="Pregúntame sobre carreras, matrícula, horarios, etc.",
            label_visibility="collapsed"
        )
    
    with col_send:
        send_button = st.button("📤 Enviar", use_container_width=True)

with col2:
    # Sidebar
    st.markdown("""
    <div class="sidebar-header fade-in">
        <h2 style="color: var(--primary-blue); margin-bottom: 15px;">🏛️ ISTA</h2>
        <p style="color: var(--text-dark); font-weight: 500;">Instituto Superior Tecnológico del Azuay</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Estado de conexión
    if st.session_state.api_connected:
        st.markdown("""
        <div class="connection-status connected">
            🟢 Conectado a la API
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="connection-status disconnected">
            🔴 Sin conexión a la API
        </div>
        """, unsafe_allow_html=True)
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
                st.session_state.messages.append({
                    "role": "user", 
                    "content": message, 
                    "timestamp": datetime.now()
                })
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

# --- Procesar mensaje ---
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

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 15px; color: var(--text-dark); opacity: 0.8;">
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

