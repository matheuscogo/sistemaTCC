from ast import arg
from datetime import datetime
from re import I
from xmlrpc.client import ResponseError
from ..site.model import Inseminacao
from ..site.model import Matriz
from ..site.model import Confinamento
from ..site.model import Plano
from ..site.model import InseminacaoSchema
from ..db import db
from werkzeug.wrappers import Response, Request
import json

def cadastrarInseminacao(inseminacao, isNewCiclo):  # Create
    try:
        if not inseminacao.matrizId:
            raise Exception(ResponseError)

        if not inseminacao.planoId:
            raise Exception(ResponseError)

        if not inseminacao.dataInseminacao:
            raise Exception(ResponseError)

        matriz = db.session.query(Matriz).filter_by(
            id=inseminacao.matrizId, deleted=False).first()
        confinamento = db.session.query(Confinamento).filter_by(
            matrizId=inseminacao.matrizId, active=True).first()
        oldInseminacao = db.session.query(Inseminacao).filter_by(
            matrizId=inseminacao.matrizId, active=True).first()

        if oldInseminacao:
            oldInseminacao.active = False
            oldInseminacao.deleted = True

        if confinamento:
            confinamento.active = False
            confinamento.deleted = True
            
        newConfinamento = Confinamento(
            planoId=inseminacao.planoId,
            matrizId=inseminacao.matrizId,
            dataConfinamento=inseminacao.dataInseminacao
        )   
        
        db.session.add(newConfinamento)
        db.session.flush()
        
        inseminacao.confinamentoId = newConfinamento.id 
        
        if isNewCiclo:
            matriz.ciclos = matriz.ciclos + 1

        newInseminacao = inseminacao
        # adicionar uma chave estrangeira na tabela inseminação para saber qual confinamento ela pertence
        db.session.add(newInseminacao)
        db.session.commit()
        return Response(response=json.dumps("{success: true, message: Inseminacao cadastrado com sucesso!, response: null}"), status=200)
    except BaseException as e:
        return Response(response=json.dumps("{success: false, message: " + e.args[0] + ", response: null}"), status=501)
    finally:
        db.session.close()


def consultarInseminacoes():  # Read
    try:
        response = db.session.query(Inseminacao).filter_by(
            deleted=False, active=True).all()
        inseminacoes = []

        for inseminacao in response:
            matrizDescription = db.session.query(Matriz).filter_by(
                id=int(inseminacao.matrizId), deleted=False).first()
            planoDescription = db.session.query(Plano).filter_by(
                id=int(inseminacao.planoId), active=True, deleted=False).first()
            obj = {"id": inseminacao.id, "planoDescription": planoDescription.nome,
                   "matrizDescription": matrizDescription.rfid, "dataInseminacao": inseminacao.dataInseminacao}
            inseminacoes.append(obj)

        return inseminacoes
    except BaseException as e:
        return Response(response=json.dumps("{success: false, message: " + e.args[0] + ", response: null}"), status=501)


def consultarInseminacao(id):  # Read
    try:
        inseminacao = db.session.query(Inseminacao).filter_by(id=id).first()
        return InseminacaoSchema().dump(inseminacao)
    except Exception as e:
        return Response(response=json.dumps("{success: false, message: " + e.args[0] + ", response: null}"), status=501)


def atualizarInseminacao(args):  # Update
    try:
        matriz = int(args['matriz'])
        dataInseminacao = str(args['dataInseminacao'])

        inseminacao = db.session.query(Inseminacao).filter_by(id=id).first()
        inseminacao.matrizId = matriz
        inseminacao.dataInseminacao = dataInseminacao
        db.session.commit()
        return Response(response=json.dumps("{success: true, message: Inseminacao atualizado com sucesso!, response: null}"), status=200)
    except BaseException as e:
        return Response(response=json.dumps("{success: false, message: " + e.args[0] + ", response: null}"), status=501)


def excluirInseminacao(id):  # Delete
    try:
        inseminacao = db.session.query(Inseminacao).filter_by(id=id).first()
        db.session.delete(inseminacao)
        db.session.commit()
        return Response(response=json.dumps("{success: true, message: Inseminacao excluido com sucesso!, response: null}"), status=200)
    except BaseException as e:
        return Response(response=json.dumps("{success: false, message: " + e.args[0] + ", response: null}"), status=501)
