# Chatbot ISTA - Frontend Streamlit

Este es el frontend del chatbot del Instituto Superior Tecnológico del Azuay (ISTA) desarrollado con Streamlit.

## Características

- ✅ Interfaz moderna con colores institucionales del ISTA
- ✅ Chat interactivo en tiempo real
- ✅ Acciones rápidas para consultas comunes
- ✅ Diseño responsive para móviles y escritorio
- ✅ Conexión con API backend independiente
- ✅ Manejo de errores y reconexión automática

## Configuración

### Variables de Entorno

- `API_BASE_URL`: URL del backend API (por defecto: https://19hninc1mm99.manus.space)

### Instalación Local

```bash
pip install -r requirements.txt
streamlit run app_improved.py
```

### Despliegue en Streamlit Cloud

1. Subir el repositorio a GitHub
2. Conectar con Streamlit Cloud
3. Configurar la variable de entorno `API_BASE_URL`
4. Desplegar

## Estructura del Proyecto

```
chatbot-ista-streamlit/
├── app_improved.py          # Aplicación principal mejorada
├── app.py                   # Aplicación original
├── requirements.txt         # Dependencias
├── .streamlit/
│   └── config.toml         # Configuración de Streamlit
└── README.md               # Este archivo
```

## API Backend

El frontend se conecta a una API REST independiente que maneja:

- Procesamiento de mensajes del chatbot
- Base de datos de carreras del ISTA
- Lógica de respuestas inteligentes
- Manejo de sesiones

## Funcionalidades

### Chat Interactivo
- Conversación en tiempo real con el asistente virtual
- Historial de mensajes con timestamps
- Formato mejorado de respuestas

### Acciones Rápidas
- Ver Carreras
- Información de Matrícula
- Datos de Contacto
- Modalidades de Estudio
- Horarios y Jornadas
- Información de Costos

### Información Institucional
- Datos de contacto siempre visibles
- Estado de conexión con la API
- Diseño con identidad visual del ISTA

## Compatibilidad

- ✅ Streamlit Cloud
- ✅ Heroku
- ✅ Docker
- ✅ Servidores locales

## Soporte

Para soporte técnico, contactar:
- Email: secretaria@tecazuay.edu.ec
- Teléfono: +593 99 536 3076

