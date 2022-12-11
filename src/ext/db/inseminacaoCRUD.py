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

def cadastrarInseminacao(newInseminacao, planoId, isNewCiclo):  # Create
    try:
        if not newInseminacao.matrizId:
            raise Exception("Matriz não repassada para o controlador.")

        if not planoId:
            raise Exception("Plano não repassada para o controlador.")

        if not newInseminacao.dataInseminacao:
            raise Exception("Data da inseminação não repassada para o controlador.")
        
        hasConfinamento = db.session.query(Confinamento.query.filter_by(matrizId=newInseminacao.matrizId, active=True, deleted=False).exists()).scalar()
        if hasConfinamento:
            confinamento = db.session.query(Confinamento).filter_by(
                matrizId=newInseminacao.matrizId, active=True).first()
            
            confinamento.active = False
            confinamento.deleted = True
        
            db.session.flush()
            
        hasInseminacao = db.session.query(Inseminacao.query.filter_by(matrizId=newInseminacao.matrizId, active=True, deleted=False).exists()).scalar()
        if hasInseminacao:
            inseminacao = db.session.query(Inseminacao).filter_by(
                matrizId=newInseminacao.matrizId, active=True).first()

            inseminacao.active = False
            inseminacao.deleted = True

            db.session.flush()
        
        if isNewCiclo:
            matriz = db.session.query(Matriz).filter_by(
                id=newInseminacao.matrizId, deleted=False).first()
            
            matriz.ciclos = matriz.ciclos + 1
            db.session.flush()
        
        newConfinamento = Confinamento(
            planoId=planoId,
            matrizId=newInseminacao.matrizId,
            dataConfinamento=newInseminacao.dataInseminacao,
            active=newInseminacao.active,
            deleted=newInseminacao.deleted,
        )   
        
        # adicionar uma chave estrangeira na tabela inseminação para saber qual confinamento ela pertence
        db.session.add(newConfinamento)
        db.session.flush()
        
        newInseminacao.confinamentoId = newConfinamento.id
        
        db.session.add(newInseminacao)
        db.session.commit()
        
        response = {
            'success': True,
            'response': {},
            'message': "Inseminação cadastrada com sucesso!"
        }
            
        return response
    except BaseException as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return  response
    
    except Exception as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return  response



def consultarInseminacoes():  # Read
    try:
        response = db.session.query(
            Inseminacao.id,
            Inseminacao.dataInseminacao,
            Confinamento.matrizId.label('matrizId'),
            Matriz.numero.label('numeroMatriz'),
            Plano.nome.label('planoNome'),
            Plano.id.label('planoId'),
            Confinamento.id.label("confinamentoId"),
            Confinamento.dataConfinamento.label("dataConfinamento"),
            Inseminacao.active
        ).join(
            Confinamento,
            Inseminacao.confinamentoId == Confinamento.id 
        ).join(
            Plano,
            Plano.id == Confinamento.planoId
        ).join(
            Matriz,
            Matriz.id == Confinamento.matrizId
        ).filter(
            Confinamento.active == True,
            Confinamento.deleted == False,
            Inseminacao.deleted==False, 
            Inseminacao.active==True,
            Matriz.deleted==False,
            Plano.deleted==False
        ).all()
                
        inseminacoes = []

        for inseminacao in response:
            obj = {
                "id": inseminacao.id, 
                "confinamento": {
                    'description': inseminacao.dataConfinamento,
                    'value': inseminacao.confinamentoId
                }, 
                "plano": {
                    'description': inseminacao.planoNome,
                    'value': inseminacao.planoId
                }, 
                "matriz": {
                    'description': inseminacao.numeroMatriz,
                    'value': inseminacao.matrizId
                }, 
                "dataInseminacao": inseminacao.dataInseminacao,
                "active": inseminacao.active
            }
            
            inseminacoes.append(obj)
            
        response = {
            'success': True,
            'response': inseminacoes,
            'message': ""
        }
            
        return response
    except BaseException as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return  response


def consultarInseminacao(id):  # Read
    try:
        if id is None:
            raise Exception("Inseminação não repassada para o controlador.")
        
        inseminacao = db.session.query(Inseminacao).filter_by(id=id).first()
        
        response = {
            'success': True,
            'response': inseminacao,
            'message': ""
        }
            
        return response
    except BaseException as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return  response
    except Exception as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return  response


def atualizarInseminacao(id, newInseminacao):  # Update
    try:
        if id is None:
            raise Exception("Inseminação não repassada para o controlador.")
        
        if not newInseminacao.matrizId:
            raise Exception("Matriz não repassada para o controlador.")

        if not newInseminacao.planoId:
            raise Exception("Plano não repassada para o controlador.")

        if not newInseminacao.dataInseminacao:
            raise Exception("Data da inseminação não repassada para o controlador.")

        hasInseminacao = db.session.query(Inseminacao.query.filter_by(id=id, deleted=False).exists()).scalar()
        
        if not hasInseminacao:
            raise BaseException("Inseminação não encontrada.")
        
        inseminacao = db.session.query(Inseminacao).filter_by(id=id, deleted=False).first()
        
        inseminacao.matrizId = newInseminacao.matrizId
        inseminacao.planoId = newInseminacao.planoId
        inseminacao.confinamentoId = newInseminacao.confinamentoId
        inseminacao.dataInseminacao = newInseminacao.dataInseminacao
        inseminacao.active = newInseminacao.active
        
        db.session.commit()
        
        response = {
            'success': True,
            'response': {},
            'message': "Inseminação atualizada com sucesso!"
        }
            
        return response
    except BaseException as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return  response
    except Exception as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return  response


def excluirInseminacao(id):  # Delete
    try:
        if id is None:
            raise Exception("Inseminação não repassada para o controlador.")
        
        hasInseminacao = db.session.query(Inseminacao.query.filter_by(id=id, active=True, deleted=False).exists()).scalar()
        if hasInseminacao:
            inseminacao = db.session.query(Inseminacao).filter_by(id=id, deleted=False).first()
            
            hasConfinamento = db.session.query(Confinamento.query.filter_by(matrizId=inseminacao.matrizId, active=True, deleted=False).exists()).scalar()
            if hasConfinamento:
                confinamento = db.session.query(Confinamento).filter_by(matrizId=inseminacao.matrizId, active=True, deleted=False).first()
                confinamento.active = False
                confinamento.deleted = True
                db.session.flush()
                
            inseminacao.deleted = True
            inseminacao.active = False
            
            db.session.flush()
            
        db.session.commit()
        
        response = {
            'success': True,
            'response': {},
            'message': "Inseminação excluida com sucesso!"
        }
            
        return response
    except BaseException as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return  response
    except Exception as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return  response
