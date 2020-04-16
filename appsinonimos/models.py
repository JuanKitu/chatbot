from django.db import models

# Create your models here.

class Sinonimo(models.Model):
    id = models.AutoField(primary_key = True)
    palabra = models.CharField(max_length = 30)
    sinonimo = models.CharField(max_length = 30)
    peso = models.FloatField()
    class Meta:
        db_table = 'reglamentacion\".\"sinonimos'
        managed = False
