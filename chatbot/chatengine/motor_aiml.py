__author__ = 'roloprogramating'
from chatbot.aiml.Kernel import Kernel
from chatbot.chatengine.resultado_motor import ResultadoMotor
import os


class MotorAiml(Kernel):
    def __init__(self, directory):
        super(MotorAiml, self).__init__()

        for nombre in os.listdir(directory):
            if nombre.upper().find('.AIML', 0, len(nombre)) > -1:
                print('learning ' + directory + '/' + nombre)
                self.learn(directory + '/' + nombre)

        self.setBotPredicate('nombre', 'Amy')
        self.setBotPredicate('name', 'Amy')
        self.setBotPredicate('ciudad', 'Concepcion del Uruguay')
        self.setBotPredicate('ciudadania', 'Argentino')
        self.setBotPredicate('edad', '27')
        self.setBotPredicate('anyo_nacimiento', '1987')

    def respond(self, question):
        result = super(MotorAiml, self).respond(question)
        return ResultadoMotor(result)