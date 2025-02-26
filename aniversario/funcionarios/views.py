import pandas as pd
import logging
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.utils import timezone
from urllib.parse import unquote
from django.db.utils import IntegrityError
from .models import Funcionario, UsuarioBasico
from .forms import FuncionarioForm, UploadExcelForm, UsuarioForm, LoginAcessoForm
from .tasks import enviar_email_aniversario
from .utils import obter_proximo_cbo, obter_proximo_idUSu
from .decorators import verificar_permissaoAcesso

#serve para disparar envio de email manualmente
# async def enviar_emails_aniversariantes_view(request):
#     await asyncio.to_thread(enviar_email_aniversario.apply_async)
#     return JsonResponse({"status": "sucess", "message": "E-mails de aniversariantes enviados."})

logger = logging.getLogger(__name__)

def home(request):
    #return HttpResponse("Página inicial do app funcionários")
    return render(request, 'funcionarios/home.html')


def login_view(request):
    if request.method == 'POST':
        form_usuario = LoginAcessoForm(request.POST)

        if form_usuario.is_valid():
            usuario = form_usuario.cleaned_data["usuario"]
            password = form_usuario.cleaned_data["password"]

            user = authenticate(request, username=usuario, password=password)

            if user is not None:
                login(request, user)
                if user.is_admin: 
                    return redirect('admin:index') #Redireciona para o painel de admin
                else:
                    return redirect('funcionarios:cadastrar_funcionarios')  
            else:        
                #Caso o login falhe
                messages.error(request, "Usuário ou senha inválidos.")
                return render(request, 'funcionarios/login.html') 

    else:
        #caso o método seja GET, cria o formulário vazio
        form_usuario = LoginAcessoForm() 

    contexto = {
        "form_usuario": form_usuario,
    }  

    return render(request, 'funcionarios/login.html', contexto) 


#@permission_required('funcionarios.cadastrar_funcionarios', raise_exception=True)
def cadastrar_funcionarios(request, cbo=None):
    funcionario = None

    tarefa_enfileirada = False #Variável para rastrear se a tarefa será enfileirada
      
    if cbo:
        try:
            funcionario = get_object_or_404(Funcionario, cbo=cbo)
        except Funcionario.DoesNotExist:
            messages.error(request, "Funcionário não encontrado!")
    
    form_funcionario = FuncionarioForm(request.POST or None, instance=funcionario)


    if request.method == "POST":

        if form_funcionario.is_valid():
            funcionario = form_funcionario.save(commit=False)
            
            if not funcionario.cbo:
                funcionario.cbo = obter_proximo_cbo()

            funcionario.save()
            messages.success(request, "Funcionário criado com sucesso!")
            tarefa_enfileirada = True
            return redirect('funcionarios:menu_cadastros')
        else:
            # form_funcionario = FuncionarioForm(initial={'cbo': cbo})
            messages.error(request, "Erro ao criar funcionário.")
            print("erros no formulário", form_funcionario.errors)

            #Chama a tarefa celery para envio de email de aniversario
            #enviar_email_aniversario.apply_async()
            #return redirect('funcionarios:cadastrar_funcionarios')
            
    # ** Enfileira a tarefa após as operações de criação **
    if tarefa_enfileirada:
        enviar_email_aniversario.apply_async()

    contexto = {
        'form_funcionario': form_funcionario, 
        'cbo_gerado': obter_proximo_cbo(),
        'data_atual': timezone.now().date(), 
    }
    return render(request, 'funcionarios/cadastrar_funcionario.html', contexto)


def cadastrar_funcionarioExcel(request, cbo=None):
    form_import = UploadExcelForm(request.POST or None, request.FILES or None) 

    tarefa_enfileirada = False #Variável para rastrear se a tarefa será enfileirada
    excel_file = None

    #Criação ou Edição de Funcionários     
    if cbo:
        funcionario = get_object_or_404(Funcionario, cbo=cbo)
        form_import = UploadExcelForm(request.POST or None, instance=funcionario)

    #Se for envio de dados via arquivo excel
    if request.method == "POST" and request.FILES.get('excel_file'):
                form_import = UploadExcelForm(request.POST, request.FILES)
                if form_import.is_valid():
                    excel_file = request.FILES['excel_file']
                    try:
                        df = pd.read_excel(excel_file)

                        for _, row in df.iterrows():
                            if 'NOME' in row and 'EMAIL' in row and 'DATA NASCIMENTO' in row:
                                Funcionario.objects.create(
                                    nome=row['Nome'],
                                    email=row['Email'],
                                    data_nascimento=row['Data Nascimento'],
                                    data_admissao=row.get('Data Admissão', None),
                                    funcao=row.get('Função', None),
                                    cbo=obter_proximo_cbo() #atribui o próximo valor de id sequencial
                                )

                                tarefa_enfileirada = True #Marca que a tarefa será enfileirada

                            else:
                                messages.error(request, "Arquivo inválido: algumas colunas estão faltando.")
                                break
                            messages.success(request, "Funcionarios importados com sucesso!")
                            print("Funcionarios importados com sucesso!")


                        #return redirect('funcionarios:cadastrar_funcionarios')

                        #Chama a tarefa celery para envio de email de aniversario
                        #enviar_email_aniversario.apply_async()
                
                    except Exception as e:
                        messages.error(request, f"Erro ao cadastrar os dados os funcionários: {e}")
                        print("Erro ao cadastrar o arquivo excel!")


    # ** Enfileira a tarefa após as operações de criação **
    if tarefa_enfileirada:
        enviar_email_aniversario.apply_async()

    contexto = {
        'form_import': form_import,
        'cbo_gerado': obter_proximo_cbo(),
        'arquivo_excel': excel_file
    }
    return render(request, 'funcionarios/cadastrar_funcionario.html', contexto)


