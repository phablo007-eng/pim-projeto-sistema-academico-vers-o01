from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from .models import (
    Aluno,
    AlunoAtividade,
    AlunoModulo,
    Atividade,
    Coordenador,
    Disciplina,
    Professor,
    Turma,
    TurmaDisciplina,
)
from .forms import AtividadeForm, EntregaAtividadeForm, CorrecaoForm, TurmaForm

# Views de Autenticação

def _get_professor(request):
    try:
        return Professor.objects.get(usuario=request.user)
    except Professor.DoesNotExist:
        messages.error(request, 'Você não está cadastrado como professor.')
        return None


def _get_aluno(request):
    try:
        return Aluno.objects.get(usuario=request.user)
    except Aluno.DoesNotExist:
        messages.error(request, 'Você não está cadastrado como aluno.')
        return None

# Views de Autenticação

def login_view(request):
    """View de login"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo(a), {user.get_full_name() or user.username}!')
            
            # Redirecionar para a página solicitada ou home
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    
    return render(request, 'sistema/login.html')


def logout_view(request):
    """View de logout"""
    logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('login')


# Views Públicas (Dashboard)

def home(request):
    """Página inicial com estatísticas gerais do sistema"""
    context = {
        'total_alunos': Aluno.objects.count(),
        'total_professores': Professor.objects.count(),
        'total_turmas': Turma.objects.count(),
        'total_disciplinas': Disciplina.objects.count(),
    }
    return render(request, 'sistema/home.html', context)

# Views Protegidas (requerem login)

@login_required
def lista_alunos(request):
    """Lista todos os alunos cadastrados"""
    alunos = Aluno.objects.select_related('usuario').all()
    return render(request, 'sistema/lista_alunos.html', {'alunos': alunos})


@login_required
def lista_professores(request):
    """Lista todos os professores cadastrados"""
    professores = Professor.objects.select_related('usuario').all()
    return render(request, 'sistema/lista_professores.html', {'professores': professores})


@login_required
def lista_coordenadores(request):
    """Lista todos os coordenadores cadastrados"""
    coordenadores = Coordenador.objects.select_related('usuario').all()
    return render(request, 'sistema/lista_coordenadores.html', {'coordenadores': coordenadores})


@login_required
def lista_turmas(request):
    """Lista todas as turmas com coordenadores"""
    turmas = Turma.objects.select_related('id_coordenador__usuario').prefetch_related('alunos').all()
    return render(request, 'sistema/lista_turmas.html', {'turmas': turmas})


@login_required
def detalhe_turma(request, turma_id):
    """Exibe detalhes de uma turma específica: alunos, disciplinas, atividades"""
    turma = get_object_or_404(Turma.objects.prefetch_related('alunos__usuario', 'modulos__id_disciplina', 'modulos__id_professor__usuario'), pk=turma_id)
    
    context = {
        'turma': turma,
        'alunos': turma.alunos.all(),
        'modulos': turma.modulos.all(),
    }
    return render(request, 'sistema/detalhe_turma.html', context)


@login_required
def lista_disciplinas(request):
    """Lista todas as disciplinas"""
    disciplinas = Disciplina.objects.all()
    return render(request, 'sistema/lista_disciplinas.html', {'disciplinas': disciplinas})


# ==================== VIEWS PARA PROFESSORES ====================

@login_required
def professor_minhas_turmas(request):
    """Lista as turmas/módulos em que o professor leciona"""
    professor = _get_professor(request)
    if not professor:
        return redirect('home')
    
    # Módulos (TurmaDisciplina) onde este professor leciona
    modulos = TurmaDisciplina.objects.filter(id_professor=professor).select_related('id_turma', 'id_disciplina')
    
    return render(request, 'sistema/professor_turmas.html', {
        'professor': professor,
        'modulos': modulos
    })


@login_required
def professor_criar_atividade(request, modulo_id):
    """Professor cria uma atividade para um módulo (turma+disciplina)"""
    professor = _get_professor(request)
    if not professor:
        return redirect('home')
    
    modulo = get_object_or_404(TurmaDisciplina, pk=modulo_id)
    
    # Verificar se o professor leciona este módulo
    if modulo.id_professor != professor:
        messages.error(request, 'Você não tem permissão para criar atividades neste módulo.')
        return redirect('professor_minhas_turmas')
    
    if request.method == 'POST':
        form = AtividadeForm(request.POST)
        if form.is_valid():
            atividade = form.save(commit=False)
            atividade.id_turma_disciplina = modulo
            atividade.save()
            messages.success(request, f'Atividade criada com sucesso para {modulo.id_turma.nome} - {modulo.id_disciplina.nome}!')
            return redirect('professor_ver_atividades', modulo_id=modulo.id)
    else:
        form = AtividadeForm()
    
    return render(request, 'sistema/professor_criar_atividade.html', {
        'form': form,
        'modulo': modulo
    })


@login_required
def professor_ver_atividades(request, modulo_id):
    """Professor vê todas as atividades de um módulo e suas entregas"""
    professor = _get_professor(request)
    if not professor:
        return redirect('home')
    
    modulo = get_object_or_404(TurmaDisciplina, pk=modulo_id)
    
    # Verificar permissão
    if modulo.id_professor != professor:
        messages.error(request, 'Você não tem permissão para ver estas atividades.')
        return redirect('professor_minhas_turmas')
    
    atividades = Atividade.objects.filter(id_turma_disciplina=modulo).prefetch_related('entregas__id_aluno__usuario')
    
    return render(request, 'sistema/professor_atividades.html', {
        'modulo': modulo,
        'atividades': atividades
    })


@login_required
def professor_corrigir_entrega(request, entrega_id):
    """Professor corrige (dá nota) a uma entrega de atividade"""
    professor = _get_professor(request)
    if not professor:
        return redirect('home')
    
    entrega = get_object_or_404(AlunoAtividade.objects.select_related(
        'id_atividade__id_turma_disciplina__id_professor',
        'id_atividade__id_turma_disciplina__id_turma',
        'id_atividade__id_turma_disciplina__id_disciplina',
        'id_aluno__usuario'
    ), pk=entrega_id)
    
    # Verificar se o professor leciona o módulo desta atividade
    if entrega.id_atividade.id_turma_disciplina.id_professor != professor:
        messages.error(request, 'Você não tem permissão para corrigir esta entrega.')
        return redirect('professor_minhas_turmas')
    
    if request.method == 'POST':
        form = CorrecaoForm(request.POST, instance=entrega)
        if form.is_valid():
            form.save()
            messages.success(request, f'Nota atribuída com sucesso para {entrega.id_aluno.usuario.get_full_name()}!')
            return redirect('professor_ver_atividades', modulo_id=entrega.id_atividade.id_turma_disciplina.id)
    else:
        form = CorrecaoForm(instance=entrega)
    
    return render(request, 'sistema/professor_corrigir.html', {
        'form': form,
        'entrega': entrega
    })


# ==================== VIEWS PARA ALUNOS ====================

@login_required
def aluno_minhas_atividades(request):
    """Aluno vê todas as atividades das suas turmas"""
    aluno = _get_aluno(request)
    if not aluno:
        return redirect('home')
    
    # Turmas em que o aluno está matriculado
    turmas = aluno.turmas.all()
    
    # Atividades de todos os módulos dessas turmas
    atividades = Atividade.objects.filter(
        id_turma_disciplina__id_turma__in=turmas
    ).select_related(
        'id_turma_disciplina__id_turma',
        'id_turma_disciplina__id_disciplina',
        'id_turma_disciplina__id_professor__usuario'
    ).prefetch_related('entregas').order_by('-data')
    
    # Adicionar info se o aluno já entregou cada atividade
    for atividade in atividades:
        atividade.minha_entrega = atividade.entregas.filter(id_aluno=aluno).first()
    
    return render(request, 'sistema/aluno_atividades.html', {
        'aluno': aluno,
        'atividades': atividades
    })


@login_required
def aluno_entregar_atividade(request, atividade_id):
    """Aluno faz a entrega de uma atividade"""
    aluno = _get_aluno(request)
    if not aluno:
        return redirect('home')
    
    atividade = get_object_or_404(Atividade.objects.select_related(
        'id_turma_disciplina__id_turma',
        'id_turma_disciplina__id_disciplina'
    ), pk=atividade_id)
    
    # Verificar se o aluno está matriculado na turma
    if not aluno.turmas.filter(id=atividade.id_turma_disciplina.id_turma.id).exists():
        messages.error(request, 'Você não está matriculado nesta turma.')
        return redirect('aluno_minhas_atividades')
    
    # Verificar se já entregou
    entrega_existente = AlunoAtividade.objects.filter(
        id_aluno=aluno,
        id_atividade=atividade
    ).first()
    
    if entrega_existente:
        messages.warning(request, 'Você já entregou esta atividade.')
        return redirect('aluno_minhas_atividades')
    
    if request.method == 'POST':
        form = EntregaAtividadeForm(request.POST, request.FILES)
        if form.is_valid():
            entrega = form.save(commit=False)
            entrega.id_aluno = aluno
            entrega.id_atividade = atividade
            entrega.data_entrega = timezone.now()
            entrega.save()
            messages.success(request, 'Atividade entregue com sucesso!')
            return redirect('aluno_minhas_atividades')
    else:
        form = EntregaAtividadeForm()
    
    return render(request, 'sistema/aluno_entregar.html', {
        'form': form,
        'atividade': atividade
    })


@login_required
def aluno_minhas_notas(request):
    """Aluno vê suas notas de provas (P1/P2) por módulo e a média/status.
    Lista registros de AlunoModulo do aluno logado.
    """
    aluno = _get_aluno(request)
    if not aluno:
        return redirect('home')

    registros = (
        AlunoModulo.objects
        .filter(id_aluno=aluno)
        .select_related(
            'id_turma_disciplina__id_turma',
            'id_turma_disciplina__id_disciplina'
        )
        .order_by('id_turma_disciplina__id_turma__nome', 'id_turma_disciplina__id_disciplina__nome')
    )

    # Classificação simples de risco (evidência de lógica "IA" baseada em regras)
    # Regras:
    # - Sem média (pendente) e P1 < 5 => risco_moderado
    # - Média < 5 => risco_alto
    # - Média < 7 => risco_moderado
    # - Média >= 7 => ok
    for r in registros:
        media = r.media_final
        p1 = r.nota_prova1
        p2 = r.nota_prova2
        if media is None:
            if p1 is not None and p1 < 5 and p2 is None:
                r.risco = 'moderado'
                r.recomendacao = 'Reforce estudos antes da P2 (P1 abaixo de 5).'
            else:
                r.risco = 'pendente'
                r.recomendacao = 'Aguarde lançamento de ambas as provas.'
        else:
            if media < 5:
                r.risco = 'alto'
                r.recomendacao = 'Procure monitoria e revise conteúdos fundamentais.'
            elif media < 7:
                r.risco = 'moderado'
                r.recomendacao = 'Aprimore revisão para elevar média acima de 7.'
            else:
                r.risco = 'ok'
                r.recomendacao = 'Bom desempenho. Mantenha o ritmo.'

    return render(request, 'sistema/aluno_notas.html', {
        'aluno': aluno,
        'registros': registros,
    })


# ==================== API: Estatísticas via C ====================

@csrf_exempt
def api_estatisticas_notas(request):
    """Endpoint API que calcula estatísticas de uma lista de notas usando a DLL C.
    POST JSON: { "notas": [7.5, 8.0, 5.0] }
    Resposta: { "media": 7.5, "minimo": 5.0, "maximo": 8.0, "quantidade": 3 }
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('Use POST com JSON {"notas": [...]}')

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except Exception:
        return HttpResponseBadRequest('JSON inválido')

    notas = payload.get('notas')
    if not isinstance(notas, list):
        return HttpResponseBadRequest('Campo "notas" deve ser uma lista')

    # Sanitiza/filtra valores não numéricos
    try:
        notas_float = [float(x) for x in notas if x is not None]
    except (TypeError, ValueError):
        return HttpResponseBadRequest('A lista "notas" deve conter números')

    # Chama wrapper C
    try:
        from c.notas_basico_wrapper import calcular_stats
        dados = calcular_stats(notas_float)
        dados['quantidade'] = len(notas_float)
        return JsonResponse(dados)
    except FileNotFoundError as e:
        return JsonResponse({'erro': str(e)}, status=500)
    except Exception as e:
        return JsonResponse({'erro': f'Falha ao calcular estatísticas: {e}'}, status=500)


