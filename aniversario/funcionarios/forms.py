from django import forms
from .models import Funcionario
from .models import Usuario

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'email', 'data_nascimento', 'data_admissao', 'funcao']
        exclude = ['cbo'] # excluio campo cbo do formulario para nao ser editado
       
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
    class Meta:
        model =  Usuario
        fields = ['usuario', 'senha_usuario', 'perfil','setor', 'data_criarUsu']
        widgets = {
            'perfil': forms.RadioSelect(choices=Usuario.TIPO_USUARIO),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'id_usuario' in self.fields:
            self.fields['id_usuario'].widget.attrs['readonly'] = True


    senha_usuario = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'Este campo é obrigatório.',
        }
    )

    #torna o campo id_usuario somente leitura
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if 'id_usuario' in self.fields:
    #         self.fields['id_usuario'].widget.attrs['readonly'] = True