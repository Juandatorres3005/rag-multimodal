import os
import requests
import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title="RAG Multimodal Técnico",
    page_icon="🤖",
    layout="wide"
)

# URL del backend de FastAPI
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.title("🤖 Asistente RAG Multimodal")
st.write("Consulta y analiza documentos técnicos con extracción de contexto e imágenes.")

# Inicializar historial de chat en la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- BARRA LATERAL: CARGA DE ARCHIVOS ---
with st.sidebar:
    st.header("1. Carga de Documentos")
    uploaded_file = st.file_uploader("Sube un archivo PDF técnico", type=["pdf"])
    
    if st.button("Procesar PDF"):
        if uploaded_file is not None:
            with st.spinner("Procesando e indexando el documento..."):
                try:
                    # Enviar el archivo al backend para extracción e indexación
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    response = requests.post(f"{BACKEND_URL}/upload", files=files)
                    
                    if response.status_code == 200:
                        st.success("Documento procesado e indexado con éxito.")
                        # Limpiar el historial del chat al subir un nuevo documento
                        st.session_state.messages = []
                    else:
                        st.error(f"Error al procesar el archivo: {response.json().get('detail', response.text)}")
                except Exception as e:
                    st.error(f"No se pudo conectar con el servidor backend: {str(e)}")
        else:
            st.warning("Por favor, selecciona un archivo PDF antes de procesar.")

# --- ÁREA PRINCIPAL: CHAT DE CONSULTA ---

# 1. Renderizar historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Renderizado de imágenes/diagramas asociados
        if message.get("images"):
            st.write("**Diagramas / Imágenes relacionadas:**")
            cols = st.columns(min(len(message["images"]), 3))
            for idx, img_path in enumerate(message["images"]):
                if os.path.exists(img_path):
                    with cols[idx % 3]:
                        st.image(img_path, caption=f"Imagen ({os.path.basename(img_path)})", use_container_width=True)

        # Renderizado de metadatos/fuentes
        if message.get("sources"):
            with st.expander("Metadatos de contexto"):
                for src in message["sources"]:
                    st.caption(f"• {src}")

# 2. Input del usuario
if prompt := st.chat_input("Pregunta sobre el documento indexado (ej. ¿Qué indica el esquema eléctrico?)"):
    # Guardar y mostrar pregunta del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta del bot
    with st.chat_message("assistant"):
        with st.spinner("Buscando en el documento y generando respuesta..."):
            try:
                # Consulta al backend
                response = requests.post(
                    f"{BACKEND_URL}/query",
                    json={"question": prompt}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No se recibió respuesta.")
                    sources = data.get("sources", [])
                    images = data.get("images", [])

                    # Mostrar texto de la respuesta
                    st.markdown(answer)

                    # Mostrar imágenes recuperadas si existen
                    if images:
                        st.write("**Diagramas / Imágenes relacionadas:**")
                        cols = st.columns(min(len(images), 3))
                        for idx, img_path in enumerate(images):
                            if os.path.exists(img_path):
                                with cols[idx % 3]:
                                    st.image(img_path, caption=f"Imagen ({os.path.basename(img_path)})", use_container_width=True)

                    # Mostrar metadatos de fuentes
                    if sources:
                        with st.expander("Metadatos de contexto"):
                            for src in sources:
                                st.caption(f"• {src}")

                    # Guardar respuesta completa en el historial de sesión
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                        "images": images
                    })
                else:
                    error_msg = f"Error del servidor backend: {response.status_code}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

            except Exception as e:
                error_msg = f"Error de conexión: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})