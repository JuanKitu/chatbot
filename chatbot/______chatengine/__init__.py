__author__ = 'andres_2'
import os
from urllib.parse import urlparse
if ('DATABASE_URL') in os.environ:
    CHATBOT_CONNECTION_STRING =os.environ["DATABASE_URL"]
else:
    CHATBOT_CONNECTION_STRING = "host='localhost' dbname='ptah' port=5432 user='postgres' password='investigacion'"

# CHATBOT_CONNECTION_STRING = "host='localhost' dbname='ptah' user='postgres' password='andres22'"
PREDEFINED_QUESTION_THRESHOLD=1
AIML_DIRECTORY=os.path.dirname(__file__)