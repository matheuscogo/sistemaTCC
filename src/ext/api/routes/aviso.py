from datetime import datetime
from ext.db import avisoCRUD
from ...db import db
from flask_restx import Api, Namespace, Resource, fields, reqparse
from ext.site.model import Aviso
from ext.site.model import AvisoSchema
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import InternalServerError

namespace = Namespace('Avisos', description='Avisos', path='/avisos')

update_aviso = namespace.model('Dados para atualizar o aviso', {
    'id': fields.Integer(required=True, description='ID do aviso'),
    'separate': fields.Boolean(required=True, description='Valor da flag')
})

list_avisos = namespace.model('Lista de avisos', {
    'id': fields.Integer(required=True, description='ID do aviso'),
    'matriz': fields.Nested(namespace.model('', {'description': fields.String, 'value': fields.String}), skip_none=True, description='FK da matriz'),
    'dataAviso': fields.DateTime(required=True, description='Data da criação do registro do aviso'),
    'separate': fields.Boolean(required=True, description='Flag para separação'),
    'active': fields.Boolean(required=True, description='FK do plano de alimentação')
})

list_avisos_response = namespace.model('Resposta para lista de avisos', {
    'success': fields.Boolean(required=True, description='Condição da requisição'),
    'message': fields.String(required=True, description='Mensagem da requisição'),
    'response': fields.Nested(list_avisos, skip_none=True, description='Mensagem da requisição')
})


headers = namespace.parser()

@namespace.route('/separarMatriz', methods=['PUT'])
@namespace.expect(headers)
class UpdateRegistro(Resource):
    @namespace.expect(update_aviso, validate=True)
    def put(self):
        """Autorização de separação de uma matriz"""
        try:
            parser = reqparse.RequestParser()
            
            parser.add_argument('id', type=int)
            parser.add_argument('separate', type=bool)

            args = parser.parse_args()
            aviso = avisoCRUD.separarMatriz(args)
            
            if not aviso:
                raise Exception("Error")
            
            return aviso
        except Exception as e:
            raise InternalServerError(e.args[0])


@namespace.route('/')
@namespace.expect(headers)
class ListAvisos(Resource):
    @namespace.marshal_with(list_avisos_response)
    def get(self):
        """Lista todos os avisos pendentes"""
        try:
            avisos = avisoCRUD.consultarAvisos()
            
            if not avisos['success']:
                raise BaseException(avisos['message'])
            
            return avisos
        except BaseException as e:
            response = {
                'success': False,
                'response': {},
                'message': e.args[0]
            }
        
            return response


def bind_with_api(api: Api):
    api.add_namespace(namespace)
    return None
