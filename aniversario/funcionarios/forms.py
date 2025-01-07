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
