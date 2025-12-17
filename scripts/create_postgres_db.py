from pathlib import Path
import environ
import psycopg2

project_root = Path(__file__).resolve().parent.parent / "sistema_academico"
environ.Env.read_env(project_root / ".env")

env = environ.Env()
dbname = env('DATABASE_NAME')
user = env('DATABASE_USER')
password = env('DATABASE_PASSWORD')
host = env('DATABASE_HOST', default='localhost')
port = env('DATABASE_PORT', default='5432')

print('Connecting to PostgreSQL to create database:', dbname)
conn = psycopg2.connect(dbname='postgres', user=user, password=password, host=host, port=port)
conn.autocommit = True
try:
    with conn.cursor() as cur:
        cur.execute(f"CREATE DATABASE {dbname}")
        print('Database created successfully.')
except psycopg2.errors.DuplicateDatabase:
    print('Database already exists; skipping creation.')
finally:
    conn.close()
