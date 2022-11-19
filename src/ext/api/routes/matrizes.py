from ext.site.model import Matriz, MatrizSchema
from ...db import db, matrizCRUD
from flask_restx import Api, Namespace, Resource, fields, reqparse
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import InternalServerError

namespace = Namespace(name='Matrizes', description='Matrizes', path='/matrizes')

insert_matriz = namespace.model('Dados para criação de uma matriz', {
    'rfid': fields.String(required=True, description='RFID'),
    'numero': fields.String(required=True, description='Número da matriz'),
    'ciclos': fields.Integer(required=True, description='Ciclos da matriz')
})

update_matriz = namespace.model('Dados para atualização de matrizes', {
    'rfid': fields.String(description='RFID das matrizes'),
    'numero': fields.String(required=True, description='RFID'),
    'ciclos': fields.Integer(required=True, description='Ciclos da matriz')
})

list_matrizes = namespace.model('Lista de matrizes', {
    'id': fields.String(required=True, description='Identificadores das matrizes'),
    'rfid': fields.String(description='RFID das matrizes'),
    'numero': fields.String(description='Numero das matrizes'),
    'ciclos': fields.Integer(description='Ciclos das matrizes')
    
})

list_matrizes_response = namespace.model('Resposta da lista de matrizes', {
    'success': fields.Boolean(required=True, description='Condição da requisição'),
    'message': fields.String(required=True, description='Mensagem da requisição'),
    'response': fields.Nested(list_matrizes, required=True, description='Mensagem da requisição')
})

delete_response = namespace.model('Resposta da remocao de matrizes', {
    'success': fields.Boolean(required=True, description='Condição da requisição'),
    'message': fields.String(required=True, description='Mensagem da requisição'),
    'response': fields.Nested(namespace.model('', {}), required=True, description='Mensagem da requisição')
})

headers = namespace.parser()
# Aqui podemos adicionar mais parametros ao headers

@namespace.route('/insert', methods=['POST'])
@namespace.expect(headers)
class CreateMatriz(Resource):
    @namespace.expect(insert_matriz, validate=True)
    @namespace.doc(security='apikey')
    def post(self):
        """Cadastra uma matriz"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('numero', type=str)
            parser.add_argument('rfid', type=str)
            parser.add_argument('ciclos', type=int)
            args = parser.parse_args()
            
            matriz = Matriz(
                rfid = args['rfid'],
                numero = args['numero'],
                ciclos = args['ciclos'],
            )
            
            matriz = matrizCRUD.cadastrarMatriz(matriz)
            
            if not matriz['success']:
                raise Exception(matriz['message'])
            
            return matriz
        except Exception as e:
            response = {
                'success': False,
                'response': {},
                'message': e.args[0]
            }
            
            return response

@namespace.route('/update/<int:id>')
@namespace.param('id')
@namespace.expect(headers)
class UpdateMatriz(Resource):
    @namespace.expect(update_matriz, validate=True)
    def put(self, id):
        """Atualiza uma matriz pelo id"""
        try:
            parser = reqparse.RequestParser()
            
            parser.add_argument('numero', type=str)
            parser.add_argument('rfid', type=str)
            parser.add_argument('ciclos', type=int)
            
            args = parser.parse_args()
            
            matriz = Matriz(
                rfid=args['rfid'],
                numero=args['numero'],
                ciclos=args['ciclos'],
                active=True,
                deleted=False,
            )
            
            matriz = matrizCRUD.atualizarMatriz(id, matriz)
            
            if not matriz['success']:
                raise BaseException(matriz['message'])

            return matriz
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
class GetMatriz(Resource):
    def get(self, id):
        """Consulta uma matriz por id"""
        try:
            matriz = matrizCRUD.consultarMatriz(id)
            
            if not matriz['success']:
                raise BaseException(matriz['message'])

            return matriz
        except BaseException as e:
            response = {
                'success': False,
                'response': {},
                'message': e.args[0]
            }
        
            return response
        
@namespace.route('/getMatrizByRfid/<rfid>')
@namespace.param('rfid')
@namespace.expect(headers)
class GetMatriz(Resource):
    def get(self, rfid):
        """Consulta uma matriz por rfid"""
        try:
            matriz = matrizCRUD.getMatrizByRfid(rfid=rfid)
            
            if not matriz['success']:
                raise BaseException(matriz['message'])
            
            return matriz
        except BaseException as e:
            response = {
                'success': False,
                'response': {},
                'message': e.args[0]
            }
        
            return response
            

@namespace.route('/', doc={"description": 'Lista todos os matrizes'})
@namespace.expect(headers)
class ListMatrizes(Resource):
    @namespace.marshal_with(list_matrizes_response)
    def get(self):
        """Lista todos os matrizess"""
        try:
            matrizes = matrizCRUD.consultarMatrizes()
            
            if not matrizes['success']:
                raise BaseException(matrizes['message'])

            return matrizes
        except BaseException as e:
            response = {
                'success': False,
                'response': {},
                'message': e.args[0]
            }
            
            return response


@namespace.route('/delete/<int:id>',
                 doc={"description": 'Apaga matrizes'},
                 methods=['DELETE'])
@namespace.param('id', 'ID da matriz')
@namespace.expect(headers)
class DeleteMatriz(Resource):
    @namespace.marshal_with(delete_response)
    def delete(self, id):
        """Remove matrizes"""
        try:
            matriz = matrizCRUD.excluirMatriz(id)
            
            if not matriz['success']:
                raise BaseException(matriz['message'])

            return matriz
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