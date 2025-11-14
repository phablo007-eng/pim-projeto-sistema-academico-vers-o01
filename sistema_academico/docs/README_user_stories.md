# Sistema Acadêmico — User Stories, Rastreabilidade

Este documento organiza as histórias de usuário por épico, adiciona IDs e conecta cada requisito a partes concretas da implementação (modelos, views, templates, rotas e, quando aplicável, módulos C). A rastreabilidade facilita validação, testes e evolução.

---
## Convenção de IDs
- Épicos: `EPxx` (ex.: `EP01`)
- Histórias: `USxx` dentro do épico (ex.: `EP01-US01`)
- Requisitos técnicos específicos (opcional): `RQxx`

Cada história segue o formato:
"Como [perfil], quero [objetivo] para [benefício]."

---
## Visão Geral dos Épicos
| Épico | Nome | Objetivo Principal |
|-------|------|-------------------|
| EP01 | Autenticação e Perfis | Acesso seguro e identificação de papéis |
| EP02 | Estrutura Acadêmica | Organização de turmas, disciplinas e módulos |
| EP03 | Atividades e Entregas | Criação, submissão e correção de atividades |
| EP04 | Avaliações (Provas) | Lançamento e cálculo de notas P1/P2 |
| EP05 | Consulta do Aluno | Visualização de atividades e notas |
| EP06 | Estatísticas e Métrica | Cálculo de estatísticas via API/C |
| EP07 | Administração e Migração | Gestão de dados e migração de usuários antigos |
| EP08 | Qualidade / Futuro | Testes, logs, desempenho (planejado) |

---
## EP01 — Autenticação e Perfis
| ID | História | Implementação | Evidência |
|----|----------|---------------|-----------|
| EP01-US01 | Como usuário quero fazer login para acessar áreas restritas | View `login_view`, template `login.html`, rota `/login/` | `sistema/views.py` |
| EP01-US02 | Como usuário quero sair da sessão para proteger minha conta | View `logout_view`, rota `/logout/` | `sistema/views.py` |
| EP01-US03 | Como admin quero criar perfis vinculados ao User | Inlines no `UserAdmin` | `sistema/admin.py` |
| EP01-US04 | Como professor/aluno quero ver meu nome na navbar | Template `base.html` | `templates/sistema/base.html` |

---
## EP02 — Estrutura Acadêmica
| ID | História | Implementação | Evidência |
|----|----------|---------------|-----------|
| EP02-US01 | Como coordenador quero cadastrar turmas | Model `Turma`, admin, rota `/turmas/` | `models.py`, `views.lista_turmas` |
| EP02-US02 | Como usuário quero listar disciplinas | Model `Disciplina`, rota `/disciplinas/` | `views.lista_disciplinas` |
| EP02-US03 | Como professor quero ver meus módulos (turma+disciplina) | Model `TurmaDisciplina`, view `professor_minhas_turmas` | `views.professor_minhas_turmas` |
| EP02-US04 | Como usuário quero ver detalhes de uma turma | View `detalhe_turma`, rota `/turmas/<id>/` | `views.detalhe_turma` |

---
## EP03 — Atividades e Entregas
| ID | História | Implementação | Evidência |
|----|----------|---------------|-----------|
| EP03-US01 | Como professor quero criar atividades para o módulo | View `professor_criar_atividade` | `views.professor_criar_atividade` |
| EP03-US02 | Como professor quero listar atividades e entregas | View `professor_ver_atividades` | `views.professor_ver_atividades` |
| EP03-US03 | Como aluno quero ver minhas atividades pendentes | View `aluno_minhas_atividades` | `views.aluno_minhas_atividades` |
| EP03-US04 | Como aluno quero entregar uma atividade | View `aluno_entregar_atividade` + upload em `media/` | `views.aluno_entregar_atividade` |
| EP03-US05 | Como professor quero corrigir entrega atribuindo nota | View `professor_corrigir_entrega` | `views.professor_corrigir_entrega` |

---
## EP04 — Avaliações (Provas P1/P2)
| ID | História | Implementação | Evidência |
|----|----------|---------------|-----------|
| EP04-US01 | Como professor quero lançar notas P1/P2 por aluno do módulo | View `professor_lancar_notas`, template `professor_lancar_notas.html` | `views.professor_lancar_notas` |
| EP04-US02 | Como sistema quero calcular média e status (aprovado/reprovado) | DLL `notas_avaliacao.dll` + wrapper + fallback Python | `c/notas_avaliacao_*`, view |
| EP04-US03 | Como professor quero ver confirmação de atualização | Mensagem via `messages.success` | `views.professor_lancar_notas` |

---
## EP05 — Consulta do Aluno
| ID | História | Implementação | Evidência |
|----|----------|---------------|-----------|
| EP05-US01 | Como aluno quero ver minhas notas P1/P2 | View `aluno_minhas_notas` | `views.aluno_minhas_notas` |
| EP05-US02 | Como aluno quero entender meu status de aprovação | Campo `status` em `AlunoModulo` | `models.AlunoModulo` |
| EP05-US03 | Como aluno quero ver média calculada | Campo `media_final` e cálculo via C/Python | `AlunoModulo` + wrapper C |

