from pydantic import BaseModel
from typing import Optional, List
from model.estabelecimento import Estabelecimento

from schemas.produto import ProdutoViewSchema


class EstabelecimentoSchema(BaseModel):
    """ Define como um novo produto a ser inserido deve ser representado
    """
    nome: str = "Loja"


class EstabelecimentoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do produto.
    """
    id: int = 1


class ListagemEstabelecimentosSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    estabelecimentos:List[EstabelecimentoSchema]


def apresenta_estabelecimentos(estabelecimentos: List[Estabelecimento]):
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
    produtos: List[ProdutoViewSchema]

    class Config:
        orm_mode = True

class EstabelecimentoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str
    
def apresenta_estabelecimento(estabelecimento: Estabelecimento):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "id": estabelecimento.id,
        "nome": estabelecimento.nome
    }

class Config:
        orm_mode = True