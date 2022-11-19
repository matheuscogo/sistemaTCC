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
    'data': fields.Nested(list_dias, required=True, description='Lista de dias')
})

headers = namespace.parser()
# Aqui podemos adicionar mais parametros ao headers

@namespace.route('/<int:dia>/<int:planoId>')
@namespace.param('dia')
@namespace.param('planoId')
@namespace.expect(headers)
class GetDia(Resource):
    def get(self, dia, planoId):
        """Consulta um dia por id"""
        try:
            dia = diasCRUD.consultarDia(planoId=planoId, dia=dia)
            
            if not dia['success']:
                raise BaseException(dia['message'])

            return dia
        except BaseException as e:
            response = {
                'success': False,
                'response': {},
                'message': e.args[0]
            }
            
            return response



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



def bind_with_api(api: Api):
    """
    Adiciona o namespace à API recebida
    :param api: Flask Restplus API
    :return: Vazio
    """
    api.add_namespace(namespace)
    return None