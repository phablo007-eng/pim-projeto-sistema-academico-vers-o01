"""
URL configuration for sistema_academico project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from sistema import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Páginas principais
    path('', views.home, name='home'),
    path('alunos/', views.lista_alunos, name='lista_alunos'),
    path('professores/', views.lista_professores, name='lista_professores'),
    path('coordenadores/', views.lista_coordenadores, name='lista_coordenadores'),
    path('turmas/', views.lista_turmas, name='lista_turmas'),
    path('turmas/<int:turma_id>/', views.detalhe_turma, name='detalhe_turma'),
    path('disciplinas/', views.lista_disciplinas, name='lista_disciplinas'),
  # Professor
    path('professor/turmas/', views.professor_minhas_turmas, name='professor_minhas_turmas'),
    path('professor/modulo/<int:modulo_id>/criar-atividade/', views.professor_criar_atividade, name='professor_criar_atividade'),
    path('professor/modulo/<int:modulo_id>/atividades/', views.professor_ver_atividades, name='professor_ver_atividades'),
    path('professor/entrega/<int:entrega_id>/corrigir/', views.professor_corrigir_entrega, name='professor_corrigir_entrega'),
    path('professor/modulo/<int:modulo_id>/lancar-notas/', views.professor_lancar_notas, name='professor_lancar_notas'),
    
    # Aluno
    path('aluno/atividades/', views.aluno_minhas_atividades, name='aluno_minhas_atividades'),
    path('aluno/atividade/<int:atividade_id>/entregar/', views.aluno_entregar_atividade, name='aluno_entregar_atividade'),
    path('aluno/notas/', views.aluno_minhas_notas, name='aluno_minhas_notas'),

    # API
    path('api/estatisticas/', views.api_estatisticas_notas, name='api_estatisticas_notas'),
    path('coordenador/turma/cadastrar/', views.coordenador_criar_turma, name='coordenador_criar_turma'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)