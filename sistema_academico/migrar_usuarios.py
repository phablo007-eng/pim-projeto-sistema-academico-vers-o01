"""
Script para migrar dados de Usuario customizado para User nativo do Django.
Execute ANTES de rodar a migração 0006.

Uso:
    python migrar_usuarios.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_academico.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import connection

def migrar_usuarios():
    """Migra registros da tabela sistema_usuario para auth_user"""
    
    with connection.cursor() as cursor:
        # Verificar se a tabela antiga existe
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='sistema_usuario'
        """)
        
        if not cursor.fetchone():
            print(" Tabela sistema_usuario não encontrada. Já foi migrada?")
            return
        
        # Buscar todos os usuários antigos
        cursor.execute("SELECT id, nome, email, criado_em FROM sistema_usuario")
        usuarios_antigos = cursor.fetchall()
        
        if not usuarios_antigos:
            print(" Nenhum usuário para migrar.")
            return
    
        print(f"📋 Encontrados {len(usuarios_antigos)} usuários para migrar...")
        
        migrados = 0
        for user_id, nome, email, criado_em in usuarios_antigos:
            # Verificar se já existe
            if User.objects.filter(id=user_id).exists():
                print(f"⏭️  User ID {user_id} já existe, pulando...")
                continue
            
            # Separar nome em first_name e last_name
            partes_nome = nome.split(' ', 1)
            first_name = partes_nome[0] if partes_nome else ''
            last_name = partes_nome[1] if len(partes_nome) > 1 else ''
            
            # Criar username a partir do email
            username = email.split('@')[0]
            
            # Se username já existe, adicionar sufixo
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            # Criar o User com o mesmo ID
            user = User.objects.create(
                id=user_id,
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_active=True,
                is_staff=False,
                is_superuser=False,
            )
            
            # Definir uma senha padrão (DEVE SER ALTERADA!)
            user.set_password('senha123')
            user.save()
            
            print(f"✅ Migrado: {nome} -> username: {username}")
            migrados += 1
        
        print(f"\n🎉 Migração concluída! {migrados} usuários migrados.")
        print("\n⚠️  IMPORTANTE: Todos os usuários foram criados com senha padrão 'senha123'")
        print("   Oriente os usuários a alterarem suas senhas!")

if __name__ == '__main__':
    print("🚀 Iniciando migração de usuários...\n")
    migrar_usuarios()
