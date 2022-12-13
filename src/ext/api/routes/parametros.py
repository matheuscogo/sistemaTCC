from ...db import parametroCRUD
from ...site.model.Parametro import Parametro
from flask_restx import Namespace, Resource, fields, reqparse, Api

namespace = Namespace(name='Parametro', description='Parametro', path='/parametros')

update_parametros = namespace.model('Dados para atualização do parametro', {
    'tempoPorcao': fields.Integer(required=True, description='Porção'),
    'quantidadePorcao': fields.Integer(required=True, description='Quantidade'),
    'intervaloPorcoes': fields.Integer(required=True, description='Intervalo'),
    'tempoProximaMatriz': fields.Integer(required=True, description='Abrir'),
    'tempoSemBrinco': fields.Integer(required=True, description='Tempo Sem Brinco'),
})

list_parametros = namespace.model('Lista de parametros', {
    'id': fields.Integer(required=True, description='Identificador do plano'),
    'tempoPorcao': fields.Integer(required=True, description='Porção'),
    'quantidadePorcao': fields.Integer(required=True, description='Quantidade'),
    'intervaloPorcoes': fields.Integer(required=True, description='Intervalo'),
    'tempoProximaMatriz': fields.Integer(required=True, description='Abrir'),
    'tempoSemBrinco': fields.Integer(required=True, description='Tempo Sem Brinco'),
})

list_parametros_response = namespace.model('Resposta da lista de parametros', {
    'success': fields.Boolean(required=True, description='Condição da requisição'),
    'message': fields.String(required=True, description='Mensagem da requisição'),
    'response': fields.Nested(list_parametros, skip_none=True, description='Mensagem da requisição')
})



headers = namespace.parser()
# Aqui podemos adicionar mais parametros ao headers

@namespace.route('/update/', methods=["PUT"])
@namespace.expect(headers)
class UpdateParametro(Resource):
    @namespace.expect(update_parametros, validate=True)
    def put(self):
        """Atualiza parametro"""
        try:
            parser = reqparse.RequestParser()
            
            parser.add_argument('tempoPorcao', type=int)
            parser.add_argument('quantidadePorcao', type=int)
            parser.add_argument('intervaloPorcoes', type=int)
            parser.add_argument('tempoProximaMatriz', type=int)
            parser.add_argument('tempoSemBrinco', type=int)
            
            args = parser.parse_args()
            
            parametro = Parametro(
                tempoPorcao = args['tempoPorcao'],
                quantidadePorcao = args['quantidadePorcao'],
                intervaloPorcoes = args['intervaloPorcoes'],
                tempoProximaMatriz = args['tempoProximaMatriz'],
                tempoSemBrinco = args['tempoSemBrinco']
            ) 

            parametro = parametroCRUD.atualizarParamtro(id=1, parametro=parametro)
            
            if not parametro['success']:
                raise BaseException(parametro['message'])

            return parametro
        except BaseException as e:
            response = {
                'success': False,
                'response': {},
                'message': e.args[0]
            }
            
            return response


@namespace.route('/', doc={"description": 'Lista os parametros'}, methods=["GET"])
@namespace.expect(headers)
class ListParametros(Resource):
    @namespace.marshal_with(list_parametros_response)
    def get(self):
        """Lista os parametros"""
        try:
            parametros = parametroCRUD.consultarParametros()
            
            if not parametros['success']:
                raise BaseException(parametros['message'])

            return parametros
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