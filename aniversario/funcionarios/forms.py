from django import forms
from .models import Funcionario

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'email', 'data_nascimento', 'data_admissao', 'funcao']


class UploadExcelForm(forms.Form):
    excel_file = forms.FileField(label="Selecione o arquivo Excel")