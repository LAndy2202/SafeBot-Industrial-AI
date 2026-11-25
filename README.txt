SAFEBOT-EPP - TRABAJO ACADÉMICO FINAL

ARCHIVOS
app.py: interfaz Streamlit
motor.py: motor de recuperación de preguntas con TF-IDF y similitud coseno
preguntas.csv: base de conocimientos editable (preguntas, respuestas, fuentes)
pruebas.csv: plan de prueba manual para completar con resultados reales
test_automatico.py: pruebas automáticas básicas
requirements.txt: bibliotecas

EJECUCIÓN LOCAL (Windows)
1. Instalar Python 3.11 o 3.12 de python.org y marcar Add Python to PATH.
2. Extraer este ZIP en una carpeta, abrir esa carpeta y escribir cmd en la barra de direcciones del Explorador.
3. Ejecutar: py -m venv .venv
4. Ejecutar: .venv\Scripts\activate
5. Ejecutar: python -m pip install -r requirements.txt
6. Ejecutar: python -m streamlit run app.py
7. Abrir http://localhost:8501 si no se abre automáticamente.
8. Detener con Ctrl+C.

PRUEBAS
Con el entorno activado: python test_automatico.py
Probar las 12 preguntas de pruebas.csv EN LA INTERFAZ; anotar resultados reales y comentarios.
Evaluar la claridad y facilidad de uso mediante una encuesta corta a participantes reales SI están disponibles.

PUBLICACIÓN SIN INSTALAR PYTHON
1. Crear repositorio público GitHub (solo estos archivos; no subir claves o datos personales).
2. Elegir Add file > Upload files y subir app.py, motor.py, preguntas.csv, requirements.txt, etc.
3. En https://share.streamlit.io iniciar sesión con GitHub.
4. Crear aplicación desde el repositorio, rama main, archivo app.py.
5. Copiar y comprobar el enlace público .streamlit.app en una ventana de incógnito.

LIMITACIONES
Este programa no usa un modelo generativo ni comprende significados como un LLM. Recupera la respuesta de mayor similitud si supera el umbral 0.23.
La similitud NO es una probabilidad de exactitud. Debe validarse con consultas reales y puede producir emparejamientos erróneos.
El sistema no reemplaza a especialistas en seguridad ni acredita uso correcto de EPP.
Los textos de preguntas.csv se redactaron como base educativa inicial y requieren una revisión de pertinencia según la normativa local y el contexto.
