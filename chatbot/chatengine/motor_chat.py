__author__ = 'roloprogramating'
from chatbot.chatengine.motor_aiml import MotorAiml
from chatbot.chatengine.motor_preguntas_predefinidas import MotorPreguntasPredefinidas
import psycopg2
from chatbot.chatengine import CHATBOT_CONNECTION_STRING
from chatbot.chatengine import PREDEFINED_QUESTION_THRESHOLD


class MotorChat:
    def __init__(self, motor_aiml, motor_predefined):
        self.motor_predefinidas = motor_predefined
        self.motor_aiml = motor_aiml

    def respond(self, question, k, threshold):
        # print('in chatbot engine')
        predef = self.motor_predefinidas.respond(question, k, threshold)
        if predef is not None:
            # print('predef: ', predef.text)
            return predef
        else:
            # print('predef  none')
            return self.motor_aiml.respond(question)
