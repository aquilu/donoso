# Importando las librerías necesarias
import time
import streamlit as st
from utils import load_chain

# Imagen personalizada para el icono de la app y el avatar del asistente
company_logo = 'https://donosoenaccion.com/wp-content/uploads/2023/08/Logo_Donoso.png'

# Mensaje promocional para mostrar al final de cada respuesta del asistente
PROMO_MESSAGE = "No olvides visitarnos en [Donoso en Acción](https://donosoenaccion.com/)"


# Configurando la página de Streamlit
st.set_page_config(
    page_title="Asistente virtual sobre Leonardo Donoso y su programa de gobierno",
    page_icon=company_logo
)

def check_for_keywords(query):
    # Si la palabra clave 'inseguridad' está en la consulta, proporciona una respuesta personalizada
    if 'inseguridad' in query.lower():
        return """La seguridad es fundamental para el desarrollo y bienestar en nuestro municipio.
Reconociendo la necesidad de brindar tranquilidad y protección a nuestros
ciudadanos, fortaleceremos y modernizaremos las capacidades operativas de
nuestras fuerzas de seguridad locales. Trabajaremos incansablemente para hacer de Chía un ejemplo de seguridad y
convivencia ciudadana."""
    # Si no hay una palabra clave reconocida, retorna None
    return None

# Inicializando la cadena LLM
chain = load_chain()

# Inicializando el historial del chat
if 'messages' not in st.session_state:
    st.session_state['messages'] = [{"role": "assistant", 
                                  "content": "¡Hola! Soy Donoso en Acción, la IA que te asiste sobre el candidato Leonardo Donoso y su programa de gobierno. ¿Cómo puedo ayudarte hoy?"}]

# Mostrando mensajes del chat desde el historial
for message in st.session_state.messages:
    if message["role"] == 'assistant':
        with st.chat_message(message["role"], avatar=company_logo):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Lógica del chat
if query := st.chat_input("Pregúntame sobre el programa de gobierno del candidato Leonardo Donoso:"):
    st.session_state.messages.append({"role": "user", "content": query})

    # Verificar si la consulta contiene alguna palabra clave
    custom_response = check_for_keywords(query)

    # Si hay una respuesta personalizada, úsala
    if custom_response:
        response = custom_response
    else:
           with st.spinner('Donoso IA está pensando...'):  # Indicador de que el asistente está "pensando"
               # De lo contrario, enviar la pregunta del usuario a nuestra cadena
               result = chain({"question": query})
               response = result['answer']

    # Añadir el mensaje promocional a la respuesta
    full_response = f"{response}\n\n---\n{PROMO_MESSAGE}"

    with st.chat_message("assistant", avatar=company_logo):
        st.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})