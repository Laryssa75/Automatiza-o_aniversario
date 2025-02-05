from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Funcionario(models.Model):
    nome = models.CharField(max_length=100,  unique=True)
    email= models.EmailField()
    data_nascimento = models.DateField()
    foto = models.ImageField(upload_to='foto/' , blank=True, null=True)
    arquivo_pdf = models.FileField(upload_to='pdf/' , blank=True, null=True)
    cbo = models.AutoField(primary_key=True)
    funcao = models.CharField(max_length=100, null=True)
    data_admissao = models.DateField(null=True, blank=True, default=timezone.now)
    id_tarefa_mail = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nome

    #Classe responsavel pelas liberações de acesso
    class Meta:
        permissions = [
            ("cadastrar_funcionarios", "Pode cadastrar funcionários")
        ]

class GerenciadorUsuarios(BaseUserManager):
    def criar_usuario(self, usuario, perfil, password,  **extra_fields):
        if not usuario:
            raise ValueError("O campo 'usuario' é obrigatório .")
        if not perfil:
            raise ValueError("O campo 'perfil' é obrigatório. ")
        
        user = self.model(
            usuario=usuario,
            perfil=perfil,
            data_criarUsu = timezone.now(),
            **extra_fields
        )
        if password:
            user.set_password(password)
        user.save(using = self._db)
        return user
    
    def UsuarioAdmin(self, usuario, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('perfil', 'admin')
        return self.criar_usuario(usuario, password, perfil="admin",  **extra_fields)


class UsuarioBasico(AbstractBaseUser, PermissionsMixin):

    TIPO_USUARIO = [
        ('admin', 'Administrador'),
        ('basico', 'Básico'),
    ]

    usuario = models.CharField(
        max_length=150,
        blank=False,
        unique=True,
        null=False,
        verbose_name="Usuário",
        help_text="Digite um nome de usuário com digitos e números.")
    id_usuario = models.AutoField(primary_key=True)
    perfil = models.CharField(max_length=50, choices=TIPO_USUARIO, default='basico')
    setor = models.CharField(max_length=100)
    data_criarUsu = models.DateField(null=True, blank=True, default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'usuario'

    REQUIRED_FIELDS = ['perfil']

    objects = GerenciadorUsuarios()

    def __str__(self):
        return self.usuario if self.usuario else f"Usuário {self.id_usuario}"
    
    @property
    def is_staff(self):
        return self.is_admin