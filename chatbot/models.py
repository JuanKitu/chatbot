__author__ = 'roloprogramating'
from django.db import models


class Question(models.Model):
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=500)
    sessionid = models.CharField(max_length=500)


class Answer(models.Model):
    type = models.CharField(max_length=500)
    text = models.CharField(max_length=5000)
    content = models.CharField(max_length=5000)


class KnownQuestion(models.Model):
    text = models.CharField(max_length=5000)
    answer = models.ForeignKey(Answer, null=True)



class Sinonimos(models.Model):
    id = models.AutoField(primary_key=True)
    palabra = models.CharField(max_length=30)
    sinonimo = models.CharField(max_length=30)
    peso = models.FloatField()

    class Meta:
        db_table = 'reglamentacion\".\"sinonimos'
        managed = False
