__author__ = 'andres_2'
import psycopg2
import sys
from chatbot.chatengine.resultado_motor import ResultadoMotor, Metadatos

"""
Clases correspondientes al Interprete que toma una especifacion de Keywords como programa fuente y una lista
de palabras correspondientes a la pregunta que hace el usuario  y devuelve un valor de similitud. El valor
0 indica que la lista de palabras se corresponde totalmente con el patron especificado por las Keywords
"""
def eliminarPalabras(listaPalabrasAEliminar, listaPalabras):
    for p in listaPalabrasAEliminar:
        if listaPalabras.count(p)>0:
            listaPalabras.remove(p)
    return listaPalabras

def eliminarSimbolos(lista, cadena):
    for sim in lista:
        if cadena.count(sim)>0:
            cadena=cadena.replace(sim,'')
    return cadena


def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


# Pasar todas las cadenas en minusculas, o en mayusculas, pero no mezclar
class InterpretePregunta:
    ############## METODOS PARA INICIALIZAR Y REALIZAR EL ANALISIS
    def __init__(self, patronFuente):
        # fuente debe ser un patron especificado de acuerdo a la CFG
        self.fuente = patronFuente
        self.longitudPatron = 1
        # cargar la tas
        self.tas = {'<keywords>': {'palabra': ['<key>', '<sigkey>'],
                                   '+': 'error',
                                   '|': 'error',
                                   '{': ['<key>', '<sigkey>'],
                                   '}': 'error',
                                   '$': 'error'
        },
                    '<sigkey>': {'palabra': 'error',
                                 '+': ['+', '<key>', '<sigkey>'],
                                 '|': [],
                                 '{': 'error',
                                 '}': [],
                                 '$': []
                    },
                    '<key>': {'palabra': ['palabra'],
                              '+': 'error',
                              '|': 'error',
                              '{': ['{', '<listaOpcional>', '}'],
                              '}': 'error',
                              '$': 'error'
                    },
                    '<listaOpcional>': {'palabra': ['<keywords>', '<sigkeywords>'],
                                        '+': 'error',
                                        '|': 'error',
                                        '{': ['<keywords>', '<sigkeywords>'],
                                        '}': 'error',
                                        '$': 'error'
                    },
                    '<sigkeywords>': {'palabra': 'error',
                                      '+': 'error',
                                      '|': ['|', '<keywords>', '<sigkeywords>'],
                                      '{': 'error',
                                      '}': [],
                                      '$': 'error'
                    }}
        # Terminales
        self.terminales = {'{', '}', 'palabra', '|', '+'}

    def siguienteComplex(self):
        # devuelve el siguiente componente lexico, error o pesos (fin del programa fuente)
        # componentes lexicos: llaveAbre, llaveCierra, palabra, barra, mas
        controlAux = self.control
        # ignorar caracteres de control
        while controlAux < len(self.fuente) and self.fuente[controlAux] <= ' ':
            controlAux = controlAux + 1
        # buscar el siguiente componente lexico, error, o pesos (fin de cadena)
        encontrado = False
        lexema = ''
        estado = 0
        while not encontrado:
            if estado == 0:
                if controlAux >= len(self.fuente):
                    terminal = '$'
                    encontrado = True
                elif self.fuente[controlAux] == '|':
                    terminal = '|'
                    encontrado = True
                    self.control = controlAux + 1
                elif self.fuente[controlAux] == '+':
                    terminal = '+'
                    encontrado = True
                    self.control = controlAux + 1
                elif self.fuente[controlAux] == '{':
                    terminal = '{'
                    encontrado = True
                    self.control = controlAux + 1
                elif self.fuente[controlAux] == '}':
                    terminal = '}'
                    encontrado = True
                    self.control = controlAux + 1
                # elif self.fuente[controlAux]==' ' or \
                elif (self.fuente[controlAux] >= 'a' and self.fuente[controlAux] <= 'z') or \
                        (self.fuente[controlAux] >= 'A' and self.fuente[controlAux] <= 'Z') or (self.fuente[controlAux] in ['á','é','í','ó','ú','ñ','Ñ']) or (self.fuente[controlAux]>='0' and self.fuente[controlAux]<='9'):
                    lexema = lexema + self.fuente[controlAux]
                    estado = 1
                    controlAux = controlAux + 1
                else:
                    encontrado = True
                    terminal = 'error'
            elif estado == 1:
                if controlAux >= len(self.fuente):
                    terminal = 'palabra'
                    encontrado = True
                    self.control = controlAux
                elif self.fuente[controlAux] == ' ' or \
                        (self.fuente[controlAux] >= 'a' and self.fuente[controlAux] <= 'z') or \
                        (self.fuente[controlAux] >= 'A' and self.fuente[controlAux] <= 'Z'):
                    lexema = lexema + self.fuente[controlAux]
                    estado = 1
                    controlAux = controlAux + 1
                else:
                    terminal = 'palabra'
                    encontrado = True
                    self.control = controlAux
        return {'terminal': terminal, 'lexema': lexema}


    def analisisSintactico(self):
        # analiza el patron Fuente y guarda el Arbol de Derivacion, para que se pueda realizar la interpretacion

        # control es el apuntador al programa fuente, que indica el elemento que se está analizando
        self.control = 0
        # inicializo el arbol de derivacion
        raiz = {'nodo': '<keywords>', 'lexema': '', 'hijos': []}
        self.arbol = raiz
        # definir la pila con el simbolo pesos y el simbolo inicial de la CFG
        # los elementos de la pila estan conformados por el simbolo gramatical y un atributo
        # el atributo es el lexema, si el simbolo es terminal, y el nodo del arbol de derivacion, si es variable
        self.pila = [{'simbolo': '$', 'atributo': '$'}, {'simbolo': '<keywords>', 'atributo': raiz}]
        elemPila = self.pila.pop()
        tope = elemPila['simbolo']
        atributo = elemPila['atributo']
        # scanner: obtener siguiente componente lexico y lexema
        terminalYLexema = self.siguienteComplex()
        terminal = terminalYLexema['terminal']
        lexema = terminalYLexema['lexema']
        estado = 'analizando'
        while estado == 'analizando':
            if tope in self.terminales:
                if tope == terminal:
                    # el tope es terminal y coincide con la entrada, por lo cual hay que registrar el lexema
                    # correspondiente al terminal en el arbol de derivacion
                    # atributo: mantiene el apuntador al nodo
                    # lexema: lexema encontrado por el analizador lexico
                    atributo['lexema'] = lexema
                    # adelantar el control que apunta a la cadena de entrada
                    terminalYLexema = self.siguienteComplex()
                    terminal = terminalYLexema['terminal']
                    lexema = terminalYLexema['lexema']
                    # desapilar un nuevo elemento
                    elemPila = self.pila.pop()
                    tope = elemPila['simbolo']
                    atributo = elemPila['atributo']
                else:
                    estado = 'error'
            elif tope == '$' and terminal == '$':
                estado = 'aceptada'
            elif self.tas[tope][terminal] == 'error':
                estado = 'error'
            else:
                # obtener la produccion de la TAS
                produccion = self.tas[tope][terminal]
                # Apilar los elementos de la produccion, en orden inverso
                # y agregar los nodos correspondientes a cada elemento en el arbol de derivacion
                for elem in reversed(produccion):
                    # crear el nodo del arbol, sin hijos
                    nodo = {'nodo': elem, 'lexema': '', 'hijos': []}
                    # agregar el nodo como hijo de la variable que produce, de tal manera que el ultimo quede al
                    # principio, ya que se recorren al reves para poder apilarlos
                    atributo['hijos'].insert(0, nodo)
                    # apilar el elemento, haciendo referencia al nodo
                    self.pila.append({'simbolo': elem, 'atributo': nodo})

                # despues de cargar la produccion en la pila, desapilar el elemento al tope
                elemPila = self.pila.pop()
                tope = elemPila['simbolo']
                atributo = elemPila['atributo']
        if estado == 'aceptada':
            return True
        else:
            return False


    ########## METODOS AUXILIARES
    def imprimirNodo(self, nodo, tab=''):
        atrib = ''
        if nodo['nodo'] == 'palabra':
            atrib = '(' + nodo['lexema'] + ')'
        print(tab, nodo['nodo'], atrib)
        tab = tab + '   '
        for elem in nodo['hijos']:
            self.imprimirNodo(elem, tab)

    def imprimirArbol(self):
        self.imprimirNodo(self.arbol)


    ##########  METODOS PARA LA INTERPRETACION ###############

    def evalKey(self, nodo, palabrasConsultadas):
        hijo = nodo['hijos'][0]
        if hijo['nodo'] == '{':
            # <key> ::= { <listaOpcional> }
            dis,cant=self.evalOpcional(nodo['hijos'][1], palabrasConsultadas)
            return dis,cant
        else:
            # <key> ::= palabra
            dis = self.minLev(hijo['lexema'], palabrasConsultadas)
            return dis,1

    def evalSigkey(self, nodo, palabrasConsultadas):
        if len(nodo['hijos']) == 0:
            # <sigkey> ::= epsilon
            return 0,0
        else:
            self.longitudPatron += 1
            # <sigkey> ::= +  <key> <sigkey>
            dis1,cant1=self.evalKey(nodo['hijos'][1], palabrasConsultadas)
            dis2,cant2=self.evalSigkey(nodo['hijos'][2], palabrasConsultadas)
            return dis1+dis2,cant1+cant2


    def evalOpcional(self, nodo, palabrasConsultadas):
        # <listaOpcional> ::=  <keywords> <sigkeywords>
        dis1,cant1=self.evalKeywords(nodo['hijos'][0], palabrasConsultadas)
        dis2,cant2=self.evalSigKeywords(nodo['hijos'][1], palabrasConsultadas)
        if dis1<dis2:
            mini=dis1
            cant=cant1
        else:
            mini=dis2
            cant=cant2
        return mini, cant

    def minLev(self, lexema, palabrasConsultadas):
        # devuelve la distancia minima de levenshtein, expresada como porcentaje sobre la longitud del lexema
        if len(lexema) == 0:
            return 0
        else:
            minimo = 1000
            for pal in palabrasConsultadas:
                dis = levenshtein(lexema, pal)
                porcentaje = dis * 100 / (max(len(lexema),len(pal)))
                #if porcentaje>100:
                #    print('/////// levenshtein entre ',pal,' y ',lexema,' mayor a 100: ',porcentaje)
                if porcentaje < minimo:
                    minimo = porcentaje
            return minimo

    def evalSigKeywords(self, nodo, palabrasConsultadas):
        if len(nodo['hijos']) == 0:
            # <sigkeywords> ::= epsilon
            return 10000000,0
        else:
            # <sigkeywords>  ::= | <keywords> <sigkeywords>
            dis1,cant1=self.evalKeywords(nodo['hijos'][1], palabrasConsultadas)
            dis2,cant2=self.evalSigKeywords(nodo['hijos'][2], palabrasConsultadas)
            if dis1<dis2:
                mini=dis1
                cant=cant1
            else:
                mini=dis2
                cant=cant2
            return mini, cant


    def evalKeywords(self, nodo, palabrasConsultadas):
        self.longitudPatron += 1
        # <keywords> ::= <key> <sigkey>
        dis1,cant1=self.evalKey(nodo['hijos'][0], palabrasConsultadas)
        dis2,cant2=self.evalSigkey(nodo['hijos'][1], palabrasConsultadas)
        return dis1+dis2,cant1+cant2
        #return self.evalKey(nodo['hijos'][0], palabrasConsultadas) + self.evalSigkey(nodo['hijos'][1],
        #                                                                             palabrasConsultadas)

    def distanciaA(self, palabrasConsultadas):
        # recorre el arbol calculando la distancia y la devuelve
        self.longitudPatron = 1
        dist,cant = self.evalKeywords(self.arbol, palabrasConsultadas)
        # normalizar distancia, como el promedio de las distancias calculadas entre las palabras de la consulta y
        # las palabras efectivamente utilizadas del patron
        # print('cant = ',cant,'   long patron = ',self.longitudPatron)
        dist = dist / cant
        return dist


