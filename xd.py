import streamlit as st
import requests
import os
import time
import re

# Configuración de la página
st.set_page_config(
    page_title="Chatbot ISTA - Instituto Tecnológico del Azuay",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL de la API
API_BASE_URL = os.getenv('API_BASE_URL', 'https://nghki1cldwq3.manussite.space')

# CSS personalizado para mejorar la apariencia
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #035AA6 0%, #F2B705 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border-left: 4px solid #035AA6;
        background-color: #f8f9fa;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
        text-align: right;
    }
    
    .bot-message {
        background-color: #f1f8e9;
        border-left-color: #4caf50;
        position: relative;
    }
    
    /* Estilos mejorados para las respuestas del bot */
    .bot-response-container {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        color: #333;
    }
    
    .bot-bold {
        font-weight: 700;
        color: #035AA6;
        font-size: 1.05em;
    }
    
    .bot-section-title {
        background: linear-gradient(135deg, #1976D2, #2196F3);
        color: #FFFFFF !important;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        margin: 1rem 0 0.5rem 0;
        font-weight: bold;
        font-size: 1.1em;
        box-shadow: 0 2px 4px rgba(3, 90, 166, 0.2);
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
        border: 2px solid #0D47A1;
    }
    
    .bot-section-title * {
        color: #FFFFFF !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
        font-weight: bold !important;
    }
    
    .bot-list-item {
        padding: 0.4rem 0.8rem;
        margin: 0.3rem 0;
        border-radius: 6px;
        background-color: #f8f9fa;
        border-left: 3px solid #F2B705;
        transition: all 0.2s ease;
    }
    
    .bot-list-item:hover {
        background-color: #e9ecef;
        transform: translateX(2px);
    }
    
    .bot-list-item.numbered {
        background-color: #fff3cd;
        border-left-color: #ffc107;
        font-weight: 500;
    }
    
    .bot-list-item.bullet {
        background-color: #d1ecf1;
        border-left-color: #17a2b8;
    }
    
    .bot-info-item {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        color: #212529 !important;
        padding: 0.6rem 1rem;
        margin: 0.4rem 0;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        font-weight: 500;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .bot-info-item * {
        color: #212529 !important;
    }
    
    .bot-text {
        padding: 0.3rem 0;
        margin: 0.2rem 0;
        line-height: 1.7;
    }
    
    .bot-separator {
        height: 2px;
        background: linear-gradient(90deg, #035AA6, #F2B705, #035AA6);
        margin: 1.5rem 0;
        border-radius: 1px;
        opacity: 0.6;
    }
    
    /* Animaciones sutiles */
    .bot-response-container {
        animation: fadeInUp 0.3s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .quick-action-btn {
        background-color: #035AA6;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin: 0.2rem;
        cursor: pointer;
        width: 100%;
        text-align: left;
    }
    
    .quick-action-btn:hover {
        background-color: #F2B705;
        color: #035AA6;
    }
    
    .status-indicator {
        padding: 0.5rem;
        border-radius: 5px;
        margin-bottom: 1rem;
        text-align: center;
        font-weight: bold;
    }
    
    .status-connected {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .status-disconnected {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    .form-container {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #035AA6;
        margin: 1rem 0;
    }
    
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Funciones auxiliares
def check_api_connection():
    """Verifica la conexión con la API"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def send_message_to_api(message):
    """Envía un mensaje a la API del chatbot"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/chat/message",
            json={"message": message},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            # Corregir: usar 'bot_response' en lugar de 'response'
            return data.get('bot_response', 'Error: No se recibió respuesta')
        else:
            return "Error: No se pudo procesar tu mensaje. Intenta de nuevo."
    except requests.exceptions.Timeout:
        return "Error: La conexión tardó demasiado. Verifica tu conexión a internet."
    except Exception as e:
        return f"Error: No se pudo conectar con el servidor. Detalles: {str(e)}"

def get_carreras_for_form():
    """Obtiene la lista de carreras para el formulario"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/matricula/carreras", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return data.get('carreras', [])
        return []
    except:
        return []

def submit_matricula_form(form_data):
    """Envía el formulario de matrícula"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/matricula/submit",
            json=form_data,
            timeout=10
        )
        return response.json()
    except:
        return {'success': False, 'message': 'Error de conexión'}

def get_quick_action_message(user_input):
    """Mapea números a mensajes de opciones rápidas"""
    # Diccionario de mapeo de números a mensajes
    number_to_message = {
        "1": "Quiero ver todas las carreras disponibles",
        "2": "Necesito la información de contacto del ISTA",
        "3": "¿Cómo es el proceso de matrícula?",
        "4": "¿Qué modalidades de estudio ofrecen?",
        "5": "¿Cuáles son los horarios y jornadas?",
        "6": "¿Cuánto cuestan las carreras?",
        "7": "Quiero llenar el formulario de matrícula"
    }
    
    # Limpiar la entrada del usuario
    clean_input = user_input.strip()
    
    # Verificar si es un número del 1 al 7
    if clean_input in number_to_message:
        return number_to_message[clean_input]
    
    # Si no es un número válido, devolver la entrada original
    return user_input

def format_bot_response(response):
    """Formatea la respuesta del bot para mostrar mejor en Streamlit"""
    
    # Aplicar formato mejorado con HTML y CSS
    formatted_response = response
    
    # Convertir **texto** a HTML bold con estilo personalizado
    formatted_response = re.sub(r'\*\*(.*?)\*\*', r'<span class="bot-bold">\1</span>', formatted_response)
    
    # Mejorar la estructura de listas con viñetas
    lines = formatted_response.split('\n')
    formatted_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            formatted_lines.append('<br>')
            continue
            
        # Detectar títulos principales (líneas que empiezan con emoji y mayúsculas)
        if re.match(r'^[🎓📋📞🎯🕐💰📝🏛️].*[A-Z].*:?\s*$', line):
            formatted_lines.append(f'<div class="bot-section-title">{line}</div>')
        
        # Detectar elementos de lista numerados
        elif re.match(r'^\d+\.\s+', line):
            formatted_lines.append(f'<div class="bot-list-item numbered">{line}</div>')
        
        # Detectar elementos de lista con viñetas
        elif re.match(r'^[•\-\*]\s+', line):
            formatted_lines.append(f'<div class="bot-list-item bullet">{line}</div>')
        
        # Detectar separadores
        elif line.strip() == '---':
            formatted_lines.append('<div class="bot-separator"></div>')
        
        # Detectar información de contacto o datos importantes
        elif ':' in line and any(keyword in line.lower() for keyword in ['teléfono', 'email', 'ubicación', 'web', 'duración', 'jornada', 'modalidad']):
            formatted_lines.append(f'<div class="bot-info-item">{line}</div>')
        
        # Texto normal
        else:
            formatted_lines.append(f'<div class="bot-text">{line}</div>')
    
    formatted_response = ''.join(formatted_lines)
    
    # Añadir contenedor principal
    formatted_response = f'<div class="bot-response-container">{formatted_response}</div>'
    
    return formatted_response

# Inicialización del estado de la sesión
if 'messages' not in st.session_state:
    st.session_state.messages = []
    # Añadir mensaje de bienvenida automático
    welcome_message = """¡Hola! 👋 **Bienvenido al ISTA**

🏛️ **Instituto Superior Tecnológico del Azuay**

Soy tu asistente virtual y puedo ayudarte con:

**1️⃣ 🎓 Carreras tecnológicas** - Ver todas las opciones disponibles
**2️⃣ 📋 Proceso de matrícula** - Requisitos y pasos a seguir
**3️⃣ 📞 Información de contacto** - Teléfonos, ubicación y horarios
**4️⃣ 🎯 Modalidades de estudio** - Presencial, dual, híbrida, en línea
**5️⃣ 🕐 Horarios y jornadas** - Matutina, vespertina, nocturna
**6️⃣ 💰 Costos** - ¡Todas nuestras carreras son gratuitas!
**7️⃣ 📝 Formulario de matrícula** - Solicita tu inscripción

---

🤔 **¿En qué puedo ayudarte hoy?**
Puedes escribir el **número** de la opción o simplemente mencionar el tema que te interesa.

Ejemplo: "1" o "carreras" o "quiero ver las carreras" """
    
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})

if 'api_connected' not in st.session_state:
    st.session_state.api_connected = check_api_connection()
if 'show_form' not in st.session_state:
    st.session_state.show_form = False
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🎓 Chatbot ISTA</h1>
    <h3>Instituto Superior Tecnológico del Azuay</h3>
    <p>Tu asistente virtual para información académica</p>
</div>
""", unsafe_allow_html=True)

# Layout principal con columnas
col1, col2 = st.columns([2, 1])

with col1:
    # Indicador de estado de conexión
    if st.session_state.api_connected:
        st.markdown("""
        <div class="status-indicator status-connected">
            ✅ Conectado al servidor - Listo para chatear
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-indicator status-disconnected">
            ❌ Sin conexión al servidor - Verifica tu internet
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Reconectar"):
            st.session_state.api_connected = check_api_connection()
            st.rerun()

    # Mostrar formulario de matrícula si está activado
    if st.session_state.show_form and not st.session_state.form_submitted:
        st.markdown("### 📝 Formulario de Matrícula")
        
        with st.form("matricula_form"):
            st.markdown("""
            <div class="form-container">
                <h4>🎓 Solicitud de Matrícula - ISTA</h4>
                <p>Completa todos los campos para procesar tu solicitud de matrícula.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Campos del formulario
            nombre_completo = st.text_input("👤 Nombre Completo *", placeholder="Ej: Juan Carlos Pérez López")
            cedula = st.text_input("🆔 Cédula de Identidad *", placeholder="Ej: 0123456789")
            email = st.text_input("📧 Correo Electrónico *", placeholder="Ej: juan.perez@email.com")
            telefono = st.text_input("📞 Teléfono *", placeholder="Ej: +593 99 123 4567")
            
            # Obtener carreras para el select
            carreras = get_carreras_for_form()
            if carreras:
                carrera_options = [f"{carrera['nombre']} ({carrera['modalidad']})" for carrera in carreras]
                carrera_interes = st.selectbox("🎯 Carrera de Interés *", carrera_options)
            else:
                carrera_interes = st.text_input("🎯 Carrera de Interés *", placeholder="Escribe la carrera que te interesa")
            
            # Campos adicionales
            col_form1, col_form2 = st.columns(2)
            with col_form1:
                fecha_nacimiento = st.date_input("📅 Fecha de Nacimiento")
                genero = st.selectbox("👥 Género", ["Masculino", "Femenino", "Otro", "Prefiero no decir"])
            
            with col_form2:
                ciudad = st.text_input("🏙️ Ciudad de Residencia", placeholder="Ej: Cuenca")
                nivel_educacion = st.selectbox("🎓 Nivel de Educación", 
                    ["Bachiller", "Técnico", "Tecnólogo", "Universitario", "Otro"])
            
            # Información adicional
            st.text_area("💬 Comentarios Adicionales (Opcional)", 
                        placeholder="Cualquier información adicional que consideres importante...")
            
            # Términos y condiciones
            acepta_terminos = st.checkbox("✅ Acepto los términos y condiciones del ISTA")
            
            # Botón de envío
            submitted = st.form_submit_button("🚀 Enviar Solicitud de Matrícula", 
                                            disabled=not acepta_terminos)
            
            if submitted:
                # Validar campos requeridos
                if not all([nombre_completo, cedula, email, telefono, carrera_interes]):
                    st.markdown("""
                    <div class="error-message">
                        ❌ Por favor completa todos los campos marcados con *
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Preparar datos del formulario
                    form_data = {
                        'nombre_completo': nombre_completo,
                        'cedula': cedula,
                        'email': email,
                        'telefono': telefono,
                        'carrera_interes': carrera_interes,
                        'fecha_nacimiento': str(fecha_nacimiento),
                        'genero': genero,
                        'ciudad': ciudad,
                        'nivel_educacion': nivel_educacion
                    }
                    
                    # Enviar formulario
                    result = submit_matricula_form(form_data)
                    
                    if result.get('success'):
                        st.session_state.form_submitted = True
                        st.session_state.form_result = result
                        st.rerun()
                    else:
                        st.markdown(f"""
                        <div class="error-message">
                            ❌ Error: {result.get('message', 'No se pudo enviar el formulario')}
                        </div>
                        """, unsafe_allow_html=True)

    # Mostrar resultado del formulario si fue enviado
    if st.session_state.form_submitted and 'form_result' in st.session_state:
        result = st.session_state.form_result
        st.markdown(f"""
        <div class="success-message">
            <h4>🎉 ¡Formulario Enviado Exitosamente!</h4>
            <p><strong>Nombre:</strong> {result['data']['nombre']}</p>
            <p><strong>Carrera:</strong> {result['data']['carrera']}</p>
            <p><strong>Número de Solicitud:</strong> {result['data']['numero_solicitud']}</p>
            <p>📞 Te contactaremos pronto al número proporcionado.</p>
            <p>✉️ También recibirás un correo de confirmación.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Enviar Otro Formulario"):
            st.session_state.form_submitted = False
            st.session_state.show_form = False
            del st.session_state.form_result
            st.rerun()

    # Área de chat
    st.markdown("### 💬 Chat con el Asistente Virtual")
    
    # Contenedor para mensajes
    chat_container = st.container()
    
    with chat_container:
        # Mostrar historial de mensajes
        for i, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 Tú:</strong><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                formatted_response = format_bot_response(message["content"])
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>🤖 Asistente ISTA:</strong><br>
                    {formatted_response}
                </div>
                """, unsafe_allow_html=True)

    # Input para nuevos mensajes
    if st.session_state.api_connected:
        with st.form("chat_form", clear_on_submit=True):
            col_input, col_send = st.columns([4, 1])
            
            with col_input:
                user_input = st.text_input("💭 Escribe tu mensaje...", 
                                         placeholder="Ej: Quiero información sobre las carreras",
                                         label_visibility="collapsed")
            
            with col_send:
                send_button = st.form_submit_button("📤 Enviar", use_container_width=True)
            
            if send_button and user_input:
                # Convertir números a mensajes de opciones rápidas
                processed_message = get_quick_action_message(user_input)
                
                # Agregar mensaje del usuario (mostrar el input original)
                st.session_state.messages.append({"role": "user", "content": processed_message})
                
                # Verificar si el usuario quiere el formulario
                if any(keyword in processed_message.lower() for keyword in 
                       ["formulario", "matricula", "matrícula", "inscripción", "inscripcion"]):
                    st.session_state.show_form = True
                
                # Obtener respuesta del bot usando el mensaje procesado
                with st.spinner("🤖 Procesando tu mensaje..."):
                    bot_response = send_message_to_api(processed_message)
                
                # Agregar respuesta del bot
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                
                st.rerun()

with col2:
    # Sidebar con opciones rápidas
    st.markdown("### 🚀 Opciones Rápidas")
    st.markdown("*Haz clic en cualquier opción para enviar la pregunta automáticamente*")
    
    # Opciones rápidas numeradas
    quick_actions = [
        ("1️⃣ 🎓 Ver todas las carreras", "Quiero ver todas las carreras disponibles"),
        ("2️⃣ 📞 Información de contacto", "Necesito la información de contacto del ISTA"),
        ("3️⃣ 📋 Proceso de matrícula", "¿Cómo es el proceso de matrícula?"),
        ("4️⃣ 🎯 Modalidades de estudio", "¿Qué modalidades de estudio ofrecen?"),
        ("5️⃣ 🕐 Horarios y jornadas", "¿Cuáles son los horarios y jornadas?"),
        ("6️⃣ 💰 Información de costos", "¿Cuánto cuestan las carreras?"),
        ("7️⃣ 📝 Formulario de matrícula", "Quiero llenar el formulario de matrícula")
    ]
    
    for button_text, message in quick_actions:
        if st.button(button_text, key=f"quick_{message}", use_container_width=True):
            if st.session_state.api_connected:
                # Agregar mensaje del usuario
                st.session_state.messages.append({"role": "user", "content": message})
                
                # Verificar si es el formulario
                if "formulario" in message.lower():
                    st.session_state.show_form = True
                
                # Obtener respuesta del bot
                with st.spinner("🤖 Procesando..."):
                    bot_response = send_message_to_api(message)
                
                # Agregar respuesta del bot
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                
                st.rerun()
            else:
                st.error("❌ Sin conexión al servidor")

    # Información adicional
    st.markdown("---")
    st.markdown("### 📍 Información de Contacto")
    st.markdown("""
    **🏛️ Instituto Superior Tecnológico del Azuay**
    
    📍 **Ubicación:** Parque Industrial, Cuenca
    
    📞 **Teléfono:** +593 99 536 3076
    
    ✉️ **Email:** secretaria@tecazuay.edu.ec
    
    🌐 **Web:** tecazuay.edu.ec
    
    📱 **Redes:** @tecdelazuay
    """)
    
    st.markdown("---")
    st.markdown("### 🕐 Horarios de Atención")
    st.markdown("""
    **Lunes a Viernes:** 8:00 AM - 5:00 PM
    
    **Sábados:** 8:00 AM - 12:00 PM
    
    **Domingos:** Cerrado
    """)
    
    # Botón para limpiar chat
    if st.button("🗑️ Limpiar Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.show_form = False
        st.session_state.form_submitted = False
        if 'form_result' in st.session_state:
            del st.session_state.form_result
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🎓 <strong>Instituto Superior Tecnológico del Azuay (ISTA)</strong></p>
    <p>Educación tecnológica de calidad • Títulos reconocidos por SENESCYT • 100% Gratuito</p>
    <p><em>Desarrollado con ❤️ para la comunidad estudiantil</em></p>
</div>
""", unsafe_allow_html=True)

