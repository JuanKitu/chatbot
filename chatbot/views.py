import sys

__author__ = 'roloprogramating'
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
import json
from chatbot.models import *
import django.core.mail as core_email
from django.conf import settings
from django.http import HttpResponseRedirect
from chatbot.utils import http_wrapper
import socket
import json


def main(request):
    if not hasattr(request.session, "session_key") or request.session.session_key is None:
        request.session.modified = True
    t = get_template('../templates/chatbot.html')
    html = t.render(Context())
    return HttpResponse(html)


def process_message(request):
    question = request.POST["message"]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname() #'10.0.0.1'#'192.168.56.1'  # 'floating-fjord-3731.herokuapp.com'#immepythonnse-dawn-3702.herokuapp.com
    port = 3883
    print('trying to connect to ' + host +' '+ str(port) + ' Pregunta:' + question)
    try:
        s.connect((host, port))
    except:
        print('No se puede conectar al servidor ')
    print("El cliente pregunta: ", question)
    results = None
    try:
        http_payload = http_wrapper.httpjson_from_dic({"question": question}, host, port)
        print('paylaod' + http_payload)
        cantBytes = s.send(bytes(http_payload, 'UTF-8'))
        print("Cliente: se enviaron ", cantBytes, " bytes")
        response = http_wrapper.dic_from_httpjson(s.recv(4096).decode("utf-8"))
        if response["status"] == "ANSWER":
            answer = response["response"]["text"]
            results = response["response"]["results"]
        else:
            answer = "ERROR: el chatbot no pudo procesar la pregunta"
    except:
        print('El ChatBot no contesta...' + str(sys.exc_info()[0]))
        answer = 'El ChatBot no contesta...'
        s.close()
    s.close()
    to_json = {'response': answer, 'results': results}
    return HttpResponse(json.dumps(to_json), content_type='application/json')


def contact(request):
    t = get_template('../templates/contact.html')
    html = t.render(Context())
    return HttpResponse(html)


def navbar(request):
    t = get_template('../templates/general.html')
    html = t.render(Context())
    return HttpResponse(html)


def send_contact(request):
    name = request.POST["name"]
    email = request.POST["email"]
    message = request.POST["textmessage"]
    core_email.send_mail('CHATBOT Contact from: ' + name + "<" + email + ">", message, email,
                         settings.CONTACT_DESTINATIONS, fail_silently=False)
    return HttpResponseRedirect('/')


def populate_database(request):
    question = KnownQuestion()
    ans = Answer()
    ans.type = 'link'
    ans.content = '/static/assets/Ordenanza_N_1345-_modificacin_de_la_condicin_de_alumno_regular.pdf'
    ans.text = 'Creo que debes cursar 2 materias al año, revisa la informacion debajo'
    ans.save()
    question.text = 'condicion ser alumno regular'
    question.answer = ans
    question.save()
    return HttpResponse()

from django.views.generic import ListView
from django.views.generic.detail import DetailView

#from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

#class ListaDocumentos(LoginRequiredMixin,ListView):
