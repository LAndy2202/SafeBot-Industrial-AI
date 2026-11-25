from motor import MotorFAQ
motor = MotorFAQ('preguntas.csv')
casos = [
  ('¿Qué son los equipos de protección personal?', True),
  ('¿Para qué sirve un casco de seguridad?', True),
  ('¿Qué es un falso negativo?', True),
  ('¿Cómo elegir guantes de seguridad?', True),
  ('¿Cuál es la capital de Francia?', False),
  ('¿Quién ganó la copa mundial de fútbol?', False),
]
aciertos = 0
for texto, esperado in casos:
    resultado = motor.responder(texto)
    ok = resultado['encontrada'] == esperado
    aciertos += int(ok)
    print(('OK' if ok else 'REVISAR'), '|', texto, '| coincidencia:', round(resultado['confianza'], 3), '|', resultado['respuesta'][:75])
print(f'Resultado pruebas básicas: {aciertos}/{len(casos)}')
