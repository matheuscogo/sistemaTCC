from sqlalchemy.sql.elements import Null
from ..site.model import Dia
from ..site.model import DiaSchema
from ..site.model import Dia
from ..db import db
from werkzeug.wrappers import Response, Request
import json

def cadastrarDia(dia):  # Create
    try:
        db.session.add(Dia.Dias(plano=dia.planoId,dia=dia,quantidade=dia.quantidade))
        db.session.commit()
        
        response = {
            'success': True,
            'response': {},
            'message': "Dia cadastrado com sucesso!"
        }
            
        return response
    except BaseException as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
            
        return response

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