# ==================== PROFESSOR: Lançar notas (duas provas) ====================

@login_required
def professor_lancar_notas(request, modulo_id):
    """Tela para o professor lançar p1/p2 por aluno do módulo e calcular média/status via C."""
    professor = _get_professor(request)
    if not professor:
        return redirect('home')

    modulo = get_object_or_404(TurmaDisciplina.objects.select_related('id_turma', 'id_disciplina', 'id_professor__usuario'), pk=modulo_id)

    if modulo.id_professor != professor:
        messages.error(request, 'Você não tem permissão para lançar notas neste módulo.')
        return redirect('professor_minhas_turmas')

    # Garante registros AlunoModulo para cada aluno da turma
    alunos = modulo.id_turma.alunos.select_related('usuario').all()
    for aluno in alunos:
        AlunoModulo.objects.get_or_create(id_aluno=aluno, id_turma_disciplina=modulo)

    registros = AlunoModulo.objects.filter(id_turma_disciplina=modulo).select_related('id_aluno__usuario')

    if request.method == 'POST':
        alteracoes = 0
        for reg in registros:
            s1 = request.POST.get(f'nota1_{reg.id_aluno_id}', '').strip()
            s2 = request.POST.get(f'nota2_{reg.id_aluno_id}', '').strip()

            def parse_nota(s):
                if s == '':
                    return None
                try:
                    v = float(s)
                    if v < 0 or v > 10:
                        raise ValueError('Fora da faixa 0-10')
                    return v
                except Exception:
                    return None

            n1 = parse_nota(s1)
            n2 = parse_nota(s2)

            mudou = False
            if (n1 is None) != (reg.nota_prova1 is None) or (n1 is not None and float(reg.nota_prova1 or 0) != n1):
                reg.nota_prova1 = n1
                mudou = True
            if (n2 is None) != (reg.nota_prova2 is None) or (n2 is not None and float(reg.nota_prova2 or 0) != n2):
                reg.nota_prova2 = n2
                mudou = True

            # Se ambas as notas presentes, calcular via C
            if n1 is not None and n2 is not None:
                try:
                    from c.notas_avaliacao_wrapper import calcular_media_status
                    res = calcular_media_status(n1, n2, 7.0)
                    reg.media_final = res['media']
                    reg.status = res['status']
                except Exception:
                    # Fallback Python
                    media = (n1 + n2) / 2.0
                    reg.media_final = media
                    reg.status = 'aprovado' if media >= 7.0 else 'reprovado'
                mudou = True
            else:
                reg.media_final = None
                reg.status = 'pendente'
                mudou = True

            if mudou:
                reg.save()
                alteracoes += 1

        messages.success(request, f'Notas atualizadas. Registros alterados: {alteracoes}.')
        return redirect('professor_lancar_notas', modulo_id=modulo.id)

    # Anexa classificação de risco para feedback rápido ao professor
    for reg in registros:
        media = reg.media_final
        p1 = reg.nota_prova1
        p2 = reg.nota_prova2
        if media is None:
            if p1 is not None and p1 < 5 and p2 is None:
                reg.risco = 'moderado'
            else:
                reg.risco = 'pendente'
        else:
            if media < 5:
                reg.risco = 'alto'
            elif media < 7:
                reg.risco = 'moderado'
            else:
                reg.risco = 'ok'

    return render(request, 'sistema/professor_lancar_notas.html', {
        'modulo': modulo,
        'registros': registros,
    })


# ==================== VIEWS PARA COORDENADORES ====================

@login_required
def coordenador_criar_turma(request):
    """Coordenador cria uma nova turma"""
    if not hasattr(request.user, 'coordenador'):
        messages.error(request, 'Apenas coordenadores podem cadastrar turmas.')
        return redirect('lista_turmas')
    
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            turma = form.save()
            messages.success(request, f'Turma "{turma.nome}" cadastrada com sucesso!')
            return redirect('lista_turmas')
    else:
        form = TurmaForm()
    
    return render(request, 'sistema/coordenador_criar_turma.html', {'form': form})

