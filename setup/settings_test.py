"""
Settings temporário para testes locais sem Docker/PostgreSQL.
Usa SQLite em memória. NÃO commitar este arquivo.
"""
from setup.settings import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
