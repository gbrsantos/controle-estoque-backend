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
        Cria um Estabelecimento

        Arguments:
            texto: o texto de um comentário.
            data_insercao: data de quando o comentário foi feito ou inserido
                           à base
        """
        self.id_produto = id_produto
        self.id_estabelecimento = id_estabelecimento
        if data_insercao:
            self.data_insercao = data_insercao