class AdmPreguntas:
    """
      La clase Admimintrador de Preguntas mantiene una lista de las preguntas formalizadas junto a sus patrones y
      los arboles de derivacion correspondientes con el fin de determinar a partir de una coleccion de palabras de
      entrada (correspondiente a una pregunta informal), cual es la pregunta que mas corresponde al conjunto.

      Permite
        - agregar preguntas (idPregunta, pregunta, patron)
        - consultar los k vecinos mas cercanos nnk(k)
    """

    def __init__(self):
        self.preguntas = []

    def agregar(self, idPregunta=0, pregunta='', patron='', keywords=[]):
        """
        :param id: identificador de la pregunta en la base de datos. Deberia ser unico y distinto de 0
        :param pregunta: cadena que representa la pregunta formalizada
        :param patron: cadena que especifica las palabras y alternativas que deberia contener una pregunta informal para ser considerada
          equivalente a la pregunta formalizada
        :return: verdadero si se pudo agregar la pregunta
        """
        print('-- Analizar pregunta [',idPregunta,']:',str(pregunta))
        print('-------- Patrón: ',str(patron))
        interprete = InterpretePregunta(patron)
        if interprete.analisisSintactico() and idPregunta > 0 and pregunta > '':
            elemento = {'idPregunta': idPregunta,
                        'pregunta': pregunta,
                        'patron': patron,
                        'interprete': interprete,
                        'keywords': keywords}
            self.preguntas.append(elemento)
            return True
        else:
            return False

    def nnk(self, palabrasConsultadas=[], k=1):
        """
        :param k: k vecinos mas cercanos. Por defecto, 1
        :return: devuelve una lista con las preguntas mas cercanas a la lista de palabras de entrada y sus distancias
        """

        resultado = []
        for elem in self.preguntas:
            distancia = elem['interprete'].distanciaA(palabrasConsultadas)
            res = {'idPregunta': elem['idPregunta'],
                   'pregunta': elem['pregunta'],
                   'distancia': distancia,
                   'keywords': elem['keywords'],
                   'patron': elem['patron']}
            resultado.append(res)
        resultado.sort(key=lambda x: x['distancia'])
        return resultado[0: k]


