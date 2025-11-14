# Sistema Acadêmico — Decisões Técnicas e de Design

Este documento apresenta as principais decisões de arquitetura, modelagem, implementação e operação adotadas no projeto, incluindo alternativas consideradas, justificativas e impactos.

---
## Sumário
1. Escopo e Stack
2. Autenticação e Perfis
3. Modelagem Relacional
4. Tabelas de Associação Explícitas
5. Validações e Integridade
6. Estratégia de Consultas (Performance)
7. Integração com Código C (ctypes)
8. Fallback Python vs DLL
9. Organização de Pastas
10. Configuração via `.env`
11. Tratamento de Entregas e Notas
12. Lançamento de P1/P2 (Modelo `AlunoModulo`)
13. Padronização de Templates / UI
14. Segurança e Permissões (Estado Atual)
15. Migração de Usuários Legados
16. Critérios para Evolução Futura
17. Trade-offs Resumidos
18. Checklist de Qualidade

---
## 1. Escopo e Stack
**Decisão:** Usar Django 5.x com SQLite para fase inicial.
**Justificativa:** Velocidade de desenvolvimento; admin pronto; zero config adicional para banco. Permite evolução posterior para PostgreSQL sem alterar lógica de negócio.
**Alternativas:** Flask (maior esforço para admin e auth), FastAPI (mais forte em APIs, menos em CRUD pronto).
**Impacto:** Time reduzido para MVP; menor complexidade de infraestrutura.

---
## 2. Autenticação e Perfis
**Decisão:** Usar o `User` nativo + perfis (`Aluno`, `Professor`, `Coordenador`) via `OneToOneField`.
**Justificativa:** Aproveitar hashing de senha, permissões, grupos futuros, interface admin já integrada.
**Alternativa:** Criar `CustomUser` com campos extras (custos de migração e testes de segurança maiores).
**Impacto:** Menos código sensível; migração de perfis simples; flexibilidade para evoluir com grupos.

---
## 3. Modelagem Relacional
**Decisão:** Separar entidades centrais (Turma, Disciplina, Atividade, Aula) e criar ligações contextuais.
**Justificativa:** Evita sobrecarga em uma única tabela; clarifica contexto (ex.: Atividade sempre ligada ao par Turma+Disciplina+Professor).
**Impacto:** Queries mais fáceis de otimizar; relacionamento explícito de responsabilidades.

---
## 4. Tabelas de Associação Explícitas
**Decisão:** `ProfessorDisciplina` e `TurmaDisciplina` ao invés de `ManyToMany` implícito.
**Justificativa:** Possibilidade de adicionar metadados (datas, carga adaptada, status futuro) + unicidade controlada.
**Alternativa:** Campo `ManyToManyField` direto com through automático.
**Impacto:** Maior verbosidade inicial; maior flexibilidade evolutiva.

---
## 5. Validações e Integridade
**Decisão:** Regex para CPF (`XXX.XXX.XXX-XX`) e semestre (`YYYY.[1|2]`), unicidade em chaves compostas.
**Justificativa:** Consistência de formato e garantia de ausência de duplicatas.
**Alternativa:** Validar no formulário (menos robusto), triggers de banco (maior esforço).
**Impacto:** Redução de erros de entrada; manutenção simples.

---
## 6. Estratégia de Consultas (Performance)
**Decisão:** Uso consistente de `select_related` em FKs e `prefetch_related` em coleções.
**Justificativa:** Evitar N+1 queries em listagens; ganho de performance em páginas de listagem.
**Alternativa:** Carregamento preguiçoso padrão (mais simples, porém ineficiente em escala).
**Impacto:** Melhor latência já na fase inicial sem caching.

---
## 7. Integração com Código C (ctypes)
**Decisão:** Dois módulos C simples (`notas_basico`, `notas_avaliacao`) carregados via `ctypes`.
**Justificativa:** Demonstração de extensão nativa, separação de responsabilidade (cálculos pontuais), possível ganho de performance com listas grandes.
**Alternativa:** Implementar tudo em Python puro (mais simples, menos demonstração técnica); usar Cython (build mais complexo).
**Impacto:** Requer toolchain MSVC para compilação em Windows; promove aprendizado de integração.

---
## 8. Fallback Python vs DLL
**Decisão:** Se DLL não estiver disponível, executar lógica equivalente em Python.
**Justificativa:** Reduz fricção para testadores sem ambiente C; evita quebra da aplicação.
**Alternativa:** Tornar DLL obrigatória (maior risco operacional para testers).
**Impacto:** Robustez; pequeno custo de manutenção dupla (código C + Python).

