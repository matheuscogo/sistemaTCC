from ..site.model import Registro, Matriz
from ..site.model import RegistroSchema
from ..db import db
from werkzeug.wrappers import Response, Request
from datetime import datetime
import json


def consultarRegistros():  # Read
    try:        
        result = db.session.query(
            Registro.id,
            Registro.dataEntrada,
            Registro.dataSaida,
            Registro.quantidade,
            Registro.matrizId,
            Matriz.numero.label('numeroMatriz'),
        ).join(Matriz).filter(
            Matriz.deleted==False,
        ).all()
        
        registros = []

        for registro in result:
            obj = {
                "id": registro.id, 
                "matriz": {
                    'description': registro.numeroMatriz,
                    'value': registro.matrizId
                }, 
                "dataEntrada": registro.dataEntrada,
                "dataSaida": registro.dataSaida,
                "quantidade": registro.quantidade,
                "tempo": ((registro.dataSaida - registro.dataEntrada).seconds) * 1000,
            }
            
            registros.append(obj)
            
        response = {
            'success': True,
            'response': registros,
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


def consultarRegistro(id): # Read
    try:
        registro = db.session.query(Registro).filter_by(id=id).first()
        matriz = db.session.query(Matriz).filter_by(id=registro.matrizId, deleted=False).first()
        
        if not registro:
            raise BaseException("Registro não encontrado.")
        
        response = {
            'success': True,
            'response': {
                "id": registro.id, 
                "matriz": {
                    'description': matriz.numero,
                    'value': registro.matrizId
                }, 
                "dataEntrada": registro.dataEntrada,
                "dataSaida": registro.dataSaida,
                "quantidade": registro.quantidade,
                "tempo": ((registro.dataSaida - registro.dataEntrada).seconds) * 1000,
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