class MotorPreguntasPredefinidas:
    def __init__(self, connection_string, threshold):
        self.administrador_preguntas = AdmPreguntas()
        self.threshold = threshold
        self.connection_string = connection_string
        con = psycopg2.connect(connection_string)
        cursor = con.cursor()
        cursor.execute("SELECT * FROM PREDEFINEDQUESTIONS")
        questions = cursor.fetchall()
        for question in questions:
            print(str(question))
            self.administrador_preguntas.agregar(question[0], question[1], question[2])

    def respond(self, question, k, threshold=0.0):
        # print('in respond')
        questionClean=eliminarSimbolos(['?',',','¿','(',')'], question)
        questionClean=questionClean.lower()
        splited = questionClean.split()
        splited = eliminarPalabras(['el','la','lo','los','las','de','para','al','a','o','y','del', 'si', 'en','un','una','es','se','ya'],splited)

        # buscar
        predefinida = self.administrador_preguntas.nnk(splited)
        if (predefinida[0]['distancia'] < self.threshold):
            print('   Palabras consultadas: ',splited)
            print('   Predefinida: ',predefinida[0]['idPregunta'],', Pregunta:',predefinida[0]['pregunta'],
                  ', Distancia:', predefinida[0]['distancia'],' -- ' ,predefinida[0]['patron'])

            # buscar
            results=self.find_result(predefinida[0]['idPregunta'], k, 0.01) #threshold)
            # print(str(results))
            respuesta_textual='Encontre las siguientes respuestas para:' + predefinida[0]['pregunta'] if len(results)>0 \
                else 'Lo siento, no tengo informacion para responder:' + predefinida[0]['pregunta']
            resultado_motor=ResultadoMotor(respuesta_textual)
            for result in results:
                resultado_motor.results.append(Metadatos(question, predefinida[0]['idPregunta'], predefinida[0]['pregunta'], predefinida[0]['distancia'], result[0],result[1],result[2]))
            return resultado_motor
        else:
            return None

    def find_result(self, idPregunta, k, threshold):
            try:
                con = psycopg2.connect(self.connection_string)
                # print("conectado con " + self.connection_string)
                cursor = con.cursor()
                # print("cursor creado para pregunta " + str(idPregunta))
                cursor.execute("select * from consultarNNK(%s, %s, %s)", (idPregunta, k, threshold))
                # print('execute created')
                result= cursor.fetchall()
                # print(str(result))
                return result
            except  Exception as ex:
                print("Unexpected error:", sys.exc_info())

