__author__ = 'Andres'
import psycopg2
from urllib.parse import urlparse
import socket
import select
import os
from chatbot.utils import http_wrapper
from chatbot.chatengine import CHATBOT_CONNECTION_STRING
from chatbot.chatengine.motor_aiml import MotorAiml
from chatbot.chatengine import AIML_DIRECTORY
from chatbot.chatengine.motor_preguntas_predefinidas import MotorPreguntasPredefinidas
from chatbot.chatengine.motor_chat import MotorChat
import json
import datetime


class TestingEngine():
    def __init__(self):
        motor_aiml = MotorAiml(AIML_DIRECTORY)
        motor_predefinidas = MotorPreguntasPredefinidas(CHATBOT_CONNECTION_STRING, 80)
        self.connection_string = CHATBOT_CONNECTION_STRING
        self.motor = MotorChat(motor_aiml, motor_predefinidas)
        self.questions={}
        self.nroLote=0

    def cargarLotePreguntas(self, nroLote=1):
        self.nroLote=nroLote
        con = psycopg2.connect(self.connection_string)
        cursor = con.cursor()
        cursor.execute("SELECT * FROM reglamentacion.loteconsultas WHERE id=id and lote = "+str(self.nroLote)+" ORDER BY id")
        self.questions = cursor.fetchall()


    def correr(self, k=10, threshold=0.0001,mostrar='todo'):
        ahora = datetime.datetime.now()
        descripcion = '-- CON USO DE SINONIMOS DESDE LA PREGUNTA PREDEFINDA A LA BD --'
        print('---------------------------------------------------------------------------------------')
        print("Comienzo de los experimentos para el Lote numero " + str(self.nroLote))
        print('FECHA Y HORA: %s' % ahora)
        print('DESCRIPCION DEL EXPERIMENTO: '+descripcion)
        print('---------------------------------------------------------------------------------------')
        print('  CONFIGURACION')
        print('      Cantidad de vecinos más cercanos: k=',k)
        print('      Umbral: threshold=',threshold)
        print('      -------------------------------------------------- ')
        print('      - Configuración de la búsqueda de las preguntas predefinidas')
        print('        - Cantidad máxima de preguntas predefinidas como respuesta: k=1')
        print('        - Distancia máxima permitida como válida entre le consulta y el patrón (radio): threshold=70 ')
        print('      - Configuración de la búsqueda de los artículos en base a la pregunta predefinida seleccionada')
        print('        - Umbral (valor mínimo que tiene que tener la comparación entre la pregunta predefinida y el texto')
        print('          para que sea considerado como respuesta): 0.06')
        print('        - Cantidad máxima de artículos como respuesta: k=10')

        for question in self.questions:
            print("La pregunta es: ",str(question))
            # self.administrador_preguntas.agregar(question[0], question[1], )
            currentQuestion=question[2]
            # Get the list sockets which are ready to be read through select
            respuesta = self.motor.respond(currentQuestion,k,threshold)
            if mostrar=='todo':
                if len(respuesta.results)>0:
                    for res in respuesta.results:
                       print("     Respuesta: (",res.score,") Art: ",res.id_articulo,"  [",res.texto_articulo,"]")
                else:
                    print('     ////> Sin respuesta')

        # The select function is given the list of connected sockets CONNECTION_LIST. The 2nd and 3rd parameters are kept empty since we do not need to check any sockets to be writable or having errors.
        # Output


if __name__ == "__main__":
    tester = TestingEngine()
    tester.cargarLotePreguntas(1)
    tester.correr(mostrar='todo')

