import datetime
from flask import render_template, request, Blueprint, redirect
from ..model.Matriz import Matriz
from ..model.Plano import Plano
from ...db import matrizCRUD, planosCRUD, confinamentoCRUD


bp_controller = Blueprint('routes', __name__)


@bp_controller.route('/cadastrarMatriz', methods=['POST', 'GET'])
def cadastrarMatriz():  # Cadastrar Matriz
    try:
        matriz = Matriz(rfid="teste",
                        numero=0,
                        ciclos=0)
        retorno = matrizCRUD.cadastrarMatriz(matriz)
        templateData = {
            'title': 'Sistema de gerenciamento de matrizes',
            'overview': 'Matrizes',
            'color': 'green',
            'retorno': retorno
        }
        return render_template("index.html", **templateData)
    except BaseException as e:
        templateData = {
            'title': 'Sistema de gerenciamento de matrizes',
            'color': 'green',
            'aviso': "Erro ao cadastrar Matriz"
        }
        return render_template("index.html", **templateData)


@bp_controller.route('/consultarMatriz', methods=['POST', 'GET'])
def consultaMatrizes():  # Consultar Matriz
    templateData = {
        'title': 'Sistema de gerenciamento de matrizes',
    }
    matrizes = matrizCRUD.consultarMatriz()
    return render_template("matrizes.html", matrizes=matrizes, **templateData)


@bp_controller.route('/atualizarMatriz', methods=['POST', 'GET'])
def atualizarMatriz():  # Atualizar Matriz
    try:
        matriz = request.form.get("id")
        matrizCRUD.atualizarMatriz(matriz)
        templateData = {
            'title': 'Sistema de gerenciamento de matrizes',
            'overview': 'Matrizes',
            'color': 'green',
            'aviso': "<scrit>alert('Matriz atualizada com sucesso')</script>"
        }
        return render_template("index.html", **templateData)
    except BaseException as e:
        templateData = {
            'title': 'Sistema de gerenciamento de matrizes',
            'color': 'green',
            'aviso': "Erro ao atualizar Matriz"
        }
        return render_template("index.html", **templateData)


@bp_controller.route('/excluirMatriz', methods=['POST', 'GET'])
def excluirMatriz():  # Excluir Matriz
    try:
        matrizCRUD.excluirMatriz(request.form.get("id"))
        templateData = {
            'title': 'Sistema de gerenciamento de matrizes',
            'overview': 'Matrizes',
            'color': 'green',
            'aviso': "Matriz"
        }
        return render_template("index.html", **templateData)
    except BaseException as e:
        templateData = {
            'title': 'Sistema de gerenciamento de matrizes',
            'color': 'green',
            'aviso': "Erro ao atualizar Matriz"
        }
        return render_template("index.html", **templateData)


@bp_controller.route('/cadastrarPlano', methods=['POST'])
def cadastrarPlano():  # Cadastrar Plano
    try:
        plano = Plano(
            nome=request.form.get("nome"),
            descricao=request.form.get("descricao"),
            tipo=request.form.get("tipo"),
            quantidadeDias=request.form.get("tipo"),
            active=True,
            deleted=False
        )
        json_list = str(('{"plano" : [' + request.form.get("json") + ']}'))
        
        planosCRUD.cadastrarPlano(plano, json_list)

        return render_template("main/cadastrarPlano.html")
    except BaseException as e:
        return render_template("main/cadastrarPlano.html")


@bp_controller.route('/atualizarPlano', methods=['POST', 'GET'])
def atualizarPlano():  # Atualizar Plano
    try:
        matriz = request.form.get("id")
        matrizCRUD.atualizarMatriz(matriz)
        templateData = {
            'title': 'Sistema de gerenciamento de matrizes',
            'overview': 'Matrizes',
            'color': 'green',
            'aviso': "<scrit>alert('Matriz atualizada com sucesso')</script>"
        }
        return render_template("index.html", **templateData)
    except BaseException as e:
        templateData = {
            'title': 'Sistema de gerenciamento de matrizes',
            'color': 'green',
            'aviso': "Erro ao atualizar Matriz"
        }
        return render_template("index.html", **templateData)


@bp_controller.route('/excluirPlano', methods=['POST', 'GET'])
def excluirPlano():  # Excluir Plano
    try:
        matrizCRUD.excluirMatriz(request.form.get("id"))
        templateData = {
            'title': 'Sistema de gerenciamento de matrizes',
            'overview': 'Matrizes',
            'color': 'green',
            'aviso': "Matriz"
        }
        return render_template("index.html", **templateData)
    except BaseException as e:
        templateData = {
            'title': 'Sistema de gerenciamento de matrizes',
            'color': 'green',
            'aviso': "Erro ao atualizar Matriz"
        }
        return render_template("index.html", **templateData)


@bp_controller.route('/cadastrarConfinamento', methods=['POST', 'GET'])
def cadastrarConfinamento():
    try:
        matriz = int(request.form.get("matriz"))
        confinamentoCRUD.cadastrarConfinamento(request)
        templateData = {
            'title': 'Sistema de gerenciamento de matrizes',
            'overview': 'Matrizes',
            'color': 'green',
            'aviso': "Matriz"
        }
        return redirect('detalhesMatriz.html?id=' + str(matriz))
    except:
        return render_template("index.html", **templateData)
