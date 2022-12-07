from ext.site.model import Alimentador
from ext.db import session, func
from werkzeug.wrappers import Response
import json


def cadastrarAlimentador(alimentador):  # Create
    try:
        session.add(alimentador)
        session.commit()
        return Response(response=json.dumps("{success: true, message: Alimentador cadastrada com sucesso!, response: null}"), status=200)
    except BaseException as e:
        return Response(response=json.dumps("{success: false, message: " + e.args[0] + ", response: null}"), status=501)


def consultarAlimentadores(hash):  # Read
    try:
        alimentador = session.query(
            func.sum(Alimentador.quantidade).label("quantidadeTotal"), 
            Alimentador.hash, Alimentador.matrizId
        ).filter_by(hash=hash).group_by(Alimentador.hash).first()
        return alimentador
    except BaseException as e:
        return Response(response=json.dumps("{success: false, message: " + e.args[0] + ", response: null}"), status=501)