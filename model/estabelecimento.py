from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union
from sqlalchemy.orm import relationship


from  model import Base

from dataclasses import dataclass

from model.produto import Produto

@dataclass
class Estabelecimento(Base):
    __tablename__ = 'estabelecimento'

    id = Column("id", Integer, primary_key=True)
    nome = Column(String(255))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o estabelecimento e produtos.
    # Aqui está sendo definido o relacionamento many-to-many com produtos
    produtos = relationship('Produto', secondary='estabelecimento_produto', back_populates='estabelecimentos')
    

    def __init__(self, nome:str, data_insercao:Union[DateTime, None] = None):
        """
        Cria um Estabelecimento

        Arguments:
            nome: o nome do estabelecimento.
            data_insercao: data de quando o estabelecimento foi feito ou inserido
                           à base
        """
        self.nome = nome
        if data_insercao:
            self.data_insercao = data_insercao

    def __str__(self):
        return '{} {}'.format(self.id, self.nome)
    
    def adiciona_produto(self, produto: Produto):
        """ Adiciona um novo produto ao Estabelecimento
        """
        self.produtos.append(produto)

    
    