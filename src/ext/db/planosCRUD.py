from ..site.model import Plano
from ..site.model import PlanoSchema
from ..db import db


def cadastrarPlano(plano):  # Create
    try:
        if plano.nome == None or plano.nome == "":
            raise Exception("Nome do plano não repasado para o controlador")
            
        if plano.tipo == None or plano.tipo == "":
            raise Exception("Tipo do plano de alimentação não repasado para o controlador")
        
        db.session.add(plano)
        db.session.commit()
        
        response = {
            'success': True,
            'response': {},
            'message': "Plano cadastrado com sucesso!"
        }
            
        return response
    except BaseException as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return  response


# def cadastrarPlano(plano, dias):  # Create
#     try:
#         if plano.nome != None:
#             planoObj = json.loads(str(dias))
#             days = planoObj["plano"]
#             db.session.add(plano)
#             db.session.commit()
#             for i in days:
#                 quantidade = i["quantidade"]
#                 dia1 = i["dias"][0]
#                 dia2 = i["dias"][1]
#                 for y in range(dia1, (dia2+1)):
#                     print("DIAS -> " + str(y) + " quantidade: " + str(quantidade))
#                     db.session.add(Dia(planoId=int(plano.id), dia = y, quantidade=quantidade))
#                     db.session.commit()
#             return ""
#         else:
#             return ""
#     except BaseException as e:
#         return False


def consultarPlanos():  # Read
    try:
        response = db.session.query(Plano).filter_by(deleted=False).all()
        
        planos = []

        for plano in response:
            
            tipo = {}
            
            if plano.tipo == '1':
                tipo =  {
                    'description': "Gestação",
                    'value': "1",
                }
            
            if plano.tipo == '2':
                tipo =  {
                    'description': "Pré - Gestação",
                    'value': "2",
                }
                
            obj = {
                "id": plano.id, 
                "nome": plano.nome, 
                "descricao": plano.descricao, 
                "quantidadeDias": plano.quantidadeDias, 
                "tipo": tipo,
                "active": plano.active
            }
            
            planos.append(obj)
            
        response = {
            'success': True,
            'response': planos,
            'message': ""
        }
            
        return response
    except BaseException as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return  response


def consultarPlano(id): # Read
    try:
        plano = db.session.query(Plano).filter_by(id=id, deleted=False).first()

        response = {
            'success': True,
            'response': plano,
            'message': ""
        }
            
        return response
    except BaseException as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return  response


def atualizarPlano(id, newPlano):  # Update
    try:
        hasPlano = db.session.query(Plano.query.filter_by(id=id, deleted=False).exists()).scalar()
        
        if not hasPlano:
            raise BaseException("Plano não encontrada.")
        
        plano = db.session.query(Plano).filter_by(id=id, deleted=False).first()

        plano.id = id
        plano.nome = newPlano.nome
        plano.descricao = newPlano.descricao
        plano.tipo = newPlano.tipo
        plano.quantidadeDias = newPlano.quantidadeDias

        db.session.commit()
        
        response = {
            'success': True,
            'response': {},
            'message': "Plano atualizado com sucesso!"
        }
            
        return response
    except BaseException as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return  response
    except Exception as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return  response


def excluirPlano(id):  # Delete
    try:
        plano = db.session.query(Plano).filter_by(id=id, deleted=False).first()
        
        if not plano:
            raise Exception(PlanoSchema().dump(plano))
        
        plano.deleted = True
        
        db.session.add(plano)
        db.session.commit()
        
        response = {
            'success': True,
            'response': {},
            'message': "Plano excluido com sucesso!"
        }
            
        return response
    except BaseException as e:
        response = {
            'success': False,
            'response': {},
            'message': e.args[0]
        }
        
        return  response


# def exists(nome):
#     exists = db.session.query(db.exists().where(
#         Plano.nome == nome)).scalar()
#     print(str(exists))
#     if exists:
#         return False
#     else:
#         return True

# def consultarQuantidade(id):
#     try:
#         quantidades = db.session.query(
#             Dia.Dias.quantidade).filter_by(plano=id).all()
#         array = list()
#         for quantidade in quantidades:
#             array.append(quantidade[0])
#         json_str = json.dumps(array)
#         return json_str
#     except:
#         return False
