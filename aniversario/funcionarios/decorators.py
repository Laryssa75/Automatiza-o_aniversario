from django.shortcuts import redirect

def verificar_permissaoAcesso(view_func):
    def verifica_acesso(request, *args, **kwargs):
        usuario_logado = request.user
        
        if not usuario_logado.is_authenticated:
            return redirect('login')
        
        # paginas_permitidas = [
        #     '/menu_usuarios/',
        #     '/cadastros/',
        #     '/cadastrar_funcionario/'
        # ]
        
        # if usuario_logado.perfil == 'basico' and request.path not in paginas_permitidas:
        #     return redirect('menu_usuarios')

        if usuario_logado.perfil == 'basico':
            if request.path != '/criar_usuarios/':
                return redirect('criar_usuarios')
            

        return view_func(request, *args, **kwargs)

    return verifica_acesso    