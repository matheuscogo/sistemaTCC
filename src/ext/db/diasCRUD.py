from sqlalchemy.sql.elements import Null
from ..site.model import Dia
from ..site.model import DiaSchema
from ..site.model import Dia
from ..db import db
from werkzeug.wrappers import Response, Request
import json

def cadastrarDia(args):  # Create
    try:
        plano = int(args['plano'])
        dia = int(args['dia'])
        quantidade = int(args['quantidade'])
        db.session.add(Dia.Dias(plano=plano,dia=dia,quantidade=quantidade))
        db.session.commit()
        return Response(response=json.dumps("{success: true, message: Dia cadastrado com sucesso!, response: null}"), status=200)
    except BaseException as e:
        return Response(response=json.dumps("{success: false, message: "+ e.args[0] +", response: null}"), status=501)

def consultarDias():  # Read
    try:
        dias = db.session.query(Dia.Dias).all()
        return dias
    except BaseException as e:
        return Response(response=json.dumps("{success: false, message: "+ e.args[0] +", response: null}"), status=501)


def consultarDia(planoId, dia):  # Read
    try:
        dia = db.session.query(Dia.Dias).filter_by(dia=dia, planoId=planoId).first()
        if not dia:
            raise Exception("")
        return DiaSchema().dump(dia)
    except Exception as e:
        return Response(response=json.dumps("{success: false, message: " + e.args[0] + ", response: null}"), status=501)

    
def atualizarDia(args):  # Update
    try:
        id=int(args['id'])
        plano=str(args['plano'])
        dia=int(args['dias'])
        quantidade=int(args['quantidade'])
        dia = db.session.query(Dia.Dias).filter_by(id=id).first()
        dia.plano = plano
        dia.quantidade = quantidade
        db.session.commit()
        return Response(response=json.dumps("{success: true, message: Dia atualizado com sucesso!, response: null}"), status=200)
    except BaseException as e:
        return Response(response=json.dumps("{success: false, message: " + e.args[0] + ", response: null}"), status=501)


def excluirDia(id):  # Delete
    try:
        dia = db.session.query(Dia.Dias).filter_by(id=id).first()
        db.session.delete(dia)
        db.session.commit()
        return Response(response=json.dumps("{success: true, message: Dia excluida com sucesso!, response: null}"), status=200)
    except BaseException as e:
        return Response(response=json.dumps("{success: false, message: "+ e.args[0] +", response: null}"), status=501)