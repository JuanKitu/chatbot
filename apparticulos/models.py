from django.db import models
from appdocumentos.models import Documento
# Create your models here.

class Articulo(models.Model):
    idarticulo = models.AutoField(primary_key = True)
    iddocumento = models.ForeignKey(Documento, db_column='iddocumento')
    tipo = models.CharField(max_length=30,choices=[('articulo', 'Articulo'), ('anexo', 'Anexo'),('considerando', 'Considerando')])
    capitulo = models.CharField(max_length=200)
    texto = models.TextField()
    numero = models.IntegerField()
    class Meta:
        db_table = 'reglamentacion\".\"articulos'
        managed = False
