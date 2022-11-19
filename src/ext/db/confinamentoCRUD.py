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
        confinamento = db.session.query(Confinamento).filter_by(id=id, deleted=False).first()
        
        response = {
            'success': True,
            'response': confinamento,
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


def getConfinamentoByMatriz(matrizId):
    try:
        confinamento = db.session.query(Confinamento.Confinamento).filter_by(matrizId=matrizId, active=True, deleted=False).first()
        return ConfinamentoSchema().dump(confinamento)
    except BaseException as e:
        return str(e)


def getQuantityForMatriz(matrizId):
    try:
        confinamento = db.session.query(Confinamento.Confinamento).filter_by(matrizId=matrizId, active=True).first()
        matrizId = confinamento.matrizId
        planoId = confinamento.planoId
        dataEntrada =  datetime.today().strftime('%d/%m/%y')
        
        day = getDaysInConfinament(matrizId=matrizId)
        
        if day == 0:
            day = 1
            
        dayQuantity = db.session.query(Dia.Dias.quantidade).filter_by(planoId=planoId, dia=day).first()[0]
        totalQuantity = db.session.query(func.sum(Registro.quantidade)).filter_by(matrizId=matrizId, dataEntrada=dataEntrada).first()[0]
        
        if totalQuantity == None:
            totalQuantity = 0
        
        total = dayQuantity - totalQuantity
        
        if total <= 0:
            total = 0
            
        return total
    except BaseException as e:
        return e.args[0]


def canOpenDoor(matrizId):
    try:
        hasConfinamento = db.session.query(Confinamento.query.filter_by(matrizId=matrizId, active=True, deleted=False).exists()).scalar()
        if not hasConfinamento:
            return "Matriz não possui confinameto"
        
        hasInseminacao = db.session.query(Inseminacao.query.filter_by(matrizId=matrizId, active=True, deleted=False).exists()).scalar()
        if not hasInseminacao:
            return "Matriz não possui inseminação"

        confinamento = db.session.query(Confinamento).filter_by(matrizId=matrizId, active=True, deleted=False).first()
        
        hasWarning = db.session.query(Aviso.query.filter_by(confinamentoId=confinamento.id, active=True, deleted=False, type=2).exists()).scalar()
        if not hasWarning:
            return "Matriz não possui aviso de separação"
        
        canOpen = db.session.query(Aviso).filter_by(confinamentoId=confinamento.id, active=True, deleted=False).first()

        return canOpen.separate
    except BaseException as e:
        return e.args[0]


def verifyDaysToOpen():
    try:
        inseminacao = db.session.query(Inseminacao).filter_by(active=True).all()
        
        for item in inseminacao:
            day = getDaysInConfinament(matrizId=item.matrizId)

            # paramters = getParameters
            if day >= 2:
                # Aviso já foi inserido?
                #if avisoInserido:
                return True
            else:
                return False
    except BaseException as e:
        return e.args[0]


def getDaysInConfinament(matrizId):
    confinamento = db.session.query(Confinamento).filter_by(matrizId=matrizId, active=True, deleted=False).first()
    dataAtual = datetime.today()
    days = dataAtual - Confinamento.dataConfinamento
    
    if days == 0:
        days = 1
        
    return days.days
