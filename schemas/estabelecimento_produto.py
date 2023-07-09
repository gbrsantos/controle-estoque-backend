from pydantic import BaseModel
from typing import Optional, List
from model.estabelecimentoProduto import EstabelecimentoProduto

from schemas.estabelecimento import EstabelecimentoSchema, EstabelecimentoViewSingleSchema
from schemas import *


class EstabelecimentoProdutoSchema(BaseModel):
    """ Define como um novo produto a ser inserido deve ser representado
    """
    produto: ProdutoViewSchema
    estabelecimento: EstabelecimentoViewSingleSchema

class EstabelecimentoProdutoViewSchema(BaseModel):
    """ Define como um produto será retornado: produto + comentários.
    """
    id: int = None
    estabelecimento = EstabelecimentoSchema
    produto = ProdutoViewSchema


class EstabelecimentoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do produto.
    """
    id: int = 1


# class ListagemEstabelecimentosSchema(BaseModel):
#     """ Define como uma listagem de produtos será retornada.
#     """
#     estabelecimentos:List[EstabelecimentoSchema]


def apresenta_estabelecimentos_produtos(estabelecimentos: List[EstabelecimentoProduto]):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    result = []
    for estabelecimento in estabelecimentos: 
        result.append({
            "id": estabelecimento.id,
            "nome": estabelecimento.nome
        })

    return {"estebelecimentos": result}


class EstabelecimentoViewSchema(BaseModel):
    """ Define como um produto será retornado: produto + comentários.
    """
    id: int = 1
    nome: str = "Loja"

class EstabelecimentoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_estabelecimento_produto(estabelecimento: EstabelecimentoProduto):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "id": estabelecimento.id,
        "nome": estabelecimento.nome
    }

