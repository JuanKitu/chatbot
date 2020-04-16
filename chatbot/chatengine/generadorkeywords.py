__author__ = 'Andres'
import psycopg2
from chatbot.chatengine import CHATBOT_CONNECTION_STRING
import datetime

# configuro Java
import os
java_path = "C:/Program Files (x86)/Java/jre1.8.0_161/bin/java.exe"
os.environ['JAVAHOME'] = java_path

# importo nltk con el tagger spanish de Stanford
from nltk.tag.stanford import POSTagger
spanish_postagger = POSTagger('c:/stanford-postagger/models/spanish.tagger', 'c:/stanford-postagger/stanford-postagger.jar')

# Leeo los textos de los articulos en la base de datos
con = psycopg2.connect(CHATBOT_CONNECTION_STRING)
cursor = con.cursor()
cursor.execute("SELECT texto FROM reglamentacion.articulos")
textos = cursor.fetchall()

# recorro los textos, hago el POS tagger de cada texto, y agrego en una lista las palabras que son sustentivos,
# adjetivos y verbos unicamente

for texto in textos:
    listaPalabras = spanish_postagger.tag(texto[0].split())
    for palabras in listaPalabras:
        for pal in palabras:
            if pal[1][0:1]=='v':
                cursor.execute("INSERT INTO reglamentacion.palabras(id, palabra, tipo) VALUES (DEFAULT, '"+pal[0]+"', 'V')")
                con.commit()
            if pal[1][0:1]=='n':
                cursor.execute("INSERT INTO reglamentacion.palabras(id, palabra, tipo) VALUES (DEFAULT, '"+pal[0]+"', 'S')")
                con.commit()
            if pal[1][0:1]=='a':
                cursor.execute("INSERT INTO reglamentacion.palabras(id, palabra, tipo) VALUES (DEFAULT, '"+pal[0]+"', 'A')")
                con.commit()

cursor.close()
con.close()

