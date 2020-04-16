__author__ = 'roloprogramating'
import json
def wrap_payload(payload,host,port):
    return 'POST / HTTP/1.1\r\n'+'Host:'+str(host)+':'+str(port)+'\r\n'+'Content-Length:'+str(len(payload))+'\r\n'+'\r\n'+str(payload)

def unwarp_payload(http_request):
    return str(str(http_request).split('\r\n')[-1])

def wrap_response(response):
    return 'HTTP/1.1 200 OK'+'\r\n'+'Content-Type: text/plain; charset=utf-8'+'\r\n'+'\r\n'+str(response)

def httpjson_from_dic(payload,host='',port='',type='request'):
    if type=='request':
        return wrap_payload(json.dumps(payload, default= lambda obj: obj.__dict__), host, port)
    elif type=='response':
        return wrap_response(json.dumps(payload, default= lambda obj: obj.__dict__))
    else:
        return None
def dic_from_httpjson(payload):
    jsonstring=unwarp_payload(payload)
    print('temp '+jsonstring)
    return json.loads(jsonstring)

