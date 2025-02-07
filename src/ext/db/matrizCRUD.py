from ..site.model import Matriz
from ..site.model import MatrizSchema
from ..db import db
from werkzeug.wrappers import Response, Request
import json

def cadastrarMatriz(matriz):  # Create
    try:
        if matriz.rfid == None or matriz.rfid == "":
            raise Exception("Rfid não repasado para o controlador")
            
        if matriz.numero == None or matriz.numero == "":
            raise Exception("Número não repasado para o controlador")
            
        if matriz.ciclos == None or matriz.ciclos == "":
            raise Exception("Quantidade de ciclos não repasado para o controlador")
            
        db.session.add(matriz)
        db.session.commit()
        
        response = {
            "success": True,
            "response": {},
            "message": "Matriz cadastrada com sucesso!"
        }
        
        return response
    except Exception as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return response

def consultarMatrizes():  # Read
    try:
        matrizes = db.session.query(Matriz).filter_by(deleted=False).all()
        
        response = {
            "success": True,
            "response": matrizes,
            "message": ""
        }
        
        return response
    except Exception as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return response

def consultarMatriz(id):  # Read
    try:
        matriz = db.session.query(Matriz).filter_by(id=id, deleted=False).first()
        
        response = {
            'success': True,
            'response': matriz,
            'message': ""
        }
            
        return response
    except Exception as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return response


def atualizarMatriz(id, matriz):  # Update
    try:
        hasMatriz = db.session.query(Matriz.Matriz.query.filter_by(id=id, delted=False).exists()).scalar()

        if not hasMatriz:
            raise BaseException("Matriz não encontrada.")
        
        matriz.id = matriz.id
        
        db.session.add(matriz)
        db.session.commit()
        
        response = {
            'success': True,
            'response': {},
            'message': "Matriz atualizada com sucesso!"
        }
            
        return response
    except BaseException as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return  response


def excluirMatriz(id):  # Delete
    try:
        matrizExists = db.session.query(Matriz.query.filter(Matriz.id == id, Matriz.deleted == True).exists()).scalar()
        
        if matrizExists:
            raise BaseException("Não foi possivel deletar matriz, matriz já foi deletada")
        
        matriz = db.session.query(Matriz).filter_by(id=id).first()

        if matriz is None:
            raise BaseException("Não foi possivel deletar matriz, não encontrada")
        
        matriz.deleted = True
        
        db.session.add(matriz)
        db.session.commit()
        
        response = {
            'success': True,
            'response': {},
            'message': "Matriz excluida com sucesso!"
        }
            
        return response
    except BaseException as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return  response
