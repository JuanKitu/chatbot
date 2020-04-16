# -*- coding: utf-8 -*-
__author__ = 'andres'

import urllib.request
import re
from bs4 import BeautifulSoup


class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"


noticias = open("noticias.csv", "w")

opener = AppURLopener()

for i in range(500):
    i1 = i + 188
    response = opener.open('https://tn.com.ar/policiales?page='+str(i1))
    cadena = response.read()
    soup = BeautifulSoup(cadena, 'html.parser')
    cant = 1
    for link in soup.find_all('a'):
        url = link.get('href')
        titulo = link.text
        stop = False
        if (url.find('/policiales/')>-1) and (len(titulo)>10):
            try:
                respuesta = opener.open('https://tn.com.ar'+url)
                htmlcuerpo = respuesta.read()
                soupcuerpo = BeautifulSoup(htmlcuerpo, 'html.parser')
                fecha = ''
                for fecont in soupcuerpo.find_all('div'):
                    clasefecha = fecont.get('class')
                    if clasefecha != None:
                        for clase in clasefecha:
                            if clase=='news-article-date':
                                for cf in fecont.find_all('span'):
                                    if cf.text.find('/')>-1:
                                        fecha = cf.text
                cuerpo = ''
                for cu in soupcuerpo.find_all('p'):
                    clase = cu.get('class')
                    texto = cu.text
                    if texto.find("Copyright")>=0:
                        stop = True
                    if not stop and (clase == None):
                        cuerpo = cuerpo + ' ' + texto
                cadena = str(i1)+' & '+str(cant)+' & '+str(fecha)+' & '+titulo.strip()+' & '+ url.strip()+' & '+cuerpo.strip()
                noticias.write(cadena.encode().decode('windows-1252','ignore')+'\n')
                print(cant)
                cant = cant + 1
            except Exception:
                print('Error al abrir url ','https://tn.com.ar'+url)

noticias.close()



