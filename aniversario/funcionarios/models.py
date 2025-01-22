from django.db import models
from django.core.validators import RegexValidator


class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    email= models.EmailField()
    data_nascimento = models.DateField(null=False, blank=False)
    foto = models.ImageField(upload_to='foto/' , blank=True, null=True)
    arquivo_pdf = models.FileField(upload_to='pdf/' , blank=True, null=True)
    cbo = models.AutoField(primary_key=True)
    funcao = models.CharField(max_length=100, null=True)
    data_admissao = models.DateField(null=True, blank=True)
    id_tarefa_mail = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nome

    #Classe responsavel pelas liberações de acesso
    class Meta:
        permissions = [
            ("cadastrar_funcionarios", "Pode cadastrar funcionários")
        ]

class Usuario(models.Model):
    #Validador para caracteres alfanuméricos
    VALIDADOR_ALFANUMERICO = RegexValidator(
        regex=r'^[a-zA-Z0-9]*$',
        message="Este campo deve conter apenas letras e números." 
    )

    TIPO_USUARIO = [
        ('admin', 'Administrador'),
        ('basico', 'Básico'),
    ]

    usuario = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        validators=[VALIDADOR_ALFANUMERICO],
        help_text="Digite um nome de usuário alfanumérico.")
    id_usuario = models.AutoField(primary_key=True)
    senha_usuario = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        validators=[VALIDADOR_ALFANUMERICO],
        help_text="Crie uma senha segura."
        )
    perfil = models.CharField(max_length=50, choices=TIPO_USUARIO, default='basico')
    setor = models.CharField(max_length=100)
    data_criarUsu = models.DateField(null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     #Atribui a senha criptografada, se for nova
    #     if not self.pk:
    #         self.senha_usuario = make_password(self.senha_usuario)

    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.usuario if self.usuario else f"Usuário {self.id_usuario}"