def editar_funcionarios(request, cbo):
    # Busca o funcionário com o 'cbo' fornecido
    funcionario = get_object_or_404(Funcionario, cbo=cbo)
    print(f"Dados do funcionário: {funcionario.nome}, {funcionario.email}, {funcionario.data_nascimento}")

    if request.method == 'POST':

        form_editar = FuncionarioForm(request.POST, instance=funcionario)
    
        if form_editar.is_valid():
            form_editar.save()  # Salva o funcionário com os dados corrigidos
            messages.success(request, "Funcionário alterado com sucesso.")
            return redirect('funcionarios:menu_cadastros')
        else:
            messages.error(request, "Falha ao editar o cadastro do funcionário.")
            print(f"Erros ao editar: {form_editar.errors}")  # Para depuração
    
    else:
        # Se for um GET, cria o formulário com os dados do funcionário
        form_editar = FuncionarioForm(instance=funcionario)

    # Retorna o formulário no caso de GET ou erro de validação
    return render(request, 'funcionarios/cadastrar_funcionario.html', {
        'form_funcionario': form_editar,
    })
    
    # else:
    #     # Quando o método não for POST, preenche o formulário com os dados do funcionário
    #     form_editar = FuncionarioForm(instance=funcionario)

    #     return render(request, 'funcionarios/cadastrar_funcionario.html', {
    #         'form_funcionario': form_editar,
    #     })


def excluir_funcionario(request, nome_funcionario):
    nome_funcionario = unquote(nome_funcionario)
    if request.method == "POST":
        funcionario = get_object_or_404(Funcionario, nome=nome_funcionario)
        funcionario.delete()
        messages.success(request, "Funcionário excluído com sucesso.")
        print(f"Funcionário {funcionario.nome} excluído com sucesso.")
    return redirect('funcionarios:menu_cadastros')


def menu_cadastros(request):
    #Buscar todos os funcionáris cadastrados
    funcionarios = Funcionario.objects.all().order_by('data_admissao')
    print(funcionarios)
    logging.info(funcionarios)
    return render(request, 'funcionarios/cadastros.html', {'funcionarios' : funcionarios})


#@verificar_permissaoAcesso
def criar_usuario(request, id_usuario=None):
    usuario = None
    erro_usuario = None

    idUsu_gerado = obter_proximo_idUSu()

    if id_usuario:
        try:
            usuario = get_object_or_404(UsuarioBasico, id_usuario=id_usuario)
        except UsuarioBasico.DoesNotExist:
            erro_usuario = "Usuário não encontrado!"

    form_usuario = UsuarioForm(request.POST or None, instance=usuario)


    if request.method == 'POST':
        if form_usuario.is_valid():
            usuario = form_usuario.save(commit=False)

            if not usuario.id_usuario:
                usuario.id_usuario = obter_proximo_idUSu() #Atribui o próximo n de idUsu
        
            if form_usuario.cleaned_data.get('password'):
                usuario.set_password(form_usuario.cleaned_data['password'])

            usuario.save()
            print(f"{usuario.usuario} salvo com sucesso!")
            return redirect('funcionarios:menu_usuarios')
        else:
            messages.error(request, "Erro ao criar usuário.")
            print(f"formulário inválido. Erros: ", form_usuario.errors)
    
    contexto = {
        'form_usuario': form_usuario,
        'idUsu_gerado': obter_proximo_idUSu(),
        'data_atual': timezone.now().date(),
        'erro_usuario': erro_usuario,
    }

    return render(request, 'admin/criar_usuario.html', contexto)


def menu_usuarios(request):
    #Busca todos os funcionários cadastrados
    usuarios = UsuarioBasico.objects.all().order_by('data_criarUsu')
    print(usuarios)
    logging.info(usuarios)
    return render(request, 'admin/menu_usuarios.html', {'usuarios': usuarios})

def excluir_usuario(request, nome_usuario):
    nome_usuario = unquote(nome_usuario)
    if request.method == "POST":
        usuario = get_object_or_404(UsuarioBasico, usuario = nome_usuario)
        usuario.delete()
        messages.success(request, "Usuário excluído com sucesso.")
    return redirect('funcionarios:menu_usuarios')

def editar_usuario(request, id_usuario):
    #Buscar o usuário com o 'id_usuario' fornecido
    usuario = get_object_or_404(UsuarioBasico, id_usuario=id_usuario)
    print(f"Dados do usuário: {usuario.usuario}, {usuario.perfil}, {usuario.id_usuario}")

    if request.method == 'POST':
        form_editar = UsuarioForm(request.POST, instance=usuario)

        if form_editar.is_valid():
            form_editar.save()
            messages.success(request, "Usuario alterado com sucesso.")
            return redirect('funcionarios:menu_usuarios')
        else:
            messages.error(request, "Falha ao editar o cadastro do usuário.")
            print(f"Erros ao editar: {form_editar.errors}")

    else:
        #Se for um GET, cria o formulário com os dados do usuário
        form_editar = UsuarioForm(instance=usuario)

    #Retorna o formulário no caso de GET ou erro de validação
    return render(request, 'admin/criar_usuario.html', {
        'form_usuario': form_editar,
        'data_atual': timezone.now().date(),
    })

def logout_and_redirect(request):
    logout(request)
    #return render (request, 'funcionarios/login.html') #esse caminho faz o caminho para o template login.html
    return redirect('funcionarios:login') #esse caminho faz o redirecionamento da url
