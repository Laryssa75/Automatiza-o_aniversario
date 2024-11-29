from django.db import models


# Create your models here.

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    email= models.EmailField()
    data_nascimento = models.DateField()
    foto = models.ImageField(upload_to='foto/' , blank=True, null=True)
    arquivo_pdf = models.FileField(upload_to='pdf/' , blank=True, null=True)
    cbo = models.IntegerField(unique=True, null=True, blank=True)
    funcao = models.CharField(max_length=100, null=True)
    data_admissao = models.DateField(null=True, blank=True)
    id_tarefa_mail = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.cbo:
            max_cbo = Funcionario.objects.aggregate(models.Max('cbo'))['cbo__max']
            self.cbo = max_cbo +1 if max_cbo else 1
        super().save(*args, **kwargs)


    def __str__(self):
        return self.nome

    #Classe responsavel pelas liberações de acesso
    class Meta:
        permissions = [
            ("importar_funcionarios", "Pode importar funcionários")
        ]