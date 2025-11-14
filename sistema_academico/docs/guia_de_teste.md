# Evidência de IA

O sistema implementa uma lógica de apoio inteligente baseada em regras, que classifica o risco de reprovação do aluno e recomenda ações de estudo. Essa evidência de IA está presente nas telas de notas do aluno e lançamento de notas do professor, por meio de badges visuais e recomendações textuais. A classificação considera a média, notas P1/P2 e pendências, fornecendo ao aluno e ao professor uma indicação clara do risco e sugestões para melhoria, conforme exigido pelo edital.
# Sistema Acadêmico — Guia de Teste Rápido (Windows)

Este README é focado em quem vai testar o projeto: pré-requisitos, instalação, configuração, como compilar as DLLs em C (opcional), rotas principais e cenários para validar rapidamente as funcionalidades de aluno e professor.

—
## Visão Rápida
- Framework: Django 5.2.x (auth nativa `User`).
- Banco: SQLite (arquivo `db.sqlite3`).
- Perfis: `Aluno`, `Professor`, `Coordenador` (1:1 com `User`).
- Funcionalidades-chave: atividades e entregas, lançamento de notas P1/P2, visualização de notas do aluno, API de estatísticas de notas.
- Integração C: DLLs para estatísticas e cálculo de média/status (fallback em Python se DLLs não estiverem disponíveis).

—

## Pré‑requisitos
- Python 3.11+ instalado (verifique com `python --version`).
- Pip em funcionamento (`python -m pip --version`).
- Windows PowerShell (comandos abaixo usam PowerShell).
- Opcional (para compilar as DLLs em C):
  - Microsoft Visual Studio 2022 Build Tools (com “Desktop development with C++”).
  - Acesso ao atalho “x64 Native Tools Command Prompt for VS”.

—
## Clonar e Entrar na Pasta do Projeto
Se ainda não tiver o código local, clone seu repositório. Em seguida, entre no diretório do projeto (onde está `manage.py`).

Exemplo (ajuste a URL/paths conforme seu ambiente):
```powershell
git clone <URL-do-seu-repo>.git sistema_academico
cd sistema_academico
```

—
## Criar e Ativar Virtualenv
```powershell
python -m venv .venv
& ".\.venv\Scripts\Activate.ps1"
```

—
## Instalar Dependências
```powershell
pip install -r requirements.txt
```

—
## Configurar Variáveis de Ambiente (.env)
Crie um arquivo `.env` na raiz (mesma pasta de `manage.py`) com o mínimo abaixo:
```
SECRET_KEY=dev-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
# DATABASE_URL opcional; por padrão usa SQLite local em db.sqlite3
# DATABASE_URL=sqlite:///db.sqlite3
```

—
## Preparar o Banco de Dados
- Se estiver começando do zero:
```powershell
python manage.py migrate
```

- Criar um superusuário para acessar o admin:
```powershell
python manage.py createsuperuser
```

- Opcional: se houver usuários legados do modelo antigo, rode a migração utilitária ANTES de certas migrações (veja `migrar_usuarios.py`).
```powershell
python migrar_usuarios.py
```

—
## Compilar as DLLs em C (Opcional, com MSVC)
O sistema funciona mesmo sem DLLs (cálculos caem em fallback Python). Para usar C nativo:

1) Abra o “x64 Native Tools Command Prompt for VS”.
2) Vá até a pasta `c/` do projeto.
```bat
cd "C:\Users\Phablo ennzo\OneDrive\Documentos\My Games\OneDrive\Documentos\pasta definitiva\sistema_academico\c"

rem Estatísticas (média/min/máx)
build_msvc.bat

rem P1/P2 → média e status
build_msvc_avaliacao.bat
```
As DLLs `notas_basico.dll` e `notas_avaliacao.dll` serão geradas na pasta `c/`. Os wrappers Python já procuram por elas nesse diretório.

—
## Executar o Servidor
```powershell
python manage.py runserver
```
Acesse: `http://127.0.0.1:8000/`
ou depois entre do navegador e pesquise
http://localhost:8000(joga direta pra tela de login) o ideal
—
## Rotas Importantes (para teste)
- Login: `http://127.0.0.1:8000/login/`
- Admin Django: `http://127.0.0.1:8000/admin/`
- Home (dashboard simples): `/`
- Listas: `/alunos/`, `/professores/`, `/coordenadores/`, `/turmas/`, `/disciplinas/`
- Professor:
  - Meus módulos: `/professor/turmas/`
  - Criar atividade: `/professor/modulo/<id>/criar-atividade/`
  - Ver atividades do módulo: `/professor/modulo/<id>/atividades/`
  - Corrigir entrega: `/professor/entrega/<id>/corrigir/`
  - Lançar notas P1/P2: `/professor/modulo/<id>/lancar-notas/`
