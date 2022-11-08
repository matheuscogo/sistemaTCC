from ext.site.model import Dia, DiaSchema
from ...db import diasCRUD
from flask_restx import Api, Namespace, Resource, fields, reqparse
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import InternalServerError
import json

namespace = Namespace(name='Dias', description='Dias', path='/dias')

insert_dia = namespace.model('Dados para criação de um dia', {
    'plano': fields.Integer(required=True, description='FK do plano de alimentação'),
    'dia': fields.Integer(required=True, description='Dias em confinamento'),
    'quantidade': fields.Integer(required=True, description='Quantidade de ração para esse dia de confinamento')
})

update_dia = namespace.model('Dados para atualização de um dia', {
    'id': fields.Integer(required=True, description='ID do dia'),
    'plano': fields.Integer(required=True, description='FK do plano de alimentação'),
    'dia': fields.Integer(required=True, description='Dias em confinamento'),
    'quantidade': fields.Integer(required=True, description='Quantidade de ração para esse dia de confinamento')
})

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

@namespace.route('/insert')
@namespace.expect(headers)
class CreateDia(Resource):
    @namespace.expect(insert_dia, validate=True)
    def post(self):
        """Cadastra um dia"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('plano', type=int)
            parser.add_argument('dia', type=int)
            parser.add_argument('quantidade', type=int)
            
            args = parser.parse_args()
            dia = diasCRUD.cadastrarDia(args)
            if not dia:
                raise Exception("Error")
            return dia
        except Exception as e:
            raise InternalServerError(e.args[0])

@namespace.route('/update/')
@namespace.expect(headers)
class UpdateDia(Resource):
    @namespace.expect(update_dia, validate=True)
    def put(self):
        """Atualiza um dia"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=int)
            parser.add_argument('plano', type=int)
            parser.add_argument('dia', type=int)
            parser.add_argument('quantidade', type=int)
            args = parser.parse_args()
            dia = diasCRUD.atualizarDia(args)
            if not dia:
                raise Exception("Error")
            return dia
        except Exception as e:
            raise InternalServerError(e.args[0])

@namespace.route('/<int:dia>/<int:planoId>')
@namespace.param('dia')
@namespace.param('planoId')
@namespace.expect(headers)
class GetDia(Resource):
    def get(self, dia, planoId):
        """Consulta um dia por id"""
        try:
            dia = diasCRUD.consultarDia(planoId=planoId, dia=dia)
            return dia
        except HTTPException as e:
            raise InternalServerError(e.args[0])


@namespace.route('/', doc={"description": 'Lista todos os matrizes'})
@namespace.expect(headers)
class ListaDias(Resource):
    @namespace.marshal_with(list_dias_response)
    def get(self):
        """Lista todos os dias"""
        try:
            dias = diasCRUD.consultarDias()
            return {"data": dias}
        except HTTPException as e:
            raise InternalServerError(e.args[0])


@namespace.route('/delete/<int:id>',
                 doc={"description": 'Apaga um dia'})
@namespace.param('id', 'ID da matriz')
@namespace.expect(headers)
class DeleteDia(Resource):
    def delete(self, id):
        """Remove um dia"""
        try:
            dia = diasCRUD.excluirDia(id)
            return dia
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