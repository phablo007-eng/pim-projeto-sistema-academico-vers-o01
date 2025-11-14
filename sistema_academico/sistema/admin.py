from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
	Coordenador,
	Professor,
	Aluno,
	Disciplina,
	ProfessorDisciplina,
	Turma,
	TurmaDisciplina,
	Atividade,
	AlunoAtividade,
	Aula,
)
from .forms import AlunoAdminForm

# Configurações básicas de listagem para facilitar busca no admin.

class AlunoInline(admin.StackedInline):
	model = Aluno
	extra = 0
	can_delete = True

class ProfessorInline(admin.StackedInline):
	model = Professor
	extra = 0
	can_delete = True

class CoordenadorInline(admin.StackedInline):
	model = Coordenador
	extra = 0
	can_delete = True

# Estender o UserAdmin existente para adicionar inlines
class UsuarioAdmin(BaseUserAdmin):
	inlines = [AlunoInline, ProfessorInline, CoordenadorInline]

# Desregistrar o admin de Usuário padrão e registrar o nosso personalizado
admin.site.unregister(User)
admin.site.register(User, UsuarioAdmin)

@admin.register(Coordenador)
class CoordenadorAdmin(admin.ModelAdmin):
	list_display = ("usuario","usuario__email" , "telefone", "data_de_contratacao")
	search_fields = ("usuario__username","usuario__email", "usuario__first_name", "usuario__last_name")
	list_filter = ("data_de_contratacao",)
	raw_id_fields = ["usuario"]

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
	list_display = ("usuario","usuario__email" , "matricula", "titulacao", "data_de_contratacao")
	search_fields = ("usuario__username","usuario__email", "usuario__first_name", "usuario__last_name", "matricula")
	list_filter = ("titulacao", "data_de_contratacao")
	raw_id_fields = ["usuario"]

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
	form = AlunoAdminForm
	list_display = ("usuario", "matricula", "cpf", "data_de_nascimento")
	search_fields = ("usuario__username", "usuario__email", "usuario__first_name", "usuario__last_name", "matricula", "cpf")
	list_filter = ("data_de_nascimento",)
	raw_id_fields = ["usuario"]

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
	list_display = ("nome", "carga_horaria")
	search_fields = ("nome",)
	ordering = ("nome",)

@admin.register(ProfessorDisciplina)
class ProfessorDisciplinaAdmin(admin.ModelAdmin):
	list_display = ("id_professor", "id_disciplina")
	search_fields = ("id_professor__usuario__username", "id_professor__usuario__first_name", "id_professor__usuario__last_name", "id_disciplina__nome")
	list_filter = ("id_disciplina",)

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
	list_display = ("nome", "curso", "semestre", "id_coordenador")
	search_fields = ("nome", "curso", "semestre")
	list_filter = ("semestre", "curso")

@admin.register(TurmaDisciplina)
class TurmaDisciplinaAdmin(admin.ModelAdmin):
	list_display = ("id_turma", "id_disciplina", "id_professor", "data_inicio", "data_fim")
	search_fields = ("id_turma__nome", "id_disciplina__nome", "id_professor__usuario__username", "id_professor__usuario__first_name", "id_professor__usuario__last_name")
	list_filter = ("data_inicio", "data_fim")

@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
	list_display = ("id_turma_disciplina", "data", "descricao")
	search_fields = ("descricao", "id_turma_disciplina__id_disciplina__nome")
	list_filter = ("data",)

@admin.register(AlunoAtividade)
class AlunoAtividadeAdmin(admin.ModelAdmin):
	list_display = ("id_aluno", "id_atividade", "nota", "data_entrega")
	search_fields = ("id_aluno__usuario__username", "id_aluno__usuario__first_name", "id_aluno__usuario__last_name", "id_atividade__id_turma_disciplina__id_disciplina__nome")
	list_filter = ("data_entrega", "nota")

@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
	list_display = ("id_turma_disciplina", "data", "conteudo")
	search_fields = ("id_turma_disciplina__id_disciplina__nome", "conteudo")
	list_filter = ("data",)

