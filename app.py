from ast import List
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from sqlalchemy.orm import  joinedload

from sqlalchemy.exc import IntegrityError

from model import Session, Produto, Estabelecimento, EstabelecimentoProduto
from logger import logger
from schemas import *
from flask_cors import CORS
import json


info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(name="Produto", description="Adição, visualização e remoção de produtos à base")
estabelecimento_tag = Tag(name="Estabelecimento", description="Adição, visualização e remoção de estabelecimento à base")
estabelecimento_produto_tag = Tag(name="Estabelecimento Produto", description="Adição de estabelecimento-produto à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/estabelecimento', tags=[estabelecimento_tag],
          responses={"200": EstabelecimentoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_estabelecimento(body: EstabelecimentoSchema):
    """Adiciona um novo Estabelecimento à base de dados
    Retorna uma representação dos estabelecimento e produtos associados.
    """
    estabelecimento = Estabelecimento(
        nome=body.nome)
    #logger.debug(f"Adicionando estabelecimento de nome: '{estabelecimento.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(estabelecimento)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        #logger.debug(f"Adicionado produto de nome: '{estabelecimento.nome}'")
        return apresenta_estabelecimento(estabelecimento), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Estabelecimento de mesmo nome já salvo na base :/"
        #logger.warning(f"Erro ao adicionar estabelecimento '{estabelecimento.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        #faz o rollback da transação
        session.rollback()
        # caso um erro fora do previsto
        error_msg = "Um erro não identificado ocorreu :/"
        #logger.warning(f"Erro ao adicionar estabelecimento '{estabelecimento.nome}', {error_msg}")
        return {"mesage": error_msg}, 400
    finally:
        session.close()

@app.delete('/estabelecimento', tags=[estabelecimento_tag],
         responses={"200": EstabelecimentoViewSchema, "404": ErrorSchema})
def delete_estabelecimento(query: EstabelecimentoViewSchema):
    """Faz o delete de um Estabelecimento a partir do id do estabelecimento    
    Retorna uma representação do estabelecimento removido.
    """
    id_estabelecimento = query.id
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca com join produtos
        ##logger.debug(f"Coletando dados sobre estabelecimento #{id_estabelecimento}")
        estabelecimento = session.query(Estabelecimento).options(joinedload(Estabelecimento.produtos)).\
        where(Estabelecimento.id == id_estabelecimento).one()
        if not estabelecimento:
            # se o estabelecimento não foi encontrado
            error_msg = "Produto não encontrado na base :/"
            ##logger.warning(f"Erro ao buscar estabelecimento '{id_estabelecimento}', {error_msg}")
            return {"mesage": error_msg}, 404
        else:
            ##logger.debug(f"Estabelecimento econtrado: '{estabelecimento.nome}'")
            # faz o delete de estabelecimento
            session.delete(estabelecimento)
            session.commit()
            #retorna uma visao de estabelecimento como json
            result = EstabelecimentoViewSchema.from_orm(estabelecimento)
            return result.json(), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Um erro não identificado ocorreu  :/"
        print(e)
        ##logger.warning(f"Erro ao adicionar estabelecimento '{estabelecimento.nome}', {error_msg}")
        return {"mesage": error_msg}, 400
    finally:
        session.close()

@app.get('/estabelecimento', tags=[estabelecimento_tag],
         responses={"200": EstabelecimentoViewSchema, "404": ErrorSchema})
def get_estabelecimento(query: EstabelecimentoViewSchema):
    """Faz a busca por um Estabelecimento a partir do id do produto
    Retorna uma representação do estabelecimento e produtos associados.
    """    
    id_estabelecimento = query.id
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        ##logger.debug(f"Coletando dados sobre estabelecimento #{id}")
        estabelecimento = session.query(Estabelecimento).options(joinedload(Estabelecimento.produtos)).\
        where(Estabelecimento.id == id_estabelecimento).one()
        if not estabelecimento:
            # se o estabelecimento não foi encontrado
            error_msg = "Produto não encontrado na base :/"
           # #logger.warning(f"Erro ao buscar estabelecimento '{id_estabelecimento}', {error_msg}")
            return {"mesage": error_msg}, 404
        else:
            ##logger.debug(f"Estabelecimento econtrado: '{estabelecimento.nome}'")
            # retorna a representação de estabelecimento em json
            result = EstabelecimentoViewSchema.from_orm(estabelecimento)
            return result.json(), 200

    except Exception as e:
        # caso um erro fora do previsto
        #faz o rollback da transação
        session.rollback()
        error_msg = "Um erro não identificado ocorreu :/"
        print(e)
        ##logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {"mesage": error_msg}, 400
    finally:
        session.close()

@app.get('/estabelecimentos', tags=[estabelecimento_tag],
         responses={"200": ListagemEstabelecimentosSchema, "404": ErrorSchema})
def get_estabelecimentos():
    """Faz a busca de todos os estabelecimentos    
    Retorna uma representação dos estabelecimentos.
    """    
    try:
        #logger.debug(f"Coletando dados sobre produto #{id}")
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        estabelecimentos = session.query(Estabelecimento).options(joinedload(Estabelecimento.produtos)).all()

        # retorna a representação de estabelecimentos
        retorno :EstabelecimentoViewSchema = []
        for estab in estabelecimentos:
                retorno.append(EstabelecimentoViewSchema.from_orm(estab))    
       
        return apresenta_estabelecimentos(estabelecimentos)
  
    except Exception as e:
        # caso um erro fora do previsto
        #faz o rollback da transação
        session.rollback()
        error_msg = "Um erro não identificado ocorreu  :/"
        print(e)
        #logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {"mesage": error_msg}, 400  
    finally:
        session.close()

@app.post('/produto', tags=[produto_tag],
          responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_produto(body: ProdutoSchema):
    """Adiciona um novo Produto à base de dados

    Retorna uma representação dos produtos.
    """
    produto = Produto(
        nome=body.nome,
        valor=body.valor)
    
    try:
        #logger.debug(f"Adicionando produto de nome: '{produto.nome}'")
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(produto)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        #logger.debug(f"Adicionado produto de nome: '{produto.nome}'")
        return apresenta_produto(produto), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Produto de mesmo nome já salvo na base :/"
        #logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        #faz o rollback da transação
        session.rollback()
        error_msg = "Um erro não identificado ocorreu  :/"
        print(e)
        #logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {"mesage": error_msg}, 400
    finally:
        session.close()

@app.get('/produtos', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
def get_produtos():
    """Faz a busca por todos os Produto cadastrados

    Retorna uma representação da listagem de produtos.
    """
    try:
    #logger.debug(f"Coletando produtos ")
    # criando conexão com a base
        session = Session()
        # fazendo a busca
        produtos = session.query(Produto).all()

        if not produtos:
            # se não há produtos cadastrados
            return {"produtos": []}, 200
        else:
            #logger.debug(f"%d rodutos econtrados" % len(produtos))
            # retorna a representação de produto
            print(produtos)
            return apresenta_produtos(produtos), 200
    except Exception as e:
        #faz o rollback da transação
        session.rollback()
        # caso um erro fora do previsto
        error_msg = "Um erro não identificado ocorreu :/"
        print(e)
        #logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {"mesage": error_msg}, 400       
    finally:
        session.close()

@app.get('/produto', tags=[produto_tag],
         responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def get_produto(query: ProdutoBuscaSchema):
    """Faz a busca por um Produto a partir do id do produto

    Retorna uma representação dos produtos e comentários associados.
    """
    try:

        produto_id = query.id
        #logger.debug(f"Coletando dados sobre produto #{produto_id}")
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        produto = session.query(Produto).filter(Produto.id == produto_id).first()

        if not produto:
            # se o produto não foi encontrado
            error_msg = "Produto não encontrado na base :/"
            #logger.warning(f"Erro ao buscar produto '{produto_id}', {error_msg}")
            return {"mesage": error_msg}, 404
        else:
            #logger.debug(f"Produto econtrado: '{produto.nome}'")
            # retorna a representação de produto
            return apresenta_produto(produto), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Um erro não identificado ocorreu  :/"
        print(e)
        #logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {"mesage": error_msg}, 400
    finally:
        session.close()

@app.delete('/produto', tags=[produto_tag],
            responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def del_produto(query: ProdutoBuscaSchema):
    """Deleta um Produto a partir do nome de produto informado

    Retorna uma mensagem de confirmação da remoção.
    """
    try:
        produto_nome = unquote(unquote(query.nome))
        print(produto_nome)
        #logger.debug(f"Deletando dados sobre produto #{produto_nome}")
        # criando conexão com a base
        session = Session()
        # fazendo a remoção
        count = session.query(Produto).filter(Produto.nome == produto_nome).delete()
        session.commit()

        if count:
            # retorna a representação da mensagem de confirmação
            #logger.debug(f"Deletado produto #{produto_nome}")
            return {"mesage": "Produto removido", "id": produto_nome}
        else:
            # se o produto não foi encontrado
            error_msg = "Produto não encontrado na base :/"
            #logger.warning(f"Erro ao deletar produto #'{produto_nome}', {error_msg}")
            return {"mesage": error_msg}, 404
        
    except Exception as e:
        #faz o rollback da transação
        session.rollback()
        # caso um erro fora do previsto
        error_msg = "Um erro não identificado ocorreu :/"
        print(e)
        #logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {"mesage": error_msg}, 400    
    finally:
        session.close()

@app.post('/estabelecimento-produto', tags=[estabelecimento_produto_tag],
          responses={"200": EstabelecimentoProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_estabelecimento_produto(body: EstabelecimentoProdutoSchema):
    """Adiciona um novo Estabelecimento Produto à base de dados

    Retorna uma representação do estabelecimento produto.
    """
    estabelecimentoProduto = EstabelecimentoProduto(
        body.estabelecimento.id,
        body.produto.id)
    ##logger.debug(f"Adicionando produto de nome: '{estabelecimento.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        #faz a busca do estabelecimento
        estabelecimentoBuscado = session.query(Estabelecimento).filter(Estabelecimento.id == estabelecimentoProduto.estabelecimento_id).first()
        #faz a busca do produto
        produto = session.query(Produto).filter(Produto.id == estabelecimentoProduto.produto_id).first()
        if not (produto or estabelecimentoBuscado): 
            error_msg = "Produto ou estabelecimento não encontrado na base :/"
            #logger.warning(f"Erro ao buscar produto ou estabelecimento, {error_msg}")
            return {"mesage": error_msg}, 404
        
        session.add(estabelecimentoProduto)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        ##logger.debug(f"Adicionado produto de nome: '{estabelecimento.nome}'")
        return apresenta_estabelecimento(estabelecimentoBuscado), 200

    except Exception as e:  
        #faz o rollback da transação
        session.rollback()  
        # caso um erro fora do previsto
        error_msg = "Um erro não identificado ocorreu  :/"
        print(e)
        ##logger.warning(f"Erro ao adicionar produto '{estabelecimento.nome}', {error_msg}")
        return {"mesage": error_msg}, 400
    finally:
        session.close()