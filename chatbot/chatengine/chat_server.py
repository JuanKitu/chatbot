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


class ServidorChat():
    def __init__(self, puerto=3883, buffer=4096, conexiones=5):
        # self.motor = MotorAiml(AIML_DIRECTORY)
        self.CONNECTION_LIST = []  # list of socket clients
        self.RECV_BUFFER = buffer  # Advisable to keep it as an exponent of 2
        self.PORT = puerto
        self.connections = conexiones
        motor_aiml = MotorAiml(AIML_DIRECTORY)
        motor_predefinidas = MotorPreguntasPredefinidas(CHATBOT_CONNECTION_STRING, 40)
        #print(CHATBOT_CONNECTION_STRING)
        self.motor = MotorChat(motor_aiml, motor_predefinidas)


    def correr(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host = socket.gethostbyname(socket.gethostname())
        print('binding to ' + host + ' in ' + str(self.PORT))
        server_socket.bind((host, self.PORT))
        server_socket.listen(self.connections)

        # Add server socket to the list of readable connections
        self.CONNECTION_LIST.append(server_socket)

        print("El Servidor de Chat/SE se está ejecutando en el puerto: " + str(self.PORT))

        while 1:
            # Get the list sockets which are ready to be read through select
            read_sockets, write_sockets, error_sockets = select.select(self.CONNECTION_LIST, [], [])

            for sock in read_sockets:

                # New connection
                if sock == server_socket:
                    # Handle the case in which there is a new connection recieved through server_socket
                    sockfd, addr = server_socket.accept()
                    self.CONNECTION_LIST.append(sockfd)
                    print("Servidor: Se conectó el Cliente (%s, %s)" % addr)

                # Some incoming message from a client
                else:
                    # Data recieved from client, process it
                    try:
                        #In Windows, sometimes when a TCP program closes abruptly,
                        # a "Connection reset by peer" exception will be thrown
                        raw_bytes = sock.recv(self.RECV_BUFFER)
                        raw_http = raw_bytes.decode('utf-8')
                        if raw_http:
                            print('se recibio el contenido http ' + raw_http)
                            request = http_wrapper.dic_from_httpjson(raw_http)
                        if request["question"]:
                            print("Servidor: El Cliente pregunta: ", request["question"])
                            respuesta = self.motor.respond(request["question"],request["k"] if "k" in request else 2, request["threshold"] if "threshold" in request else 1)
                            if not respuesta:
                                status = "NO_ANSWER"
                            else:
                                status = "ANSWER"
                            response = http_wrapper.httpjson_from_dic(
                                {"response": {"text": respuesta.text, "results": respuesta.results if respuesta.results is not None else None}, "status": status},
                                type='response')
                            print("Servidor: La respuesta es: ", respuesta.text)
                            sock.send(bytes(response, 'UTF-8'))
                            print("Se envio la respuesta: " + response)
                    except Exception as ex:
                        print("Servidor: El Cliente (%s, %s) se encuentra offline" % addr)
                        sock.close()
                        self.CONNECTION_LIST.remove(sock)
                        continue

        server_socket.close()

        # The select function is given the list of connected sockets CONNECTION_LIST. The 2nd and 3rd parameters are kept empty since we do not need to check any sockets to be writable or having errors.
        # Output


if __name__ == "__main__":
    servidor = ServidorChat()
    servidor.correr()

