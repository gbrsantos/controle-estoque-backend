from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base

class EstabelecimentoProduto(Base):
    __tablename__ = "estabelecimento_produto"

    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey('produto.id'))
    estabelecimento_id = Column(Integer, ForeignKey('estabelecimento.id'))
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, id_produto:int, id_estabelecimento:int, data_insercao:Union[DateTime, None] = None):
        """
        Cria um EstabelecimentoProduto

        Arguments:
            produto_id: foreing key de produto.
            estabelecimento_id: foreing key de estabelecimento.
            data_insercao: data de quando o EstabelecimentoProduto foi feito ou inserido
                           à base
        """
        self.produto_id = id_produto
        self.estabelecimento_id = id_estabelecimento
        if data_insercao:
            self.data_insercao = data_insercao

    #Define como será o retorno do objeto formatado para string    
    def __str__(self):        
        return '{} {}'.format(self.produto_id, self.estabelecimento_id)        