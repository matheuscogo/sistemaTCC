from ..site.model import Matriz
from ..site.model import MatrizSchema
from . import db
from werkzeug.wrappers import Response, Request
import json

def cadastrarParametro(matriz):  # Create
    try:
        if matriz.rfid == None:
            raise Exception("Rfid não repasado para o controlador")
            
        if matriz.numero == None:
            raise Exception("Número não repasado para o controlador")
            
        if matriz.ciclos == None:
            raise Exception("Quantidade de ciclos não repasado para o controlador")
            
        db.session.add(matriz)
        db.session.commit()
        
        return Response(response=json.dumps("{success: true, message: Parametro cadastrada com sucesso!, response: null}"), status=200)
    except BaseException as e:
        return Response(response=json.dumps("{success: false, message: "+ e.args[0] +", response: null}"), status=501)

def consultarParametroes():  # Read
    try:
        matrizes = db.session.query(Parametro).all()
        return matrizes
    except BaseException as e:
        return Response(response=json.dumps("{success: false, message: "+ e.args[0] +", response: null}"), status=501)


def consultarParametro(id):  # Read
    try:
        matriz = db.session.query(Parametro.Parametro).filter_by(id=id).first()
        if not matriz:
            raise Exception(ParametroSchema().dump(matriz))
        return ParametroSchema().dump(matriz)
    except Exception as e:
        return e.args[0]
    
def getParametroByRfid(rfid):  # Read
    try:
        matriz = db.session.query(Parametro.Parametro).filter_by(rfid=rfid).first()
        if not matriz:
            raise Exception(ParametroSchema().dump(matriz))
        return ParametroSchema().dump(matriz)
    except Exception as e:
        return e.args[0]

    
def atualizarParametro(args):  # Update
    try:
        id=int(args['id'])
        rfid=str(args['rfid'])
        numero=int(args['numero'])
        ciclos=int(args['ciclos'])
        matriz = db.session.query(Parametro).filter_by(id=id).first()
        matriz.rfid = rfid
        matriz.numero = numero
        matriz.ciclos = ciclos
        db.session.commit()
        return Response(response=json.dumps("{success: true, message: Parametro atualizada com sucesso!, response: null}"), status=200)
    except BaseException as e:
        return Response(response=json.dumps("{success: false, message: " + e.args[0] + ", response: null}"), status=501)


def excluirParametro(id):  # Delete
    try:
        matriz = db.session.query(Parametro).filter_by(id=id).first()
        db.session.delete(matriz)
        db.session.commit()
        return Response(response=json.dumps("{success: true, message: Matriz excluida com sucesso!, response: null}"), status=200)
    except BaseException as e:
        return Response(response=json.dumps("{success: false, message: "+ e.args[0] +", response: null}"), status=501)
    
def consultarMatrizRFID(rfid):  # Read
    try:
        matriz = db.session.query(Matriz.Matriz).filter_by(rfid=rfid).first()
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