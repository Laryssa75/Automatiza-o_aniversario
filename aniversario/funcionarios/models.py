from django.db import models

# Create your models here.

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    email= models.EmailField()
    data_nascimento = models.DateField()
    foto = models.ImageField(upload_to='foto/' , blank=True, null=True)
    arquivo_pdf = models.FileField(upload_to='pdf/' , blank=True, null=True)
    cbo = models.IntegerField()
    funcao = models.CharField(max_length=100)
    data_admissao = models.DateField(null=True, blank=True)


    def __str__(self):
        return self.nome
