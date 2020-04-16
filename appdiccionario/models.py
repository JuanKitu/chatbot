from django.db import models

# Create your models here.

class Diccionario(models.Model):
    id=models.AutoField(primary_key=True)
    palabra=models.CharField(max_length=30)
    porter=models.CharField(max_length=30)
    class Meta:
        db_table = 'reglamentacion\".\"diccionario'
        managed=False
