# Continuação da Transição para PostgreSQL

Este documento reúne os próximos passos para garantir que o projeto rode com PostgreSQL em vez de SQLite.

## Pré-requisitos
- Instale e rode um servidor PostgreSQL local (ou a instância remota de sua preferência).
- Defina as credenciais corretas no arquivo `.env` dentro de `sistema_academico/`.
  - Os nomes esperados já existem, por exemplo: `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_HOST`, `DATABASE_PORT` e `DATABASE_ENGINE=postgresql`.
- Garanta que as dependências estejam instaladas com `pip install -r sistema_academico/requirements.txt`.

## Passo a passo
1. Atualize ou confirme os valores do `.env` com as credenciais válidas do servidor PostgreSQL.
2. Execute `python scripts/create_postgres_db.py` para garantir que o banco de dados exista. O script lê o `.env` do diretório `sistema_academico/` e ignora erros caso o banco já exista.
3. Aplique as migrações do Django:
   ```
   python sistema_academico/manage.py migrate
   ```
4. Se quiser recuperar os dados já exportados de SQLite, carregue o fixture fornecido:
   ```
   python sistema_academico/manage.py loaddata dumpdata.json
   ```
   O arquivo `sistema_academico/dumpdata.json` contém os registros atuais.
5. Rode os testes ou execute o servidor normalmente com `python sistema_academico/manage.py runserver` para verificar.

## Alternativas e reversão
- Para voltar temporariamente ao SQLite, basta definir `DATABASE_ENGINE=sqlite3` no `.env`. O Django irá usar `db.sqlite3` como antes.
- Se precisar recriar o banco PostgreSQL com um nome diferente, ajuste `DATABASE_NAME` no `.env` e execute novamente o script de criação.

## Observações
- Como a `psycopg2` é necessária para a conexão, ela já foi adicionada às dependências (ver `sistema_academico/requirements.txt`).
- O script `scripts/create_postgres_db.py` já lida com `DuplicateDatabase`, então você pode rodá-lo quantas vezes precisar.
