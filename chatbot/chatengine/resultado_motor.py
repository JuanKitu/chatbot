__author__ = 'roloprogramating'


class ResultadoMotor:
    def __init__(self, text):
        self.text = text
        self.results = list()

class Metadatos:
    def __init__(self, pregunta_original,id_pregunta_comprendida, pregunta_comprendida, distancia, id_articulo, texto_articulo, score):
        self.pregunta_original=pregunta_original
        self.distancia=distancia
        self.pregunta_comprendida=id_pregunta_comprendida
        self.pregunta_comprendida=pregunta_comprendida
        self.id_articulo=id_articulo
        self.texto_articulo=texto_articulo
        self.score=score