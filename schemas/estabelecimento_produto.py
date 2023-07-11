from pydantic import BaseModel
from typing import Optional, List
from model.estabelecimentoProduto import EstabelecimentoProduto

from schemas.estabelecimento import EstabelecimentoSchema, EstabelecimentoViewSingleSchema
from schemas import *


class EstabelecimentoProdutoSchema(BaseModel):
    """ Define como um novo estabelecimento a ser inserido deve ser representado
    """
    produto: ProdutoViewSchema
    estabelecimento: EstabelecimentoViewSingleSchema

class EstabelecimentoProdutoViewSchema(BaseModel):
    """ Define como um estabelecimento será retornado: estabelecimento + produto.
    """
    id: int = None
    estabelecimento = EstabelecimentoSchema
    produto = ProdutoViewSchema


class EstabelecimentoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do Estabelecimento Produto.
    """
    id: int = 1

class EstabelecimentoViewSchema(BaseModel):
    """ Define como um Estabelecimento Produto será retornado: id + nome.
    """
    id: int = 1
    nome: str = "Loja"
