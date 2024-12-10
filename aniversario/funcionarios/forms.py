from django import forms
from .models import Funcionario

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'email', 'data_nascimento', 'data_admissao', 'funcao']
        exclude = ['cbo'] # excluio campo cbo do formulario para nao ser editado

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

class UploadExcelForm(forms.Form):
    excel_file = forms.FileField(label="Selecione o arquivo Excel")