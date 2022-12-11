from ...db import diasCRUD
from flask_restx import Api, Namespace, Resource, fields

namespace = Namespace(name='Dias', description='Dias', path='/dias')

list_dias = namespace.model('Lista de dias', {
    'id': fields.Integer(required=True, description='ID do dia'),
    'plano': fields.Integer(required=True, description='FK do plano de alimentação'),
    'dia': fields.Integer(required=True, description='Dias em confinamento'),
    'quantidade': fields.Integer(required=True, description='Quantidade de ração para esse dia de confinamento')    
})

list_dias_response = namespace.model('Resposta da lista de dias', {
    'success': fields.Boolean(required=True, description='Condição da requisição'),
    'message': fields.String(required=True, description='Mensagem da requisição'),
    'response': fields.Nested(list_dias, skip_none=True, description='Mensagem da requisição')
})
headers = namespace.parser()
# Aqui podemos adicionar mais parametros ao headers

@namespace.route('/', doc={"description": 'Lista todos os matrizes'})
@namespace.expect(headers)
class ListDias(Resource):
    @namespace.marshal_with(list_dias_response)
    def get(self):
        """Lista todos os dias"""
        try:
            dias = diasCRUD.consultarDias()
            
            if not dias['success']:
                raise BaseException(dias['message'])

            return dias
        except BaseException as e:
            response = {
                'success': False,
                'response': {},
                'message': e.args[0]
            }
            
            return response
        
@namespace.route('/<int:planoId>/<int:dia>', doc={"description": 'Lista todos os matrizes'})
@namespace.expect(headers)
class GetDias(Resource):
    @namespace.marshal_with(list_dias_response)
    def get(self, dia, planoId):
        """Consulta um dias"""
        try:
            dias = diasCRUD.consultarDia(planoId=planoId, dia=dia)
            
            if not dias['success']:
                raise BaseException(dias['message'])

            return dias
        except BaseException as e:
            response = {
                'success': False,
                'response': {},
                'message': e.args[0]
            }
            
            return response


def bind_with_api(api: Api):
    """
    Adiciona o namespace à API recebida
    :param api: Flask Restplus API
    :return: Vazio
    """
    api.add_namespace(namespace)
    return None