---
## 9. Organização de Pastas
```
raiz/
  sistema_academico/ (config projeto)
  sistema/           (app de domínio)
  c/                 (código nativo + wrappers)
  media/             (uploads)
  static/            (recursos estáticos locais)
  diagrams/          (diagramas Mermaid e texto)
```
**Decisão:** Separação clara de responsabilidades.
**Impacto:** Localização rápida de componentes para novos contribuidores.

---
## 10. Configuração via `.env`
**Decisão:** Uso de `django-environ`.
**Justificativa:** Facilita troca de banco, chaves secretas e flags sem editar código.
**Alternativa:** Variáveis hardcoded em `settings.py` (inseguro e inflexível).
**Impacto:** Padroniza práticas Dev/Prod.

---
## 11. Tratamento de Entregas e Notas
**Decisão:** Modelo `AlunoAtividade` guarda entrega e nota de cada atividade; notas de provas ficam em `AlunoModulo`.
**Justificativa:** Diferenciar nota de atividade (granular) das notas de avaliação formal P1/P2.
**Alternativa:** Colocar tudo em um único modelo (mistura conceitos, dificulta regras diferentes).
**Impacto:** Semântica clara; escalável para adicionar recuperação ou P3.

---
## 12. Lançamento de P1/P2 (`AlunoModulo`)
**Decisão:** Criar registros `AlunoModulo` automaticamente ao acessar tela de lançamento (garantia de existência).
**Justificativa:** Evitar exceções por ausência e diminuir fluxo manual de criação.
**Alternativa:** Criar via seed ou ação administrativa prévia.
**Impacto:** Menos passos para professor; complexidade mínima.

---
## 13. Padronização de Templates / UI
**Decisão:** Bootstrap 5 CDN + ícones `bootstrap-icons`.
**Justificativa:** Reduz setup de front-end; responsividade imediata.
**Alternativa:** Tailwind (config adicional), UI custom (maior esforço).
**Impacto:** Acelera desenvolvimento; estética consistente.

---
## 14. Segurança e Permissões (Estado Atual)
**Decisão:** Proteger páginas com `@login_required`; confiando em perfis para contexto.
**Justificativa:** MVP sem granularidade de permissões complexas.
**Alternativa:** Uso imediato de grupos/permissions fine-grained.
**Impacto:** Simplicidade inicial; requer evolução se acesso diferenciado for exigido.

---
## 15. Migração de Usuários Legados
**Decisão:** Script `migrar_usuarios.py` recria `auth_user` preservando IDs.
**Justificativa:** Evitar que FKs para perfis que apontam para antigos IDs quebrem.
**Alternativa:** Recriar perfis manualmente (propenso a erro), alterar FKs.
**Impacto:** Transição suave; segurança de integridade relacional.

---
## 16. Critérios para Evolução Futura
| Área | Próxima Ação | Benefício |
|------|--------------|-----------|
| Testes | Adicionar testes de autenticação e modelos | Confiabilidade em refactors |
| Permissões | Grupos por perfil | Segurança e isolamento |
| UX | Paginação e busca | Usabilidade em escala |
| Relatórios | Dashboard de notas/entregas | Valor analítico |
| Logs | Logging estruturado e auditoria | Rastreamento e conformidade |
| Deploy | Migrar para Postgres + container | Escalabilidade |

---
## 17. Trade-offs Resumidos
| Decisão | Benefício | Custo | Mitigação |
|---------|-----------|-------|-----------|
| User nativo | Menos código auth | Limitação de campos diretos | Perfis 1:1 |
| Tabelas associação | Flexibilidade | Verbosidade | Documentação clara |
| Regex validação | Consistência | Falta de validação semântica profunda | Possível validação adicional depois |
| DLL opcional | Robustez / fallback | Manutenção extra | Código C simples |
| Geração automática `AlunoModulo` | Facilidade professor | Execução em view | Checagem idempotente |
| SQLite inicialmente | Simplicidade | Escalabilidade limitada | Migração futura para Postgres |

---
## 18. Checklist de Qualidade (Atual vs Futuro)
- [x] Autenticação básica funcional
- [x] Modelos centrais normalizados
- [x] Uso de `select_related`/`prefetch_related`
- [x] Fallback para ausência de DLL
- [ ] Testes automatizados
- [ ] Permissões avançadas
- [ ] Logs estruturados
- [ ] Paginação e busca global
- [ ] Métricas / dashboard

---
### Conclusão
As decisões privilegiam clareza, evolução gradual e robustez mínima para testes. Padrões adotados facilitam expansão sem reestruturações drásticas.

Para sugestões ou dúvidas: ver README principal ou abrir issue de mudança específica.