---
## EP06 — Estatísticas e Métrica
| ID | História | Implementação | Evidência |
|----|----------|---------------|-----------|
| EP06-US01 | Como usuário quero enviar lista de notas e obter estatísticas | API `POST /api/estatisticas/` | `views.api_estatisticas_notas` |
| EP06-US02 | Como sistema quero calcular média/min/máx eficientemente | DLL `notas_basico.dll` + wrapper | `c/notas_basico_*` |
| EP06-US03 | Como testador quero continuar mesmo sem DLL | Fallback (mensagem erro DLL ausente) | `notas_basico_wrapper.py` |

---
## EP07 — Administração e Migração
| ID | História | Implementação | Evidência |
|----|----------|---------------|-----------|
| EP07-US01 | Como admin quero cadastrar tudo rapidamente via interface | Admin configurado com inlines | `admin.py` |
| EP07-US02 | Como mantenedor quero migrar usuários antigos preservando IDs | Script `migrar_usuarios.py` | Arquivo script |
| EP07-US03 | Como admin quero alterar senhas inicializadas | Senha padrão + prompt de troca | `migrar_usuarios.py` saída |

---
## EP08 — Qualidade / Futuro (Planejado)
| ID | História | Status | Observação |
|----|----------|--------|------------|
| EP08-US01 | Como desenvolvedor quero ter testes automatizados | Pendência | Criar casos em `tests.py` |
| EP08-US02 | Como admin quero paginação em listas grandes | Pendência | Introduzir `Paginator` |
| EP08-US03 | Como gestor quero dashboards de desempenho | Pendência | Agregar dados de notas |
| EP08-US04 | Como auditor quero logs detalhados de ações críticas | Pendência | Logging estruturado |

---
## Matriz de Rastreabilidade (Resumo)
| História | Modelos | Views | Templates | Rotas | Cód. C (se houver) |
|----------|---------|-------|----------|-------|---------------------|
| EP03-US04 | Aluno, Atividade, AlunoAtividade | `aluno_entregar_atividade` | `aluno_entregar.html` | `/aluno/atividade/<id>/entregar/` | - |
| EP04-US01 | AlunoModulo, TurmaDisciplina, Aluno | `professor_lancar_notas` | `professor_lancar_notas.html` | `/professor/modulo/<id>/lancar-notas/` | `notas_avaliacao.c` |
| EP05-US01 | AlunoModulo | `aluno_minhas_notas` | `aluno_notas.html` | `/aluno/notas/` | `notas_avaliacao.c` (cálculo) |
| EP06-US01 | - | `api_estatisticas_notas` | - | `/api/estatisticas/` | `notas_basico.c` |
| EP07-US02 | User | - | - | - | - (script Python) |

---
## Cobertura Atual vs Planejada
| Tipo | Coberto | Observações |
|------|---------|-------------|
| Autenticação | Sim | Login/logout + proteção `@login_required` |
| Perfis | Sim | Perfis 1:1 (Aluno, Professor, Coordenador) |
| CRUD Acadêmico | Parcial | Foco em criação básica via admin |
| Atividades | Sim | Criação, listagem, entrega, correção |
| Provas P1/P2 | Sim | Lançamento + cálculo média/status |
| Estatísticas | Sim | API + C + fallback |
| Testes automatizados | Não | Planejado (EP08) |
| Paginação | Não | Planejado |
| Dashboards | Não | Planejado |
| Logs estruturados | Não | Planejado |

---
## Prioridades Recomendadas (Incremento)
1. Implementar testes mínimos (login, criação de atividade, cálculo de média).
2. Paginação em listagens maiores (alunos, atividades).
3. Logging de fallback (quando DLL ausente) para auditoria.
4. Dashboard inicial (total aprovados/reprovados por turma).
5. Permissões avançadas (se diferentes papéis exigirem escopo restrito).

---
## Exemplo de Caso de Teste Derivado (EP04-US01)
| Caso | Passos | Resultado Esperado |
|------|--------|--------------------|
| Lançar notas válidas | Acessar rota, preencher P1=8, P2=6, salvar | Média=7, status=aprovado (DLL ou Python) |
| Nota fora da faixa | P1=11, salvar | Ignora valor inválido (campo volta vazio) |
| Uma nota faltando | P1=7, P2= (vazio) | Status pendente, média não calculada |

---
## Riscos Identificados
| Risco | Mitigação |
|-------|-----------|
| Falta de testes → regressões silenciosas | Introduzir suíte mínima EP08-US01 |
| Escala de leitura em listas grandes | Paginação + índices |
| Dependência da DLL em ambientes sem compilador | Manter fallback Python e logar ausência |
| Ausência de controle granular de permissões | Implementar grupos (Aluno/Professor/Coordenador) |

---
## Observações Finais
Este documento deve ser atualizado quando novas histórias forem adicionadas ou concluídas (especialmente as marcadas como pendentes no EP08). A matriz de rastreabilidade pode ser expandida com colunas de teste (ID de caso) à medida que os testes forem criados.

Para dúvidas ou adições, abra uma solicitação registrando o ID da história (ex.: EP05-US03) e a proposta de alteração.
