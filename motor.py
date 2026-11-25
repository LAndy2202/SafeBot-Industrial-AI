"""SafeBot-EPP — motor de recuperación controlada, versión 3.
Selecciona respuestas del archivo CSV y nunca genera información nueva.
"""
import re
import unicodedata
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

VERSION_MOTOR = '3.0'

def normalizar(texto):
    t = str(texto).casefold()
    t = ''.join(c for c in unicodedata.normalize('NFD', t) if unicodedata.category(c) != 'Mn')
    t = re.sub(r'[^a-z0-9ñ]+', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

MENSAJE_FUERA = ('Esta consulta está fuera de mi dominio. Solo respondo preguntas sobre '
                 'equipos de protección personal, prevención de riesgos y detección de EPP mediante IA.')
MENSAJE_DUDA = ('No tengo una respuesta suficientemente confiable para esa consulta. '
               'Prueba preguntarme sobre cascos, guantes, batas o métricas de detección. '
               'Para decisiones de seguridad, consulta a una persona profesional responsable.')
PALABRAS_DOMINIO = set(('epp proteccion protector protectora personal industrial seguridad casco cascos guante guantes '
 'bata batas prenda prendas riesgo riesgos taller accidente accidentes peligro peligros maquina maquinas '
 'mano manos cabeza quimico quimicos inspeccion inspeccionar vision computacional ia inteligencia '
 'detector deteccion detectar modelo dataset aprendizaje datos imagen imagenes alerta alertas '
 'falso falsa negativo negativa positivo positiva precision recall map sobreajuste jerarquia '
 'controles equipos equipamiento grieta grietas rota rotos roto rotas elegir usar iou f1 fps '
 'inferencia fotograma fotogramas clasificacion').split())

class MotorFAQ:
    def __init__(self, ruta='preguntas.csv', umbral=0.30):
        self.datos = pd.read_csv(ruta, encoding='utf-8-sig').fillna('')
        self.umbral = umbral
        if not {'pregunta','respuesta','fuente','categoria'} <= set(self.datos.columns):
            raise ValueError('El CSV debe contener: categoria,pregunta,respuesta,fuente')
        self.preguntas_norm = self.datos['pregunta'].astype(str).map(normalizar).tolist()
        self.exactas = {q: i for i, q in enumerate(self.preguntas_norm)}
        self.vectorizador = TfidfVectorizer(preprocessor=normalizar, ngram_range=(1,2), sublinear_tf=True)
        self.matriz = self.vectorizador.fit_transform(self.datos['pregunta'].astype(str))

    def _resultado(self, indice, puntaje):
        row = self.datos.iloc[indice]
        return {'respuesta':str(row['respuesta']), 'fuente':str(row['fuente']),
                'confianza':float(puntaje), 'encontrada':True}

    def _intencion(self, q):
        """Reglas acotadas: diferenciar negación, concepto y acción antes de TF-IDF."""
        w = set(q.split())
        # False alarms and false negatives have opposite meanings.
        pos = ('falso positivo' in q or 'falsa alarma' in q or 'falsos positivos' in q)
        neg = ('falso negativo' in q or 'falsos negativos' in q)
        if pos and neg:
            return 'cual es la diferencia entre un falso positivo y un falso negativo'
        if pos: return 'que es un falso positivo'
        if neg: return 'que es un falso negativo'
        if 'precision' in w and 'recall' in w:
            return 'cual es la diferencia entre precision y recall'
        # 'Casco' intent: detection vs whether it is worn correctly vs protection vs inspection.
        casco = bool(w & {'casco','cascos'})
        if casco:
            correcta = any(p in q for p in ('bien colocad','correctamente','bien puesto','uso correcto','bien ajustad'))
            if correcta and any(p in q for p in ('detect','reconoc','identific','ia','inteligencia','vision')):
                return 'si la ia detecta un casco significa que esta bien colocado'
            if any(p in q for p in ('detect','reconoc','identific','localiz')) and any(p in q for p in ('ia','inteligencia artificial','vision','modelo','algoritmo','aprendizaje profundo','camara')):
                return 'la inteligencia artificial puede detectar un casco'
            if any(p in q for p in ('grieta','roto','dana','deterior')):
                return 'que pasa si el casco tiene una grieta'
            if any(p in q for p in ('inspecc','revis','antes de usar')):
                return 'como inspeccionar un casco'
            if any(p in q for p in ('para que','por que','necesito','protege','funcion','utilidad','importante','debo usar','debo poner')):
                return 'para que sirve un casco de seguridad'
        if 'bata' in w and any(p in q for p in ('quimic','sustancia','acido','todos los productos')):
            return 'una bata comun protege de cualquier sustancia'
        return None

    def responder(self, pregunta):
        q = normalizar(pregunta)
        if not q:
            return {'respuesta':'Escribe una pregunta para continuar.', 'fuente':'', 'confianza':0.0,'encontrada':False}
        if not (set(q.split()) & PALABRAS_DOMINIO):
            return {'respuesta':MENSAJE_FUERA, 'fuente':'', 'confianza':0.0,'encontrada':False}
        key = self._intencion(q)
        if key in self.exactas:
            return self._resultado(self.exactas[key], 1.0)
        if q in self.exactas:
            return self._resultado(self.exactas[q], 1.0)
        vector = self.vectorizador.transform([pregunta])
        sims = cosine_similarity(vector, self.matriz).ravel()
        index = int(sims.argmax());score=float(sims[index])
        if score < self.umbral:
            return {'respuesta':MENSAJE_DUDA, 'fuente':'','confianza':score,'encontrada':False}
        return self._resultado(index,score)
