from django.db import models
from datetime import date

# Create your models here.
class Documento(models.Model):
    iddocumento = models.AutoField(primary_key = True)
    nro = models.CharField(max_length = 20)
    fecha = models.DateField(default=date.today())
    descripcion=models.CharField(max_length=50, null=False)
    texto=models.TextField()
    tipo =models.CharField(max_length=30, choices=[('ley', 'Ley'),('reglamentacion informal', 'Reglamentacion Informal'),('ordenanza', 'Ordenanza'),('jurisprudencia', 'Jurisprudencia'),('acta', 'Acta'),('resolucion', 'Resolucion'),('estatuto', 'Estatuto'),('otra', 'Otra')])
    class Meta:
        db_table = 'reglamentacion\".\"documentos'
        managed = False