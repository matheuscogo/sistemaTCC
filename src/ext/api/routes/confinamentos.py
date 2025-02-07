from datetime import datetime
from ext.db import confinamentoCRUD
from flask_restx import Api, Namespace, Resource, fields, reqparse
from ext.site.model import Confinamento

namespace = Namespace('Confinamentos', description='Confinamentos', path='/confinamentos')

insert_confinamento = namespace.model('Dados para criação de Matrizes', {
    'dataConfinamento': fields.DateTime(required=True, description='Data de entrada no confinamento'),
    'matrizId': fields.Integer(required=True, description='FK da matriz'),
    'planoId': fields.Integer(required=True, description='FK do plano de alimentação')
})

update_confinamento = namespace.model('Dados para atualizar o confinamento', {
    'dataConfinamento': fields.String(required=True, description='Data de /entrada no confinamento'),
    'planoId': fields.Integer(required=True, description='FK do plano de alimentação'),
    'active': fields.Boolean(required=True, description='Flag que valida se o confinamento está ativo')
})

list_confinamento = namespace.model('Lista de confinamentos', {
    'id': fields.Integer(required=True, description='ID da inseminação'),
    'dataConfinamento': fields.String(required=True, description='Data de /entrada no confinamento'),
    'matriz': fields.Nested(namespace.model('', {'description': fields.String, 'value': fields.String}), skip_none=True, description='FK da matriz'),
    'plano': fields.Nested(namespace.model('', {'description': fields.String, 'value': fields.String}), skip_none=True, description='FK do plano de alimentação'),
    'active': fields.Boolean(required=True, description='Flag que valida se o confinamento está ativo')
})

list_confinamento_response = namespace.model('Resposta da lista de confinamentos', {
    'success': fields.Boolean(required=True, description='Condição da requisição'),
    'message': fields.String(required=True, description='Mensagem da requisição'),
    'response': fields.Nested(list_confinamento, skip_none=True, description='Mensagem da requisição')
})

headers = namespace.parser()

@namespace.route('/insert')
@namespace.expect(headers)
class CreateConfinamento(Resource):
    @namespace.expect(insert_confinamento, validate=True)
    def post(self):
        """Cadastra um confinamento"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(
                'dataConfinamento', 
                type=lambda s: datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%fZ')
            )
            parser.add_argument('matrizId', type=int)
            parser.add_argument('planoId', type=int)
            
            args = parser.parse_args()
            
            confinamento = Confinamento(
                planoId = args['planoId'],
                matrizId = args['matrizId'],
                dataConfinamento = args['dataConfinamento'],
                active = True,
                deleted = False,
            )

            confinamento = confinamentoCRUD.cadastrarConfinamento(confinamento)

            if not confinamento['success']:
                raise BaseException(confinamento['message'])
            
            return confinamento
        except BaseException as e:
            response = {
                'success': False,
                'response': {},
                'message': e.args[0]
            }
        
            return response

@namespace.route('/update/<int:id>')
@namespace.expect(headers)
class UpdateConfinamento(Resource):
    @namespace.expect(update_confinamento, validate=True)
    def put(id, self):
        """Atualiza um confinamento"""
        try:
            parser = reqparse.RequestParser()
            
            parser.add_argument('dataConfinamento', type=str)
            parser.add_argument('planoId', type=int)
            parser.add_argument('active', type=bool)
            
            args = parser.parse_args()
            
            confinamento = Confinamento(
                dataConfinamento=args['dataConfinamento'],
                planoId=args['planoId'],
                active=args['active'],
            )
            
            confinamento = confinamentoCRUD.atualizarConfinamento(id, confinamento)
            
            if not confinamento['success']:
                raise BaseException(confinamento['message'])
            
            return confinamento
        except BaseException as e:
            response = {
                'success': False,
                'response': {},
                'message': e.args[0]
            }
        
            return response

@namespace.route('/<int:id>')
@namespace.param('id')
@namespace.expect(headers)
class GetConfinamento(Resource):
    @namespace.marshal_with(list_confinamento_response)
    def get(self, id):
        """Consulta um confinamento por id"""
        try:
            confinamento = confinamentoCRUD.consultarConfinamento(id)
            
            if not confinamento['success']:
                raise BaseException(confinamento['message'])
            
            return confinamento
        except BaseException as e:
            response = {
                'success': False,
                'response': {},
                'message': e.args[0]
            }
        
            return response


@namespace.route('/')
@namespace.expect(headers)
class ListConfinamento(Resource):
    @namespace.marshal_with(list_confinamento_response)
    def get(self):
        """Lista todos os confinamentos"""
        try:
            confinamentos = confinamentoCRUD.consultarConfinamentos()
            
            if not confinamentos['success']:
                raise BaseException(confinamentos['message'])
            
            return confinamentos
        except BaseException as e:
            response = {
                'success': False,
                'response': {},
                'message': e.args[0]
            }
        
            return response


@namespace.route('/delete/<int:id>')
@namespace.param('id', 'ID do confinamento')
@namespace.expect(headers)
class DeleteConfinamento(Resource):
    def delete(self, id):
        """Remove um confinamento"""
        try:
            confinamento = confinamentoCRUD.excluirConfinamento(id)
            
            if not confinamento['success']:
                raise BaseException(confinamento['message'])
            
            return confinamento
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
