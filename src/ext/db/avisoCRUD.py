from genericpath import exists
from queue import Empty

from responses import activate, delete

from ext.site.model import Inseminacao
from ..site.model import Aviso
from ..site.model import Registro
from ..site.model import Confinamento, ConfinamentoSchema
from ..db import db
import datetime
from werkzeug.wrappers import Response, Request
from xmlrpc.client import ResponseError
import json
from ..site.model import Dia
from ..site.model import Plano
from ..site.model import Matriz
from ..site.model import Registro
from ..db import db
from sqlalchemy.sql import func
from datetime import datetime, timedelta

def cadastrarAviso(aviso):  # Create
    try:

        if not aviso.confinamentoId:
            raise Exception(ResponseError)
            
        if not aviso.dataAviso:
            raise Exception(ResponseError)

        db.session.add(aviso)
        db.session.commit()
        
        return Response(response=json.dumps("{success: true, message: Aviso cadastrado com sucesso!, response: null}"), status=200)
    except BaseException as e:
        return Response(response=json.dumps("{success: false, message: " + e.args[0] + ", response: null}"))


def consultarConfinamento(id):  # Read
    try:
        confinamento = db.session.query(Confinamento).filter_by(id=id, active=True).first()
        return ConfinamentoSchema().dump(confinamento)
    except BaseException as e:
        return str(e)

def consultarAvisos():  # Read
    try:
        responses = db.session.query(
            Aviso.id, 
            Aviso.type, 
            Aviso.dataAviso, 
            Aviso.separate, 
            Aviso.active, 
            Matriz.numero.label('matrizNumero')
        ).join(
            Confinamento, Confinamento.id == Aviso.confinamentoId
        ).join(
            Matriz, Matriz.id == Confinamento.matrizId
        ).filter(
            Aviso.active==True,
            Aviso.deleted==False
        ).all()
        
        avisos = []
        
        for aviso in responses:
            msg = ''
            
            # Matriz sem brinco
            if aviso.type is 1:
                msg = "Matriz sem brinco"
            
            # Matriz prestes a parir
            if aviso.type is 2:
                msg = "Matriz nº " + str(aviso.matrizNumero) + " está prestes a parir"
            
            # Reservatório de comida quase vazio
            if aviso.type is 3:
                msg = "Há pouca ração no reservatório"
        
            obj = {
                'id': aviso.id,
                'aviso': {
                    'label': msg,
                    'value': aviso.type
                },
                'dataAviso': aviso.dataAviso,
                'separate': aviso.separate,
                'active': aviso.active
            }
        
            avisos.append(obj)

        return avisos
    except BaseException as e:
        return str(e)

def separarMatriz(args):
    try:
        id = args['id']    
        separar = args['separar']

        aviso = db.session.query(Aviso.Aviso).filter_by(id=id).first()

        aviso.separar = separar
        
        db.session.commit()
        return Response(response=json.dumps("{success: true, message: Aviso atualizado com sucesso!, response: null}"), status=200)
    except BaseException as e:
        return Response(response=json.dumps("{success: false, message: " + e.args[0] + ", response: null}"), status=501)

def excluirConfinamento(id):  # Delete
    try:
        confinameto = db.session.query(Confinamento).filter_by(id=id).first()
        db.session.delete(confinameto)
        db.session.commit()
        return Response(response=json.dumps("{success: true, message: Confinameto excluido com sucesso!, response: null}"), status=200)
    except BaseException as e:
        return Response(response=json.dumps("{success: false, message: "+ e.args[0] +", response: null}"), status=501)


def getConfinamentoByMatriz(matrizId):
    try:
        confinamento = db.session.query(Confinamento.Confinamento).filter_by(matrizId=matrizId, active=True).first()
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

        hasInseminacao = db.session.query(Inseminacao.Inseminacao.query.filter_by(matrizId=matrizId, active=True).exists()).scalar()
        
        if not hasInseminacao:
            return "Matriz não possui inseminação valida"

        day = getDaysInConfinament(matrizId=matrizId)

        # paramters = getParameters
        if day >= 110:
            # Aviso já foi inserido?
            #if avisoInserido:
            return True
        else:
            return False
    except BaseException as e:
        return e.args[0]


def verifyDaysToOpen():
    try:
        inseminacao = db.session.query(Inseminacao.Inseminacao).filter_by(active=True).all()
        
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
    confinamento = db.session.query(Confinamento.Confinamento).filter_by(matrizId=matrizId, active=True).first()
    dataEntrada = datetime.strptime(confinamento.dataConfinamento, '%d/%m/%y')
    dataAtual = datetime.today()
    days = dataAtual - dataEntrada
    print("DIA ENTRADA = " + str(dataEntrada))
    print("DIA ATUAL = " + str(dataAtual))
    return days.days
