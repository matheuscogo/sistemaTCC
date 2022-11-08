from ..site.model import Matriz
from ..site.model import MatrizSchema
from ..db import db
from werkzeug.wrappers import Response, Request
import json

def cadastrarMatriz(matriz):  # Create
    try:
        if matriz.rfid == None:
            raise Exception("Rfid não repasado para o controlador")
            
        if matriz.numero == None:
            raise Exception("Número não repasado para o controlador")
            
        if matriz.ciclos == None:
            raise Exception("Quantidade de ciclos não repasado para o controlador")
            
        db.session.add(matriz)
        db.session.commit()
        
        return Response(response=json.dumps("{success: true, message: Matriz cadastrada com sucesso!, response: null}"), status=200)
    except BaseException as e:
        return Response(response=json.dumps("{success: false, message: "+ e.args[0] +", response: null}"), status=501)

def consultarMatrizes():  # Read
    try:
        matrizes = db.session.query(Matriz).filter_by(deleted=False).all()
        return matrizes
    except BaseException as e:
        return Response(response=json.dumps("{success: false, message: "+ e.args[0] +", response: null}"), status=501)


def consultarMatriz(id):  # Read
    try:
        matriz = db.session.query(Matriz).filter_by(id=id, deleted=False).first()
        return MatrizSchema().dump(matriz)
    except Exception as e:
        return e.args[0]
    
def getMatriz(id):  # Read
    try:
        matriz = db.session.query(Matriz).filter_by(id=id, deleted=False).first()
        if not matriz:
            raise Exception(MatrizSchema().dump(matriz))
        return MatrizSchema().dump(matriz)
    except Exception as e:
        return e.args[0]
    
def getMatrizByRfid(rfid):  # Read
    try:
        matriz = db.session.query(Matriz).filter_by(rfid=rfid, deleted=False).first()
        return MatrizSchema().dump(matriz)
    except Exception as e:
        return e.args[0]
    
    
def atualizarMatriz(id, args):  # Update
    try:
        rfid=str(args['rfid'])
        numero=str(args['numero'])
        ciclos=int(args['ciclos'])
        deleted=bool(args['deleted'])
        
        matriz = db.session.query(Matriz).filter_by(id=id, deleted=False).first()
        
        if not matriz:
            raise Exception(MatrizSchema().dump(matriz))
        
        matriz.rfid = rfid
        matriz.numero = numero
        matriz.ciclos = ciclos
        matriz.deleted = deleted
        
        db.session.add(matriz)
        db.session.commit()
        
        return Response(response=json.dumps("{success: true, message: Matriz atualizada com sucesso!, response: null}"), status=200)
    except BaseException as e:
        return Response(response=json.dumps("{success: false, message: " + e.args[0] + ", response: null}"), status=501)


def excluirMatriz(id):  # Delete
    try:
        matriz = db.session.query(Matriz).filter_by(id=id).first()
        
        matriz.deleted = True
        
        db.session.add(matriz)
        db.session.commit()
        
        return Response(response=json.dumps("{success: true, message: Matriz excluida com sucesso!, response: null}"), status=200)
    except BaseException as e:
        return Response(response=json.dumps("{success: false, message: "+ e.args[0] +", response: null}"), status=501)
    
def consultarMatrizRFID(rfid):  # Read
    try:
        matriz = db.session.query(Matriz.Matriz).filter_by(rfid=rfid, deleted=False).first()
        return matriz
    except Exception as e:
        return e.args[0]
    
def existsRFID(rfid):
    exists = db.session.query(db.exists().where(Matriz.Matriz.rfid == rfid)).scalar()
    if exists:
        return False
    else:
        return True
    
def existsNumero(numero):
    exists = db.session.query(db.exists().where(Matriz.Matriz.numero == numero)).scalar()
    print(str(exists))
    if exists:
        return False
    else:
        return True
    
def consultarMatrizRFID(rfid):  # Read
    try:
        matriz = db.session.query(Matriz.Matriz.id).filter_by(rfid=rfid).first()
        a = str(matriz).replace(", )", "")
        id = str(a).replace("(", "")
        return matriz[0]
    except:
        return False