############### CODIGO PARA EJECUTAR EL MODULO COMO PROGRAMA; SOLO PARA PRUEBA
if __name__ == '__main__':
    patron = '{requisitos| necesita |pautas| cuales+puntos| cuando |que}+ alumno+ regular'
    # patron = '{ hola + como + te + va} '
    palabrasConsultadas = ['que', 'se', 'necesita', 'para', 'ser', 'alumno', 'regilar', '?']
    palabrasConsultadasInvalidas = ['hola', 'como', 'estas', '?']
    interprete = InterpretePregunta(patron)
    if interprete.analisisSintactico():
        print('VALIDA...')
        interprete.imprimirArbol()
        # valido
        print('La distancia entre:')
        print('    ', patron)
        print('y:')
        print('    ', palabrasConsultadas)
        print('     es igual a: ', interprete.distanciaA(palabrasConsultadas))
        # invalido
        print('')
        print('    ', palabrasConsultadasInvalidas)
        print('     es igual a: ', interprete.distanciaA(palabrasConsultadasInvalidas))
        # otro
        print('')
        print('    ', ['hola'])
        print('     es igual a: ', interprete.distanciaA(['hola']))

        # Prueba del administrador de preguntas
        adm = AdmPreguntas()
        adm.agregar(1, '¿Cuales son los requisitos para ser alumno regular?',
                    '{requisitos| necesita |pautas| cuales+puntos| cuando |que}+ alumno+ regular')
        adm.agregar(2, '¿Cuantas veces se puede rendir un final?', '{veces|cuando + recursar} + final')
        adm.agregar(3, '¿Cuanto dura la regularidad de una materia?', '{extender|cuanto|extension} + regularidad')
        resul = adm.nnk(palabrasConsultadas, 3)
        for r in resul:
            print(r)
    else:
        print('INVALIDA')