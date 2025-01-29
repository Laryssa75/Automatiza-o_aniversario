import pandas as pd
import logging
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.utils import timezone
from django.db.utils import IntegrityError
from .models import Funcionario, UsuarioBasico
from .forms import FuncionarioForm, UploadExcelForm, UsuarioForm, LoginAcessoForm
from .tasks import enviar_email_aniversario
from .utils import obter_proximo_cbo, reorganizar_cbo, obter_proximo_idUSu, reorganizar_idUSu
from .decorators import verificar_permissaoAcesso
import traceback

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
            # usuario = request.POST.get('usuario')
            # senha_usuario = request.POST.get('password')
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

    #Formularios
    form_funcionario = FuncionarioForm(request.POST or None)
    form_import = UploadExcelForm(request.POST or None, request.FILES or None)

    tarefa_enfileirada = False #Variável para rastrear se a tarefa será enfileirada
    excel_file = None

    #Criação ou Edição de Funcionários     
    if cbo:
        funcionario = get_object_or_404(Funcionario, cbo=cbo)
        form_funcionario = FuncionarioForm(request.POST or None, instance=funcionario)

    if request.method == 'POST':
        # Envio de dados manual
        if 'manual' in request.POST:
            if form_funcionario.is_valid():
                print(f"{form_funcionario} é valido")
                funcionario = form_funcionario.save(commit=False)
                
                if not funcionario.cbo:
                    funcionario.cbo = obter_proximo_cbo()  # Atribui o próximo valor de cbo
                form_funcionario.save()  
                messages.success(request, "Funcionário criado com sucesso!")
                tarefa_enfileirada = True
                return redirect('funcionarios:menu_cadastros')
            else:
                # form_funcionario = FuncionarioForm(initial={'cbo': cbo})
                messages.error(request, "Erro ao criar funcionário.")

            
        #Se for envio de dados via arquivo excel
        elif 'import' in request.POST and request.FILES.get('excel_file'):
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
        'form_funcionario': form_funcionario, 
        'form_import': form_import,
        'cbo_gerado': obter_proximo_cbo(),
        'arquivo_excel': excel_file, 
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


def excluir_funcionario(request, cbo):
    if request.method == "POST":
        funcionario = get_object_or_404(Funcionario, cbo=cbo)
        funcionario.delete()
        reorganizar_cbo()
        messages.success(request, "Funcionário excluído com sucesso.")
    return redirect('funcionarios:menu_cadastros')


def menu_cadastros(request):
    #Buscar todos os funcionáris cadastrados
    funcionarios = Funcionario.objects.all()
    print(funcionarios)
    logging.info(funcionarios)
    return render(request, 'funcionarios/cadastros.html', {'funcionarios' : funcionarios})


#@verificar_permissaoAcesso
def criar_usuario(request, id_usuario=None):

    try:

        print("iniciando processo de criação de usuário...")
        
        idUsu_gerado = obter_proximo_idUSu()
        print(f"próximo id gerado: {idUsu_gerado}")

        if id_usuario:
            usuario = get_object_or_404(UsuarioBasico, id_usuario=id_usuario)
            form_usuario = UsuarioForm(request.POST or None, instance=usuario)
            print(f"editando usuário existente: {usuario.usuario}")

        else:
            form_usuario = UsuarioForm(request.POST or None)
            print("criando novo usuário")

        print(f"dados recebidos:", request.POST)
        if request.method == 'POST':
            if form_usuario.is_valid():
                print(f"formulário valido")
                usuario = form_usuario.save(commit=False)

                if not usuario.id_usuario:
                    usuario.id_usuario = obter_proximo_idUSu() #Atribui o próximo n de idUsu
            
                if form_usuario.cleaned_data.get('password'):
                    print("criptografando senha...")
                    usuario.set_password(form_usuario.cleaned_data['password'])

                usuario.save()
                print(f"{usuario.usuario} salvo com sucesso!")
                messages.success(request, "Usuário criado com sucesso!")
                return redirect('funcionarios:menu_usuarios')
            else:
                messages.error(request, "Erro ao criar usuário.")
                print(f"formulário inválido. Erros: ", form_usuario.errors)
        
        contexto = {
            'form_usuario': form_usuario,
            'idUsu_gerado': obter_proximo_idUSu(),
            'data_atual': timezone.now().date(),
        }

        return render(request, 'admin/criar_usuario.html', contexto)
    except Exception as e:
        print(f"Erro de validação {e}")
        messages.error(request, f"Erro ao criar usuário: {e}")
    except ValueError as e:
        print(f"Erro no banco de dados: {e}")
        messages.error(request, f"Erro de validação: {e}")
    except IntegrityError as e:
        print(f"Erro inesperado: {e}")
        print(traceback.format_exc())
        messages.error(request, f"Erro de banco de dados: {e}")


        return redirect('funcionarios:menu_usuarios')


def menu_usuarios(request):
    #Busca todos os funcionários cadastrados
    usuarios = UsuarioBasico.objects.all()
    print(usuarios)
    logging.info(usuarios)
    return render(request, 'admin/menu_usuarios.html', {'usuarios': usuarios})


#@verificar_permissaoAcesso
def menu_usuarios(request):
    usuarios = UsuarioBasico.objects.all()
    return render(request, 'admin/menu_usuarios.html', {'usuarios': usuarios})


def logout_and_redirect(request):
    logout(request)
    #return render (request, 'funcionarios/login.html') #esse caminho faz o caminho para o template login.html
    return redirect('funcionarios:login') #esse caminho faz o redirecionamento da url
