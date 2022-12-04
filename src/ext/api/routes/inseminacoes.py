from datetime import datetime
from ext.site.model import Inseminacao, InseminacaoSchema
from ...db import db, inseminacaoCRUD
from flask_restx import Api, Namespace, Resource, fields, reqparse
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import InternalServerError

namespace = Namespace(name='Inseminação', description='Inseminação', path='/inseminacoes')

insert_inseminacao = namespace.model('Dados para criação de uma inseminação', {
    'matrizId': fields.Integer(required=True, description='ID da inseminação'),
    'planoId': fields.Integer(required=True, description='Plano para inseminação'),
    'dataInseminacao': fields.DateTime(required=True, description='Data da inseminação'),
    'isNewCiclo': fields.Boolean(required=True, description='isNewCiclo')
})

update_inseminacao = namespace.model('Dados para atualização de inseminações', {
    'id': fields.Integer(required=True, description='ID da inseminação'),
    'matrizId': fields.Integer(required=True, description='ID da inseminação'),
    'planoId': fields.Integer(required=True, description='Plano para inseminação'),
    'dataInseminacao': fields.DateTime(required=True, description='Data da inseminação'),
    'active': fields.Boolean(required=True, description='Verifica se a inseminação está ativo ou não'),
    'deleted': fields.Boolean(required=True, description='Flag que verifica se inseminação está deleteada')
})

list_inseminacoes = namespace.model('Lista de inseminacaoes', {
    'id': fields.String(required=True, description='Identificadores das inseminacaoes'),
    'dataInseminacao': fields.DateTime(required=True, description='Data da inseminação'),
    'confinamento': fields.Nested(namespace.model('', {'description': fields.String, 'value': fields.String}), skip_none=True, description='Confinamento'),
    'matriz': fields.Nested(namespace.model('', {'description': fields.String, 'value': fields.String}), skip_none=True, description='Matriz'),
    'plano': fields.Nested(namespace.model('', {'description': fields.String, 'value': fields.String}), skip_none=True, description='Plano'),
    'active': fields.Boolean(required=True, description='Verifica se a inseminação está ativo ou não'),
    'deleted': fields.Boolean(required=True, description='Flag que verifica se inseminação está deleteada')
})

list_inseminacoes_response = namespace.model('Resposta da lista de matrizes', {
    'success': fields.Boolean(required=True, description='Condição da requisição'),
    'message': fields.String(required=True, description='Mensagem da requisição'),
    'response': fields.Nested(list_inseminacoes, skip_none=True, description='Mensagem da requisição')
})


delete_episode_response = namespace.model('Resposta da remocao de inseminacaoes', {
    'removed': fields.Boolean(required=True, description='Indicador de remocao com sucesso')
})

headers = namespace.parser()
# Aqui podemos adicionar mais parametros ao headers

@namespace.route('/insert', methods=['POST'])
@namespace.expect(headers)
class CreateInseminacao(Resource):
    @namespace.expect(insert_inseminacao, validate=True)
    @namespace.doc(security='apikey')
    def post(self):
        """Cadastra uma inseminação"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('matrizId', type=int)
            parser.add_argument('planoId', type=int)
            parser.add_argument('dataInseminacao', type=lambda s: datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%fZ'))
            parser.add_argument('isNewCiclo', type=bool)
            args = parser.parse_args()
            
            inseminacao = Inseminacao(
                planoId = args['planoId'],
                matrizId = args['matrizId'],
                dataInseminacao = args['dataInseminacao'],
                active=True,
                deleted=False,
            )
            
            inseminacao = inseminacaoCRUD.cadastrarInseminacao(inseminacao, args['isNewCiclo'])
            
            if not inseminacao['success']:
                raise BaseException(inseminacao['message'])

            return inseminacao
        except BaseException as e:
            response = {
                'success': False,
                'response': {},
                'message': e.args[0]
            }
            
            return response


@namespace.route('/update/', methods=["PUT"])
@namespace.expect(headers)
class UpdateInseminacao(Resource):
    @namespace.expect(update_inseminacao, validate=True)
    def put(self):
        """Atualiza uma inseminação"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=int)
            parser.add_argument('matrizId', type=int)
            parser.add_argument('dataInseminacao', type=str)
            args = parser.parse_args()
            
            inseminacao = inseminacaoCRUD.atualizarInseminacao(args)
            
            if not inseminacao['success']:
                raise BaseException(inseminacao['message'])

            return inseminacao
        except BaseException as e:
            response = {
                'success': False,
                'response': {},
                'message': e.args[0]
            }
            
            return response

@namespace.route('/<int:id>', methods=["GET"])
@namespace.param('id')
@namespace.expect(headers)
class GetInseminacao(Resource):
    @namespace.marshal_with(list_inseminacoes_response)
    def get(self, id):
        """Consulta uma inseminação por id"""
        try:
            inseminacao = inseminacaoCRUD.consultarInseminacao(id)
            
            if not inseminacao['success']:
                raise BaseException(inseminacao['message'])

            return inseminacao
        except BaseException as e:
            response = {
                'success': False,
                'response': {},
                'message': e.args[0]
            }
            
            return response


@namespace.route('/', doc={"description": 'Lista todos os inseminações'}, methods=["GET"])
@namespace.expect(headers)
class ListaInseminacoes(Resource):
    @namespace.marshal_with(list_inseminacoes_response)
    def get(self):
        """Lista todos os inseminações"""
        try:
            inseminacaoes = inseminacaoCRUD.consultarInseminacoes()
            
            if not inseminacaoes['success']:
                raise BaseException(inseminacaoes['message'])

            return inseminacaoes
        except BaseException as e:
            response = {
                'success': False,
                'response': {},
                'message': e.args[0]
            }
            
            return response


@namespace.route('/delete/<int:id>',
                 doc={"description": 'Apaga inseminacaoes'},
                 methods=['DELETE'])
@namespace.param('id', 'ID da inseminacao')
@namespace.expect(headers)
class DeleteInseminacao(Resource):
    def delete(self, id):
        """Remove inseminação"""
        try:
            inseminacao = inseminacaoCRUD.excluirInseminacao(id)
            
            if not inseminacao['success']:
                raise BaseException(inseminacao['message'])

            return inseminacao
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