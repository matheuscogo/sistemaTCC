from ext.site.model import Registro, RegistroSchema
from ...db import registroCRUD
from flask_restx import Api, Namespace, Resource, fields, reqparse
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import InternalServerError
import json

namespace = Namespace(name='Registros', description='Registros', path='/registros')

insert_registro = namespace.model('Dados para criação de um registro', {
    'matrizId': fields.Integer(required=True, description='FK da matriz'),
    'dataEntrada': fields.String(required=True, description='Dia da entrada da matriz no alimentador'),
    'dataSaida': fields.String(required=True, description='Dia da saida da matriz no alimentador'),
    'horaEntrada': fields.String(required=True, description='Hora de entrada da matriz no alimentador'),
    'horaSaida': fields.String(required=True, description='Hora de saida da matriz no alimentador'),
    'tempo': fields.String(required=True, description='Tempo que a matriz permaneceu no confinamento'),
    'quantidade': fields.Integer(required=True, description='Quantidade de ração consumida pela matriz')
})

update_registro = namespace.model('Dados para atualização de um registro', {
    'id': fields.Integer(required=True, description='ID do registro'),
    'matrizId': fields.Integer(required=True, description='FK da matriz'),
    'dataEntrada': fields.String(required=True, description='Dia da entrada da matriz no alimentador'),
    'dataSaida': fields.String(required=True, description='Dia da saida da matriz no alimentador'),
    'horaEntrada': fields.String(required=True, description='Hora de entrada da matriz no alimentador'),
    'horaSaida': fields.String(required=True, description='Hora de saida da matriz no alimentador'),
    'tempo': fields.String(required=True, description='Tempo que a matriz permaneceu no confinamento'),
    'quantidade': fields.Integer(required=True, description='Quantidade de ração consumida pela matriz')
})

list_registros = namespace.model('Lista de registros', {
    'id': fields.Integer(required=True, description='ID do registro'),
    'matriz': fields.Nested(namespace.model('', {'description': fields.String, 'value': fields.String}), required=True, description='FK da matriz'),
    'dataEntrada': fields.DateTime(required=True, description='Dia da entrada da matriz no alimentador'),
    'dataSaida': fields.DateTime(required=True, description='Dia da saida da matriz no alimentador'),
    'tempo': fields.Integer(required=True, description='Tempo que a matriz permaneceu no confinamento'),
    'quantidade': fields.Integer(required=True, description='Quantidade de ração consumida pela matriz')
})

list_registros_response = namespace.model('Resposta da lista de registros', {
    'success': fields.Boolean(required=True, description='Condição da requisição'),
    'message': fields.String(required=True, description='Mensagem da requisição'),
    'response': fields.Nested(list_registros, required=True, description='Mensagem da requisição')
})

headers = namespace.parser()
# Aqui podemos adicionar mais parametros ao headers

@namespace.route('/<int:id>')
@namespace.param('id')
@namespace.expect(headers)
class GetRegistro(Resource):
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