from django.db import models

# Create your models here.
class Keyword(models.Model):
    id = models.AutoField(primary_key = True)
    palabra = models.CharField(max_length = 30)
    stem = models.CharField(max_length = 30)
    class Meta:
        db_table = 'reglamentacion\".\"keywords'
        managed = False
