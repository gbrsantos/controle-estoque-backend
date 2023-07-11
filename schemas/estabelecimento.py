from pydantic import BaseModel
from typing import Optional, List
from model.estabelecimento import Estabelecimento

from schemas.produto import ProdutoViewSchema


class EstabelecimentoSchema(BaseModel):
    """ Define como um novo estabelecimento a ser inserido deve ser representado
    """
    nome: str = "Loja"


class EstabelecimentoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do estabelecimento.
    """
    id: int = 1


class ListagemEstabelecimentosSchema(BaseModel):
    """ Define como uma listagem de estabelecimento será retornada.
    """
    estabelecimentos:List[EstabelecimentoSchema]


class EstabelecimentoViewSchema(BaseModel):
    """ Define como um estabelecimento será retornado: estabelecimento + produtos.
    """
    id: int = 0
    nome: Optional[str] = ""   
    produtos: Optional[List[ProdutoViewSchema]]

    class Config:
        orm_mode = True        

class EstabelecimentoViewSingleSchema(BaseModel):
    """ Define como um estabelecimento será retornado: id + nome.
    """
    id: int = 1
    nome: str = "Loja"
    class Config:
        orm_mode = True

class EstabelecimentoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str
    
def apresenta_estabelecimento(estabelecimento: Estabelecimento):
    """ Retorna uma representação do estabelecimento seguindo o schema definido em
        EstabelecimentoViewSchema.
    """
    return {
        "id": estabelecimento.id,
        "nome": estabelecimento.nome
    }


def apresenta_estabelecimentos(estabelecimentos: List[Estabelecimento]):
    """ Retorna uma representação do estabelecimento seguindo o schema definido em
        EstabelecimentoViewSchema.
    """
    result = []
    for estabelecimento in estabelecimentos: 
        result.append({
            "id": estabelecimento.id,
            "nome": estabelecimento.nome
        })

    return {"estabelecimentos": result}