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
    produtos = relationship('Produto', secondary='estabelecimento_produto', back_populates='estabelecimentos')

    
    # Definição do relacionamento entre o comentário e um produto.
    # Aqui está sendo definido a coluna 'produto' que vai guardar
    # a referencia ao produto, a chave estrangeira que relaciona
    # um produto ao comentário.

    #produto = Column(Integer, ForeignKey("produto.pk_produto"), nullable=False)
    

    def __init__(self, nome:str, data_insercao:Union[DateTime, None] = None):
        """
        Cria um Estabelecimento

        Arguments:
            texto: o texto de um comentário.
            data_insercao: data de quando o comentário foi feito ou inserido
                           à base
        """
        self.nome = nome
        if data_insercao:
            self.data_insercao = data_insercao

    def __str__(self):
        return '{} {}'.format(self.id, self.nome)
    
    def adiciona_produto(self, produto: Produto):
        """ Adiciona um novo comentário ao Produto
        """
        self.produtos.append(produto)

    
    