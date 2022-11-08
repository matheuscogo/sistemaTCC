from ...site.model import PlanoSchema
from ...site.model import Plano
from ...db import db, planosCRUD
from flask_restx import Api, Namespace, Resource, fields, reqparse
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import InternalServerError
import json

namespace = Namespace(name='Planos de alimentação', description='Planos', path='/planos')

insert_plano = namespace.model('Dados para criação de um plano', {
    'nome': fields.String(required=True, description='Nome do plano de alimentação'),
    'descricao': fields.String(required=True, description='Descrição do plano de alimentação'),
    'tipo': fields.Integer(required=True, description='Tipo do plano de alimentação'),
    'quantidadeDias': fields.Integer(required=True, description='Quantidade de dias do plano de alimentação'),
})

update_plano = namespace.model('Dados para atualização de um plano', {
    'nome': fields.String(required=True, description='Nome do plano de alimentação'),
    'descricao': fields.String(required=True, description='Descrição do plano de alimentação'),
    'tipo': fields.Integer(required=True, description='Tipo do plano de alimentação'),
    'quantidadeDias': fields.Integer(required=True, description='Quantidade de dias do plano de alimentação'),
    'active': fields.Boolean(required=True, description='Verifica se o plano de alimentação está ativo ou não'),
    'deleted': fields.Boolean(required=True, description='Verifica se o plano de alimentação está deletado ou não')   
})

get_plano_response = namespace.model('Response para plano de alimentação', {
    'nome': fields.String(required=True, description='Nome do plano de alimentação'),
    'descricao': fields.String(required=True, description='Descrição do plano de alimentação'),
    'tipo': fields.Integer(required=True, description='Tipo do plano de alimentação'),
    'quantidadeDias': fields.Integer(required=True, description='Quantidade de dias do plano de alimentação'),
    'active': fields.Boolean(required=True, description='Verifica se o plano de alimentação está ativo ou não')
})

list_planos = namespace.model('Lista de planos de alimentação', {
    'id': fields.Integer(required=True, description='ID do plano de alimentação'),
    'nome': fields.String(required=True, description='Nome do plano de alimentação'),
    'descricao': fields.String(required=True, description='Descrição do plano de alimentação'),
    'tipo': fields.Integer(required=True, description='Tipo do plano de alimentação'),
    'quantidadeDias': fields.Integer(required=True, description='Quantidade de dias do plano de alimentação'),
    'active': fields.Boolean(required=True, description='Verifica se o plano de alimentação está ativo ou não'),
    'deleted': fields.Boolean(required=True, description='Verifica se o plano de alimentação está deletado ou não')   
})

list_planos_response = namespace.model('Response para lista de planos', {
    'data': fields.Nested(list_planos, required=True, description='Lista de planos de alimentação')
})

headers = namespace.parser()
# Aqui podemos adicionar mais parametros ao headers

@namespace.route('/insert')
@namespace.expect(headers)
class CreatePlano(Resource):
    @namespace.expect(insert_plano, validate=True)
    def post(self):
        """Cadastra uma plano de alimentação"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('nome', type=str)
            parser.add_argument('descricao', type=str)
            parser.add_argument('tipo', type=int)
            parser.add_argument('quantidadeDias', type=int)
            args = parser.parse_args()
            plano = planosCRUD.cadastrarPlano(args)
            if not plano:
                raise Exception("Error")
            return plano
        except Exception as e:
            raise InternalServerError(e.args[0])

@namespace.route('/update/<int:id>')
@namespace.expect(headers)
class UpdatePlano(Resource):
    @namespace.expect(update_plano, validate=True)
    def put(self, id):
        """Atualiza uma plano"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('nome', type=str)
            parser.add_argument('descricao', type=str)
            parser.add_argument('tipo', type=int)
            parser.add_argument('quantidadeDias', type=int)
            parser.add_argument('active', type=bool)
            parser.add_argument('deleted', type=bool)
            args = parser.parse_args()
            plano = planosCRUD.atualizarPlano(id, args)
            if not plano:
                raise Exception("Error")
            return plano
        except Exception as e:
            raise InternalServerError(e.args[0])

@namespace.route('/<int:id>')
@namespace.param('id')
@namespace.expect(headers)
class GetPlano(Resource):
    def get(self, id):
        """Consulta um plano por id"""
        try:
            plano = planosCRUD.consultarPlano(id)
            return PlanoSchema().dump(plano)
        except HTTPException as e:
            raise InternalServerError(e.args[0])


@namespace.route('/', doc={"description": 'Lista todos os matrizes'})
@namespace.expect(headers)
class ListPlanos(Resource):
    @namespace.marshal_with(list_planos_response)
    def get(self):
        """Lista todos os planos de alimentação"""
        try:
            planos = planosCRUD.consultarPlanos()
            return {"data": planos}
        except HTTPException as e:
            raise InternalServerError(e.args[0])


@namespace.route('/delete/<int:id>',
                 doc={"description": 'Deleta um plano de alimentação'})
@namespace.param('id', 'ID da matriz')
@namespace.expect(headers)
class DeletePlano(Resource):
    def delete(self, id):
        """Remove um plano de alimentação"""
        try:
            plano = planosCRUD.excluirPlano(id)
            return plano
        except Exception as e:
            raise InternalServerError(e.args[0])

def bind_with_api(api: Api):
    """
    Adiciona o namespace à API recebida
    :param api: Flask Restplus API
    :return: Vazio
    """
    api.add_namespace(namespace)
    return None