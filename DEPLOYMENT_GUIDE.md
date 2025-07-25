# 🚀 Guía de Despliegue en Streamlit Cloud

## Pasos para Desplegar el Chatbot ISTA

### 1. Preparar el Repositorio en GitHub

1. **Crear un nuevo repositorio en GitHub:**
   - Ve a https://github.com/new
   - Nombre: `chatbot-ista-streamlit`
   - Descripción: `Chatbot del Instituto Superior Tecnológico del Azuay`
   - Público o Privado (tu elección)
   - ✅ Crear repositorio

2. **Subir los archivos:**
   ```bash
   git clone https://github.com/TU-USUARIO/chatbot-ista-streamlit.git
   cd chatbot-ista-streamlit
   
   # Copiar todos los archivos de este proyecto EXCEPTO .streamlit/secrets.toml
   # Los archivos necesarios son:
   # - streamlit_app.py (archivo principal)
   # - requirements.txt
   # - .streamlit/config.toml
   # - .gitignore
   # - README.md
   
   git add .
   git commit -m "Initial commit: Chatbot ISTA"
   git push origin main
   ```

### 2. Desplegar en Streamlit Cloud

1. **Ir a Streamlit Cloud:**
   - Visita: https://share.streamlit.io/
   - Inicia sesión con tu cuenta de GitHub

2. **Crear nueva aplicación:**
   - Clic en "New app"
   - Repository: `TU-USUARIO/chatbot-ista-streamlit`
   - Branch: `main`
   - Main file path: `streamlit_app.py`

3. **Configurar Advanced Settings:**
   - Clic en "Advanced settings..."
   - En la sección "Secrets", pegar:
   ```toml
   [general]
   API_BASE_URL = "https://19hninc1mm99.manus.space"
   ```

4. **Desplegar:**
   - Clic en "Deploy!"
   - Esperar 2-3 minutos

### 3. Verificar el Despliegue

✅ **La aplicación debería estar disponible en una URL como:**
`https://TU-USUARIO-chatbot-ista-streamlit-streamlit-app-XXXXX.streamlit.app/`

✅ **Verificar que funciona:**
- El chatbot responde a mensajes
- Las acciones rápidas funcionan
- El estado de conexión muestra "Conectado"
- El diseño se ve correctamente

## Archivos Incluidos

### `streamlit_app.py` (Principal)
- Aplicación principal optimizada para Streamlit Cloud
- Manejo de secretos con `st.secrets`
- Diseño responsive con colores institucionales
- Chat funcional con historial
- Acciones rápidas en sidebar

### `requirements.txt`
```
streamlit==1.28.1
requests==2.31.0
```

### `.streamlit/config.toml`
- Configuración de tema con colores del ISTA
- Configuración de servidor para producción

### `.gitignore`
- Excluye archivos sensibles como `secrets.toml`
- Configurado para proyectos Python/Streamlit

## Variables de Entorno

### En Streamlit Cloud (Secrets):
```toml
[general]
API_BASE_URL = "https://19hninc1mm99.manus.space"
```

### Para desarrollo local:
Crear `.streamlit/secrets.toml`:
```toml
[general]
API_BASE_URL = "https://19hninc1mm99.manus.space"
```

## Características Implementadas

### ✅ Chat Funcional
- Historial de mensajes con timestamps
- Respuestas en tiempo real desde la API
- Manejo de errores de conexión
- Indicador de estado de carga

### ✅ Diseño Institucional
- Colores oficiales del ISTA (Azul #035AA6, Amarillo #F2B705)
- Logo y branding institucional
- Diseño responsive para móviles
- Interfaz moderna y profesional

### ✅ Funcionalidades Avanzadas
- Acciones rápidas para consultas comunes
- Estado de conexión con la API en tiempo real
- Botón de reconexión manual
- Limpieza de conversación
- Información de contacto siempre visible

### ✅ Optimizaciones para Producción
- Manejo robusto de errores
- Timeouts configurados
- Validación de entrada
- Compatibilidad total con Streamlit Cloud

## Mantenimiento

### Actualizar la Aplicación:
1. Hacer cambios en el código local
2. Commit y push a GitHub
3. Streamlit Cloud redespliega automáticamente

### Actualizar Secretos:
1. Ir a la configuración de la app en Streamlit Cloud
2. Editar la sección "Secrets"
3. Guardar cambios

### Monitoreo:
- Logs disponibles en el dashboard de Streamlit Cloud
- Métricas de uso y rendimiento incluidas

## Soporte

### Documentación:
- Streamlit: https://docs.streamlit.io/
- Streamlit Cloud: https://docs.streamlit.io/streamlit-community-cloud

### Contacto ISTA:
- Email: secretaria@tecazuay.edu.ec
- Teléfono: +593 99 536 3076

---

## ✅ Checklist de Despliegue

- [ ] Repositorio creado en GitHub
- [ ] Archivos subidos (sin secrets.toml)
- [ ] Aplicación creada en Streamlit Cloud
- [ ] Secretos configurados
- [ ] Despliegue exitoso
- [ ] Pruebas de funcionalidad completadas
- [ ] URL final documentada

**¡Tu chatbot estará listo para usar en producción!** 🎉

