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
    'matrizId': fields.Integer(required=True, description='FK da matriz'),
    'dataEntrada': fields.String(required=True, description='Dia da entrada da matriz no alimentador'),
    'dataSaida': fields.String(required=True, description='Dia da saida da matriz no alimentador'),
    'horaEntrada': fields.String(required=True, description='Hora de entrada da matriz no alimentador'),
    'horaSaida': fields.String(required=True, description='Hora de saida da matriz no alimentador'),
    'tempo': fields.String(required=True, description='Tempo que a matriz permaneceu no confinamento'),
    'quantidade': fields.Integer(required=True, description='Quantidade de ração consumida pela matriz')
})

list_registros_response = namespace.model('Resposta da lista de registros', {
    'response': fields.Nested(list_registros, required=True, description='Lista de registros')
})

headers = namespace.parser()
# Aqui podemos adicionar mais parametros ao headers

@namespace.route('/insert')
@namespace.expect(headers)
class CreateRegistro(Resource):
    @namespace.expect(insert_registro, validate=True)
    def post(self):
        """Cadastra um registro"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('matrizId', type=int)
            parser.add_argument('dataEntrada', type=str)
            parser.add_argument('dataSaida', type=str)
            parser.add_argument('horaEntrada', type=str)
            parser.add_argument('horaSaida', type=str)
            parser.add_argument('tempo', type=str)
            parser.add_argument('quantidade', type=int)
            args = parser.parse_args()
            registro = registroCRUD.cadastrarRegistro(args)
            if not registro:
                raise Exception("Error")
            return registro
        except Exception as e:
            raise InternalServerError(e.args[0])

@namespace.route('/update/')
@namespace.expect(headers)
class UpdateRegistro(Resource):
    @namespace.expect(update_registro, validate=True)
    def put(self):
        """Atualiza um registro"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=int)
            parser.add_argument('matriz', type=int)
            parser.add_argument('dataEntrada', type=str)
            parser.add_argument('dataSaida', type=str)
            parser.add_argument('horaEntrada', type=str)
            parser.add_argument('horaSaida', type=str)
            parser.add_argument('tempo', type=str)
            parser.add_argument('quantidade', type=int)
            args = parser.parse_args()
            registro = registroCRUD.atualizarRegistro(args)
            if not registro:
                raise Exception("Error")
            return registro
        except Exception as e:
            raise InternalServerError(e.args[0])

@namespace.route('/<int:id>')
@namespace.param('id')
@namespace.expect(headers)
class GetRegistro(Resource):
    def get(self, id):
        """Consulta um registro por id"""
        try:
            registro = registroCRUD.consultarRegistro(id)
            return registro
        except HTTPException as e:
            raise InternalServerError(e.args[0])


@namespace.route('/', doc={"description": 'Lista todos os matrizes'})
@namespace.expect(headers)
class ListaRegistros(Resource):
    @namespace.marshal_with(list_registros_response)
    def get(self):
        """Lista todos os registros"""
        try:
            registros = registroCRUD.consultarRegistros()
            return { "response": registros }
        except HTTPException as e:
            raise InternalServerError(e.args[0])


@namespace.route('/delete/<int:id>',
                 doc={"description": 'Apaga um registro'})
@namespace.param('id', 'ID do registro')
@namespace.expect(headers)
class DeleteRegistro(Resource):
    def delete(self, id):
        """Remove um registro"""
        try:
            registro = registroCRUD.excluirRegistro(id)
            return registro
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