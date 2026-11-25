import streamlit as st
from motor import MotorFAQ, VERSION_MOTOR

st.set_page_config(page_title='SafeBot-EPP', page_icon='🦺', layout='centered')
st.title('🦺 SafeBot-EPP')
st.caption('Asistente académico sobre equipos de protección personal en entrenamiento industrial')
st.info('Prototipo educativo basado en preguntas frecuentes. No sustituye una evaluación de seguridad ni verifica el uso correcto de EPP.')

# Sin cache del motor para evitar conservar una versión antigua de preguntas.csv.
motor = MotorFAQ('preguntas.csv')
with st.sidebar:
    st.subheader('Temas disponibles')
    st.write('Casco · Guantes · Bata · Protección · Inspección · IA y EPP')
    st.caption(f'Versión del motor: {VERSION_MOTOR} · Base: {len(motor.datos)} preguntas')
    st.write('**Preguntas de ejemplo:**')
    st.write('¿Qué es un EPP?')
    st.write('¿Para qué sirve el casco?')
    st.write('¿Qué significa un falso positivo?')
    mostrar = st.checkbox('Mostrar similitud técnica', value=False)
    if st.button('Limpiar conversación'):
        st.session_state.mensajes = []
        st.rerun()

if 'mensajes' not in st.session_state:
    st.session_state.mensajes = []

for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje['rol']):
        st.markdown(mensaje['texto'])

pregunta = st.chat_input('Escribe una pregunta sobre EPP...')
if pregunta:
    st.session_state.mensajes.append({'rol': 'user', 'texto': pregunta})
    with st.chat_message('user'):
        st.markdown(pregunta)
    resultado = motor.responder(pregunta)
    texto = resultado['respuesta']
    if resultado['fuente']:
        texto += '\n\n**Fuente de referencia:** ' + resultado['fuente']
    if mostrar:
        texto += f"\n\n*Similitud TF-IDF (no es una probabilidad): {resultado['confianza']:.3f}*"
    with st.chat_message('assistant'):
        st.markdown(texto)
    st.session_state.mensajes.append({'rol': 'assistant', 'texto': texto})
