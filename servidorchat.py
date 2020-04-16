import os
from chatbot.chatengine.chat_server import ServidorChat
port=3883
if ('PORT') in os.environ:
    port=int(os.environ['PORT'])
print('binding to port: ' +str(port))
servidor=ServidorChat(port)
servidor.correr()
