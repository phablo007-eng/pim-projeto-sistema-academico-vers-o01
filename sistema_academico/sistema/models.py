from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

"""Modelos do sistema acadêmico.

Estrutura baseada no diagrama fornecido. Agora usando o User nativo do Django
para autenticação. Cada perfil especializado (Coordenador, Professor, Aluno) 
referencia User via OneToOneField compartilhando a mesma chave primária.
"""

# Alias para compatibilidade com código existente
Usuario = User

class Coordenador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    cpf = models.CharField(
        max_length=14, 
        unique=True, 
        null=True,
        blank=True,
        validators=[RegexValidator(regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', message='CPF deve estar no formato XXX.XXX.XXX-XX')]
    )
    data_de_contratacao = models.DateField()

    def __str__(self):
        return f"Coordenador: {self.usuario.get_full_name() or self.usuario.username}"

class Professor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    matricula = models.CharField(max_length=20, unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    cpf = models.CharField(
        max_length=14, 
        unique=True, 
        null=True,
        blank=True,
        validators=[RegexValidator(regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', message='CPF deve estar no formato XXX.XXX.XXX-XX')]
    )
    data_de_contratacao = models.DateField()
    titulacao = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Prof. {self.usuario.get_full_name() or self.usuario.username} ({self.matricula})"

class Aluno(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True, related_name='perfil_aluno')
    matricula = models.CharField(max_length=20, unique=True)
    data_de_nascimento = models.DateField()
    cpf = models.CharField(
        max_length=14, 
        unique=True, 
        null=True,
        blank=True,
        validators=[RegexValidator(regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', message='CPF deve estar no formato XXX.XXX.XXX-XX')]
    )

    def __str__(self):
        return f"Aluno: {self.usuario.get_full_name() or self.usuario.username} ({self.matricula})"
    
  
# 3. Disciplina e Relacionamento Professor-Disciplina

class Disciplina(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    carga_horaria = models.PositiveIntegerField()  # Em horas, garante não-negativo

    def __str__(self):
        return self.nome

class ProfessorDisciplina(models.Model):
    # Tabela M:N (Muitos para Muitos) explícita entre Professor e Disciplina
    id_professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='disciplinas_ministradas')
    id_disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='professores')
    
    class Meta:
        # Garante que um professor só pode ser associado uma vez a uma disciplina
        unique_together = ('id_professor', 'id_disciplina')
        verbose_name = 'Associação Professor-Disciplina'
        verbose_name_plural = 'Associações Professor-Disciplina'

    def __str__(self):
        return f"{self.id_professor.usuario.get_full_name() or self.id_professor.usuario.username} - {self.id_disciplina.nome}"
    
# 4. Turma

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    semestre = models.CharField(
        max_length=6, 
        validators=[RegexValidator(regex=r'^[0-9]{4}\.[12]$', message='Semestre deve estar no formato YYYY.1 ou YYYY.2')]
    )  # Ex: 2024.1
    curso = models.CharField(max_length=100)

    # Relacionamentos
    id_coordenador = models.ForeignKey(Coordenador, on_delete=models.SET_NULL, null=True, blank=True, related_name='turmas')

    # Relacionamento M:N com Aluno
    alunos = models.ManyToManyField(Aluno, related_name='turmas')

    def __str__(self):
        return f"{self.nome} ({self.curso} - {self.semestre})"
        


# 5. Turma Disciplina (Tabela que liga Turma, Disciplina e Professor)

class TurmaDisciplina(models.Model):
    # Liga Turma, Disciplina e o Professor que ministra AQUELE módulo
    id_turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='modulos')
    id_disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='turmas_associadas')
    id_professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='modulos_ministrados')
    
    # Informações específicas da Turma/Disciplina
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)

    class Meta:
        # Garante que uma Turma só pode ter a mesma Disciplina associada uma vez
        unique_together = ('id_turma', 'id_disciplina')
        verbose_name = 'Módulo de Turma/Disciplina'
        verbose_name_plural = 'Módulos de Turmas/Disciplinas'

    def __str__(self):
        return f"{self.id_turma.nome} - {self.id_disciplina.nome}"

# 6. Atividade e Entrega

class AlunoModulo(models.Model):
    """
    Matrícula do aluno no módulo (TurmaDisciplina) com notas consolidadas de provas.
    """
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('reprovado', 'Reprovado'),
    )

    id_aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='modulos')
    id_turma_disciplina = models.ForeignKey(TurmaDisciplina, on_delete=models.CASCADE, related_name='alunos_modulo')

    nota_prova1 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    nota_prova2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    media_final = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pendente')

    class Meta:
        unique_together = ('id_aluno', 'id_turma_disciplina')
        verbose_name = 'Aluno no Módulo'
        verbose_name_plural = 'Alunos no Módulo'

    def __str__(self):
        return f"{self.id_aluno} em {self.id_turma_disciplina}"

class Atividade(models.Model):
    data = models.DateField()
    descricao = models.TextField()
    id_turma_disciplina = models.ForeignKey(TurmaDisciplina, on_delete=models.CASCADE, related_name='atividades')

    def __str__(self):
        return f"Atividade em {self.id_turma_disciplina} - {self.data}"

class AlunoAtividade(models.Model):
    # Representa a ENTREGA de uma atividade por um aluno
    id_aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='atividades_entregues')
    id_atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE, related_name='entregas')
    # Campos de entrega
    arquivo = models.FileField(upload_to='entregas/%Y/%m/', null=True, blank=True)
    resposta_texto = models.TextField(null=True, blank=True)
    nota = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    data_entrega = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Garante que um aluno só pode entregar uma vez a mesma atividade
        unique_together = ('id_aluno', 'id_atividade')
        verbose_name = 'Entrega de Atividade'
        verbose_name_plural = 'Entregas de Atividades'

    def __str__(self):
        return f"Entrega de {self.id_atividade} por {self.id_aluno.usuario.get_full_name() or self.id_aluno.usuario.username}"

# 7. Aula

class Aula(models.Model):
    id_turma_disciplina = models.ForeignKey(TurmaDisciplina, on_delete=models.CASCADE, related_name='aulas')
    data = models.DateField()
    conteudo = models.TextField()

    def __str__(self):
        return f"Aula de {self.id_turma_disciplina} em {self.data}"
