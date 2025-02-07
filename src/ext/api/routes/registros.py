from ...db import registroCRUD
from flask_restx import Api, Namespace, Resource, fields

namespace = Namespace(name='Registros', description='Registros', path='/registros')

list_registros = namespace.model('Lista de registros', {
    'id': fields.Integer(required=True, description='ID do registro'),
    'matriz': fields.Nested(namespace.model('', {'description': fields.String, 'value': fields.String}), skip_none=True, description='FK da matriz'),
    'dataEntrada': fields.DateTime(required=True, description='Dia da entrada da matriz no alimentador'),
    'dataSaida': fields.DateTime(required=True, description='Dia da saida da matriz no alimentador'),
    'tempo': fields.Integer(required=True, description='Tempo que a matriz permaneceu no confinamento'),
    'quantidade': fields.Integer(required=True, description='Quantidade de ração consumida pela matriz')
})

list_registros_response = namespace.model('Resposta da lista de registros', {
    'success': fields.Boolean(required=True, description='Condição da requisição'),
    'message': fields.String(required=True, description='Mensagem da requisição'),
    'response': fields.Nested(list_registros, skip_none=True, description='Mensagem da requisição')
})

headers = namespace.parser()
# Aqui podemos adicionar mais parametros ao headers

@namespace.route('/<int:id>')
@namespace.param('id')
@namespace.expect(headers)
class GetRegistro(Resource):
    @namespace.marshal_with(list_registros_response)
    def get(self, id):
        """Consulta um registro por id"""
        try:
            registro = registroCRUD.consultarRegistro(id)
            
            if not registro['success']:
                raise BaseException(registro['message'])
            
            return registro
        except BaseException as e:
            response = {
                'success': False,
                'response': {},
                'message': e.args[0]
            }
        
            return response


@namespace.route('/', doc={"description": 'Lista todos os matrizes'})
@namespace.expect(headers)
class ListRegistros(Resource):
    @namespace.marshal_with(list_registros_response)
    def get(self):
        """Lista todos os registros"""
        try:
            registros = registroCRUD.consultarRegistros()
            
            if not registros['success']:
                raise BaseException(registros['message'])

            return registros
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