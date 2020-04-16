from django.db import models

# Create your models here.
class Predefinida(models.Model):
    id = models.AutoField(primary_key = True)
    question = models.CharField(max_length = 100)
    expression = models.CharField(max_length = 1000)
    reglamento = models.CharField(max_length = 50)
    articulo = models.IntegerField()
    class Meta:
        db_table = 'public\".\"predefinedquestions'
        managed = False

#  id integer NOT NULL DEFAULT nextval('predefinedquestions_id_seq'::regclass),
#  question text,
#  expression character varying(1000),
#  reglamento character varying(50), -- Nombre/numero del reglamento de donde se extrajo la pregunta, por ejemplo "Estatuto" o "Resolucion 154/16"
#  articulo integer,