from ..site.model.Parametro import Parametro
from ..db import db


def consultarParametros():  # Read
    try:
        parametro = db.session.query(Parametro).first()
        
        response = {
            "success": True,
            "response": {
                'id': parametro.id,
                'tempoPorcao': parametro.tempoPorcao,
                'quantidadePorcao': parametro.quantidadePorcao,
                'intervaloPorcoes': parametro.intervaloPorcoes,
                'tempoProximaMatriz': parametro.tempoProximaMatriz,
            },
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

def atualizarParamtro(id, parametro):  # Update
    try:
        param = db.session.query(Parametro).filter_by(id=id).first()

        param.tempoPorcao = parametro.tempoPorcao
        param.quantidadePorcao = parametro.quantidadePorcao
        param.intervaloPorcoes = parametro.intervaloPorcoes
        param.tempoProximaMatriz = parametro.tempoProximaMatriz
 
        db.session.commit()
        
        response = {
            'success': True,
            'response': {},
            'message': "Parametro atualizada com sucesso!"
        }
            
        return response
    except BaseException as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return  response
