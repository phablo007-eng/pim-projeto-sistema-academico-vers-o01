from django import forms
from .models import Aluno, Atividade, AlunoAtividade, Turma, Coordenador

class AlunoAdminForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = "__all__"
        widgets = {
            # HTML5 date picker evita erros de formato (envia YYYY-MM-DD)
            "data_de_nascimento": forms.DateInput(attrs={"type": "date"}),
        }

class AtividadeForm(forms.ModelForm):
    """Form para professor criar atividade"""
    class Meta:
        model = Atividade
        fields = ['data', 'descricao']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Descreva a atividade...'}),
        }
        labels = {
            'data': 'Data de entrega',
            'descricao': 'Descrição da atividade',
        }

class EntregaAtividadeForm(forms.ModelForm):
    """Form para aluno entregar atividade (arquivo ou texto)."""
    class Meta:
        model = AlunoAtividade
        fields = ['arquivo', 'resposta_texto']  # nota e data_entrega automáticos
        widgets = {
            'resposta_texto': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Digite sua resposta textual (opcional se enviar arquivo)'
            }),
        }
        labels = {
            'arquivo': 'Arquivo (PDF, DOCX, IMG...)',
            'resposta_texto': 'Resposta textual',
        }

class CorrecaoForm(forms.ModelForm):
    """Form para professor corrigir entrega"""
    class Meta:
        model = AlunoAtividade
        fields = ['nota']
        widgets = {
            'nota': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '10',
                'step': '0.1',
                'placeholder': '0.0 a 10.0'
            })
        }
        labels = {
            'nota': 'Nota (0 a 10)',
        }

class TurmaForm(forms.ModelForm):
    """Form para coordenador criar turma"""
    class Meta:
        model = Turma
        fields = ['nome', 'semestre', 'curso', 'id_coordenador']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da turma'}),
            'semestre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 2025.2'}),
            'curso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Curso'}),
            'id_coordenador': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome': 'Nome da Turma',
            'semestre': 'Semestre',
            'curso': 'Curso',
            'id_coordenador': 'Coordenador Responsável',
        }