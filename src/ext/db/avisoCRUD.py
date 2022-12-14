from ..site.model import Aviso, Confinamento
from ..db import db
from werkzeug.wrappers import Response
from xmlrpc.client import ResponseError
import json
from ..site.model import Matriz
from ..db import db

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


def consultarAviso(id):  # Read
    try:
        aviso = db.session.query(Aviso).filter_by(id=id, active=True).first()
        
        msg = ''
        
        # Matriz sem brinco
        if aviso.tipo == 1:
            msg = "Matriz sem brinco"
        
        # Matriz prestes a parir
        if aviso.tipo == 2:
            matriz = db.session.query(
                Matriz
            ).join(Confinamento, Confinamento.matrizId == Matriz.id).filter(
                Confinamento.active==True,
                Matriz.deleted==False,
                Confinamento.deleted==False
            ).first()
            
            msg = "Matriz nº " + str(matriz.numero) + " está prestes a parir."
        
        # Reservatório de comida quase vazio
        if aviso.tipo == 3:
            msg = "Há pouca ração no reservatório."
            
        # Reservatório de comida quase vazio
        if aviso.tipo == 4:
            msg = "Matriz sem confinamento."
        
        obj = {
                'id': aviso.id,
                'aviso': msg,
                'dataAviso': aviso.dataAviso,
                'separate': aviso.separate,
                'tipo': aviso.tipo,
                'active': aviso.active
            }
        

        response = {
            'success': True,
            'response': obj,
            'message': ""
        }
        
        return response
    except BaseException as e:
        return str(e)

def consultarAvisos():  # Read
    try:
        responses = db.session.query(
            Aviso.id, 
            Aviso.tipo, 
            Aviso.dataAviso,
            Aviso.confinamentoId,
            Aviso.separate,
            Aviso.confinamentoId,
            Aviso.active, 
        ).filter(
            Aviso.active==True,
            Aviso.deleted==False
        ).all()
        
        avisos = []
        
        for aviso in responses:
            msg = ''
            
            # Matriz sem brinco
            if aviso.tipo == 1:
                msg = "Matriz sem brinco"
            
            # Matriz prestes a parir
            if aviso.tipo == 2:
                matriz = db.session.query(
                    Matriz
                ).join(Confinamento, Confinamento.id == aviso.confinamentoId).filter(
                    Confinamento.active==True,
                    Matriz.deleted==False,
                    Confinamento.deleted==False
                ).first()
                
                msg = "Matriz nº " + str(matriz.numero) + " está prestes a parir."
            
            # Reservatório de comida quase vazio
            if aviso.tipo == 3:
                msg = "Há pouca ração no reservatório."
                
            # Reservatório de comida quase vazio
            if aviso.tipo == 4:
                msg = "Matriz sem confinamento."
        
            obj = {
                'id': aviso.id,
                'aviso': msg,
                'dataAviso': aviso.dataAviso,
                'separate': aviso.separate,
                'tipo': aviso.tipo,
                'active': aviso.active
            }
        
            avisos.append(obj)

        response = {
            'success': True,
            'response': avisos,
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

def separarMatriz(id, separar):
    try:
        aviso = db.session.query(Aviso).filter_by(id=id).first()

        aviso.separate = separar
        
        db.session.commit()
        
        response = {
            'success': True,
            'response': {},
            'message': "Aviso atualizado com sucesso!"
        }
        
        return response
    except BaseException as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return  response

def excluirAviso(id):  # Delete
    try:
        aviso = db.session.query(Aviso).filter_by(id=id).first()
        
        aviso.deleted = True
        
        db.session.commit()
        
        response = {
            'success': True,
            'response': {},
            'message': "Aviso excluido com sucesso!"
        }
        
        return response
    except BaseException as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return  response
