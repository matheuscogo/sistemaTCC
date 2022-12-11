from ext.site.model import Inseminacao
from ..site.model import Confinamento
from ..site.model import Registro
from ..site.model import ConfinamentoSchema
from ..db import db
import datetime
from werkzeug.wrappers import Response, Request
from xmlrpc.client import ResponseError
import json
from ..site.model import Dia
from ..site.model import Aviso
from ..site.model import Plano
from ..site.model import Matriz
from ..site.model import Registro
from ..db import db
from sqlalchemy.sql import func
from datetime import datetime

def cadastrarConfinamento(newConfinamento):  # Create
    try:
        if not newConfinamento.matrizId:
            raise Exception(ResponseError)

        if not newConfinamento.planoId:
            raise Exception(ResponseError)
            
        if not newConfinamento.dataConfinamento:
            raise Exception(ResponseError)
        
        hasInseminacao = db.session.query(Inseminacao.query.filter_by(matrizId=newConfinamento.matrizId, active=True, deleted=False).exists()).scalar()
        if hasInseminacao:
            raise Exception("Existe uma inseminação ativa para essa matriz.")
        
        hasConfinamento = db.session.query(Confinamento.query.filter_by(matrizId=newConfinamento.matrizId, active=True, deleted=False).exists()).scalar()
        if hasConfinamento:
            confinamento = db.session.query(Confinamento).filter_by(matrizId=newConfinamento.matrizId, active=True, deleted=False).first()
            confinamento.active = False
            confinamento.deleted = True
            db.session.flush()
            
        db.session.add(newConfinamento)
        db.session.commit()
        
        response = {
            'success': True,
            'response': {},
            'message': "Confinamento cadastrado com sucesso!"
        }
            
        return response
    except BaseException as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return  response
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
    
    
def consultarConfinamento(id):  # Read
    try:
        confinamento = db.session.query(
            Confinamento.id,
            Confinamento.dataConfinamento,
            Matriz.numero.label('numeroMatriz'),
            Confinamento.matrizId.label('matrizId'),
            Plano.nome.label('planoNome'),
            Plano.id.label('planoId'),
            Confinamento.active
        ).join(Matriz).join(Plano).filter(
            Confinamento.id == id,
            Confinamento.deleted==False, 
            Confinamento.active==True,
            Matriz.deleted==False,
            Plano.deleted==False
        ).first()

        response = {
            'success': True,
            'response': {
                "id": confinamento.id, 
                "plano": {
                    'description': confinamento.planoNome,
                    'value': confinamento.planoId
                }, 
                "matriz": {
                    'description': confinamento.numeroMatriz,
                    'value': confinamento.matrizId
                }, 
                "dataConfinamento": confinamento.dataConfinamento,
                "active": confinamento.active
            },
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

def consultarConfinamentos():  # Read
    try:
        response = db.session.query(
            Confinamento.id,
            Confinamento.dataConfinamento,
            Matriz.numero.label('numeroMatriz'),
            Confinamento.matrizId.label('matrizId'),
            Plano.nome.label('planoNome'),
            Plano.id.label('planoId'),
            Confinamento.active
        ).join(Matriz).join(Plano).filter(
            Confinamento.deleted==False, 
            Confinamento.active==True,
            Matriz.deleted==False,
            Plano.deleted==False
        ).all()
        
        confinamentos = []

        for confinamento in response:
            obj = {
                "id": confinamento.id, 
                "plano": {
                    'description': confinamento.planoNome,
                    'value': confinamento.planoId
                }, 
                "matriz": {
                    'description': confinamento.numeroMatriz,
                    'value': confinamento.matrizId
                }, 
                "dataConfinamento": confinamento.dataConfinamento,
                "active": confinamento.active
            }
            
            confinamentos.append(obj)
            
        response = {
            'success': True,
            'response': confinamentos,
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

def atualizarConfinamento(id, newConfinamento):
    try:
        if id is None:
            raise Exception("Confinamento não repassada para o controlador.")
        
        if not newConfinamento.planoId:
            raise Exception("Plano não repasado para o controlador.")
            
        if not newConfinamento.dataConfinamento:
            raise Exception("Data do confinamento não repasado para o controlador.")
        
        confinamento = db.session.query(Confinamento).filter_by(id=id, deleted=False).first()
        
        hasInseminacao = db.session.query(Inseminacao.query.filter_by(matrizId=confinamento.matrizId, active=True, deleted=False).exists()).scalar()
        if hasInseminacao:
            raise Exception("Existe uma inseminação ativa para essa matriz.")

        confinamento.dataConfinamento = newConfinamento.dataConfinamento
        confinamento.planoId = newConfinamento.planoId
        confinamento.active = newConfinamento.active
        
        db.session.add(confinamento)
        db.session.commit()
        
        response = {
            'success': True,
            'response': {},
            'message': "Confinamento atualizado com sucesso!"
        }
            
        return response
    except BaseException as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return  response

def excluirConfinamento(id):  # Delete
    try:
        if id is None:
            raise Exception("Confinamento não repassada para o controlador.")
        
        confinamento = db.session.query(Confinamento).filter_by(id=id, deleted=False).first()
        
        hasInseminacao = db.session.query(Inseminacao.query.filter_by(matrizId=confinamento.matrizId, active=True, deleted=False).exists()).scalar()
        if hasInseminacao:
            raise Exception("Existe uma inseminação ativa para essa matriz.")

        confinamento.deleted = True
        
        db.session.commit()
        
        response = {
            'success': True,
            'response': {},
            'message': "Confinamento excluida com sucesso!"
        }
            
        return response
    except BaseException as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return  response
