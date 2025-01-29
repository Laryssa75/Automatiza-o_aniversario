from django import forms
from .models import Funcionario
from .models import UsuarioBasico

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'email', 'data_nascimento', 'data_admissao', 'funcao']
       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'cbo' in self.fields:
            self.fields['cbo'].widget.attrs['readonly'] = True
    

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite um e-mail válido'
        }),
        error_messages={
            'invalid':'Por favor, insira um endereço de e-mail válido.',
            'required': 'Este campo é obrigatório',
        }
    )

    #Definindo um widget para data com formato customizado
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%d/%m/%Y'),
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],
        error_messages={
            'invalid': 'Insira uma data válida no formato DD/MM/YYYY.',
            'required': 'Este campo é obrigatório.',
        }
    )
    data_admissao = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control'}, format='%d/%m/%Y'),
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],
        error_messages={
            'invalid': 'Insira uma data válida no formato DD/MM/YYYY.',
        }
    )


class UploadExcelForm(forms.Form):
    excel_file = forms.FileField(
        label="Selecione o arquivo Excel",
        error_messages={
            'required': 'Por favor, selecione um arquivo.',
            'invalid': 'Envie um arquivo válido.',
        })
    
    #Validação para garantir que o arquivo seja excel
    def validacao_excel_file(self):
        excel_file = self.cleaned_data.get('excel_file')
        if not excel_file.name.endswith(('.xls', '.xlsx')):
            raise forms.ValidationError("O arquivo deve ser no formato .xls ou .xlsx.")
        #Retorna o arquivo validando
        return excel_file


class UsuarioForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha'}), label="Senha")  

    class Meta:
        model =  UsuarioBasico
        fields = ['usuario', 'perfil','setor', 'data_criarUsu', 'password']
        widgets = {
            'perfil': forms.RadioSelect(choices=UsuarioBasico.TIPO_USUARIO),
            'data_criarUsu': forms.DateInput(attrs={'type': 'date'}),
        }

    #torna o campo id_usuario somente leitura
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'id_usuario' in self.fields:
            self.fields['id_usuario'].widget.attrs['readonly'] = True

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 3:
            print("a senha deve ter pelo menos 3 caracteres")
            raise forms.ValidationError("A senha deve ter pelo menos 15 caracteres.")
        # Adicione validações extras se necessário
        return password

    # Garantindo que a senha seja corretamente armazenada de forma criptografada
    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])  # Usa o set_password para criptografar a senha
        if commit:
            user.save()
        return user

class LoginAcessoForm(forms.Form):
    usuario = forms.CharField(
        max_length=150,
        label="Usuário",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuário'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
        label="Senha"
    )


