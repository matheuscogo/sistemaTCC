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

insert_aviso = namespace.model('Dados para criação de um aviso', {
    'dataAviso': fields.DateTime(required=True, description='Data de criação do aviso'),
    'confinamentoId': fields.Integer(required=True, description='FK do confinamento')
})

update_aviso = namespace.model('Dados para atualizar o aviso', {
    'id': fields.Integer(required=True, description='ID do aviso'),
    'separate': fields.Boolean(required=True, description='Valor da flag')
})

list_avisos = namespace.model('Lista de avisos', {
    'id': fields.Integer(required=True, description='ID do aviso'),
    'aviso': fields.Nested(namespace.model('', {'label': fields.String, 'value': fields.Integer}), required=True, description='Descrição da flag separar'),
    'dataAviso': fields.DateTime(required=True, description='Data da criação do registro do aviso'),
    'separate': fields.Boolean(required=True, description='Flag para separação'),
    'active': fields.Boolean(required=True, description='FK do plano de alimentação')
})

list_avisos_response = namespace.model('Resposta para lista de avisos', {
    'data': fields.Nested(list_avisos, required=True, description='Lista de avisos')
})

headers = namespace.parser()

@namespace.route('/insert', methods=['POST'])
@namespace.expect(headers)
class CreateAviso(Resource):
    @namespace.expect(insert_aviso, validate=True)
    def post(self):
        """Cadastra um aviso"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('dataAviso', type=lambda s: datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%fZ'))
            parser.add_argument('confinamentoId', type=int)
            args = parser.parse_args()
            
            aviso = avisoCRUD.cadastrarAviso(Aviso(
                dataAviso=args['dataAviso'],
                confinamentoId=args['confinamentoId'],
            ))
            
            if not aviso:
                raise Exception("Error")
            return aviso
        except Exception as e:
            raise InternalServerError(e.args[0])

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

# @namespace.route('/<int:id>')
# @namespace.param('id')
# @namespace.expect(headers)
# class GetRegistro(Resource):
#     def get(self, id):
#         """Consulta um registro por id"""
#         try:
#             confinamento = confinamentoCRUD.consultarConfinamento(id)
#             return confinamento
#         except HTTPException as e:
#             raise InternalServerError(e.args[0])


@namespace.route('/')
@namespace.expect(headers)
class ListaRegistros(Resource):
    @namespace.marshal_with(list_avisos_response)
    def get(self):
        """Lista todos os avisos pendentes"""
        try:
            avisos = avisoCRUD.consultarAvisos()
            return {"data": avisos}
        except HTTPException as e:
            raise InternalServerError(e.args[0])


# @namespace.route('/delete/<int:id>')
# @namespace.param('id', 'ID do confinamento')
# @namespace.expect(headers)
# class DeleteRegistro(Resource):
#     def delete(self, id):
#         """Remove um registro"""
#         try:
#             confinamento = confinamentoCRUD.excluirConfinamento(id)
#             return confinamento
#         except Exception as e:
#             raise InternalServerError(e.args[0])


# @namespace.route('/getConfinamentoByMatriz/<int:matrizId>')
# @namespace.param('matrizId', 'ID da matriz')
# @namespace.expect(headers)
# class GetConfinamentoByMatriz(Resource):
#     def get(self, matrizId):
#         """Consulta um confinamento pelo id de uma matriz"""
#         try:
#             confinamento = confinamentoCRUD.getConfinamentoByMatriz(matrizId)
#             return confinamento
#         except Exception as e:
#             raise InternalServerError(e.args[0])


# @namespace.route('/getDaysInConfinament/<int:matrizId>')
# @namespace.param('matrizId', 'ID da matriz')
# @namespace.expect(headers)
# class GetDaysInConfinament(Resource):
#     def get(self, matrizId):
#         """Consulta um confinamento pelo id de uma matriz"""
#         try:
#             confinamento = confinamentoCRUD.getDaysInConfinament(matrizId)
#             return confinamento
#         except Exception as e:
#             raise InternalServerError(e.args[0])


# @namespace.route('/canOpenDoor/<int:matrizId>')
# @namespace.param('matrizId', 'ID da matriz')
# @namespace.expect(headers)
# class canOpenDoor(Resource):
#     def get(self, matrizId):
#         """Consulta um confinamento pelo id de uma matriz"""
#         try:
#             confinamento = confinamentoCRUD.canOpenDoor(matrizId)
#             return confinamento
#         except Exception as e:
#             raise InternalServerError(e.args[0])


# @namespace.route('/getQuantityForMatriz/<int:matrizId>')
# @namespace.param('matrizId', 'ID da matriz')
# @namespace.expect(headers)
# class GetQuantityForMatriz(Resource):
#     def get(self, matrizId):
#         """Consulta um confinamento pelo id de uma matriz"""
#         try:
#             confinamento = confinamentoCRUD.getQuantityForMatriz(matrizId)
#             return confinamento
#         except Exception as e:
#             raise InternalServerError(e.args[0])


# @namespace.route('/verifyDaysToOpen')
# @namespace.expect(headers)
# class ListaRegistros(Resource):
#     def get(self):
#         """Verifica quais matrizes podem ser separadas"""
#         try:
#             confinamentoCRUD.verifyDaysToOpen()
#             return True
#         except HTTPException as e:
#             raise InternalServerError(e.args[0])


def bind_with_api(api: Api):
    api.add_namespace(namespace)
    return None
