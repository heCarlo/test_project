"""
este módulo define a base declarativa para modelos ORM usando sqlalchemy

a base declarativa é usada como uma classe base para todos os modelos do banco de dados
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()
