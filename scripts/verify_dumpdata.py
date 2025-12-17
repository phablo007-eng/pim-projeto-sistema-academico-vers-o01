import json
import os
import sys
from collections import Counter
from pathlib import Path

import django


BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR / 'sistema_academico'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_academico.settings')
sys.path.insert(0, str(PROJECT_DIR))
os.environ['DATABASE_ENGINE'] = 'sqlite3'
django.setup()

from django.apps import apps


def load_dump_counts():
    dump_path = PROJECT_DIR / 'dumpdata.json'
    if not dump_path.exists():
        raise FileNotFoundError(f'Fixture não encontrada: {dump_path}')

    with dump_path.open(encoding='utf-16') as handle:
        payload = json.load(handle)

    return Counter(item['model'] for item in payload)


def main() -> None:
    dump_counts = load_dump_counts()
    interesting_models = [
        'auth.user',
        'auth.group',
        'admin.logentry',
        'sessions.session',
        'sistema.coordenador',
        'sistema.professor',
        'sistema.aluno',
        'sistema.disciplina',
        'sistema.turma',
        'sistema.turmadisciplina',
        'sistema.alunomodulo',
        'sistema.atividade',
        'sistema.alunoatividade',
        'sistema.aula',
    ]

    issues = []

    print('Comparando registros exportados com o banco SQLite atual:')
    for label in interesting_models:
        try:
            model = apps.get_model(label)
        except LookupError:
            issues.append(f'Modelo ausente no projeto: {label}')
            continue

        exported = dump_counts.get(label, 0)
        actual = model.objects.count()
        status = 'OK' if actual == exported else 'MISMATCH'
        padding = ' ' * max(1, 35 - len(label))
        print(f'  {label}{padding}DB={actual:<4} dump={exported:<4} {status}')

        if actual != exported:
            issues.append(f'{label}: banco {actual} vs dump {exported}')

    if issues:
        print('\nInconsistências encontradas:')
        for issue in issues:
            print('-', issue)
        sys.exit(1)

    print('\nTodos os dados do SQLite estão refletidos no dump exportado.')


if __name__ == '__main__':
    main()