- Aluno:
  - Minhas atividades: `/aluno/atividades/`
  - Entregar atividade: `/aluno/atividade/<id>/entregar/`
  - Minhas notas (P1/P2, média e status): `/aluno/notas/`

—
## Cenário Mínimo para Validar o Fluxo
1) No admin (`/admin/`), crie:
   - Um `User` do tipo professor e um do tipo aluno (pode ser você mesmo para testar; marque `is_staff` para acessar o admin).
   - Perfis vinculados: crie `Professor` e `Aluno` ligando cada um ao seu `User` correspondente.
   - Uma `Disciplina` (ex.: “Algoritmos”).
  - Uma `Turma` (ex.: “TADS 2025.2”). Adicione o aluno em “alunos da turma”.
  - Crie um perfil de `Coordenador` e vincule ao usuário correspondente. O coordenador pode gerenciar turmas, professores e disciplinas, organizando a estrutura acadêmica antes do lançamento de atividades e notas.
  - Um `TurmaDisciplina` (módulo), ligando a Turma + Disciplina + Professor.
2) Faça login como coordenador para visualizar e organizar turmas, professores e disciplinas. Em seguida, faça login como professor e acesse “Módulos do Professor”.
3) Crie uma atividade no módulo e, opcionalmente, faça upload/entrega como aluno em “Minhas Atividades”.
4) Como professor, acesse “Lançar Notas” do módulo, preencha P1 e P2; salve. A média/status são calculados (via DLL ou fallback Python).
5) Como aluno, acesse “Minhas Notas” para ver P1/P2, média e status (aprovado se média ≥ 7).

—
## API de Estatísticas (Teste Rápido)
Endpoint: `POST /api/estatisticas/`

Exemplo (PowerShell):
```powershell
$body = @{ notas = @(7.5, 8.0, 5.0, 10.0) } | ConvertTo-Json
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/api/estatisticas/ `
  -ContentType 'application/json' `
  -Body $body
```
Resposta esperada:
```json
{ "media": 7.625, "minimo": 5.0, "maximo": 10.0, "quantidade": 4 }
```

—
## Onde Ficam os Arquivos
- Código Django do app: `sistema/`
- Configuração do projeto: `sistema_academico/`
- Templates HTML: `sistema/templates/sistema/`
- Uploads (desenvolvimento): `media/` (servida automaticamente em `DEBUG=True`).
- Módulos C e wrappers: `c/`
- Dependências: `requirements.txt`

—
## Dúvidas Comuns (FAQ)
- “Preciso compilar as DLLs para testar?”
  - Não. Sem DLLs, o sistema usa cálculo em Python (fallback). Compilar é opcional.
- “Como crio os perfis de aluno/professor?”
  - No admin, crie o `User` e depois crie o perfil `Aluno`/`Professor` usando o mesmo usuário.
- “Onde vejo as notas lançadas?”
  - Menu “Minhas Notas” do aluno (`/aluno/notas/`).
- “Erro de permissão ao lançar notas?”
  - Verifique se o `Professor` do seu usuário está vinculado ao `TurmaDisciplina` do módulo.

—
## Diagramas (Opcional)
Arquivos em `sistema_academico/diagrams/` (formato Mermaid e texto). Para visualizar Mermaid no VS Code, instale a extensão “Markdown Preview Mermaid Support” ou use um visualizador online (ex.: mermaid.live).

—
## Troubleshooting Rápido
- “DLL não encontrada” ao lançar notas:
  - Compile `c/notas_avaliacao.dll` ou ignore (o fallback Python cobre). Mensagens de erro detalham o caminho esperado.
- Uploads não aparecem:
  - Confirme `DEBUG=True` no `.env` e use `http://127.0.0.1:8000/`. Arquivos são servidos via `static()` no `urls.py` em modo debug.
- `DisallowedHost` em produção/local diferente:
  - Ajuste `ALLOWED_HOSTS` no `.env`.

—
## Versões
- Python: 3.11+
- Django: 5.2.7
- django‑environ: 0.12.0

—
## Licença e Uso
Projeto acadêmico para fins educacionais. Ajuste credenciais e dados antes de uso público.