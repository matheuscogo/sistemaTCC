import datetime
from flask import render_template, request, Blueprint, redirect
from ext.api import rasp
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
        if planosCRUD.exists(request.form.get("nome")) != None:
            plano = Plano(
                nome=request.form.get("nome"),
                          descricao=request.form.get("descricao"),
                          tipo=request.form.get("tipo"),
                          quantidadeDias=int(request.form.get("tipo")),
                          active=1
            )
            json_list = str(('{"plano" : [' + request.form.get("json") + ']}'))
            planosCRUD.cadastrarPlano(plano, json_list)
            templateData = {
                'title': 'Sistema de gerenciamento de matrizes',
                'overview': 'Matrizes',
                'color': 'green',
                'aviso': "Plano de alimentação cadastrado com sucesso!"
            }
            return redirect("http://localhost:3000/planos")
        else:
            templateData = {
                'title': 'Sistema de gerenciamento de matrizes',
                'overview': 'Matrizes',
                'color': 'green',
                'aviso': "Plano de alimentação já existe!"
            }
        return render_template("index.html", **templateData)

    except BaseException as e:
        return render_template("index.html")


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


@bp_controller.route('/TESTE', methods=['POST', 'GET'])
def TESTE():
    from ...db import matrizCRUD, registroCRUD, confinamentoCRUD
    import datetime, time
    from ..model.Registro import Registro
    import RPi.GPIO as GPIO
    from pirc522 import RFID
    
    bot1 = 37
    bot2 = 35
    led1 = 40
    led2 = 38
    led3 = 36

    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(bot1, GPIO.IN)
    GPIO.setup(bot2, GPIO.IN)
    GPIO.setup(led1, GPIO.OUT)
    GPIO.setup(led2, GPIO.OUT)
    GPIO.setup(led3, GPIO.OUT)
    
    dataEntrada = ""
    horaEntrada = ""
    matriz = 0
    quantidade = 0
    dataSaida = ""
    horaSaida = ""    
            
    while True:
        uid = rasp.leitorRFID()
        entrada = 1
        while entrada:
            if not matrizCRUD.existsRFID(str(uid)):
                print('Matriz {} identificada'.format(uid))
                dataEntrada = str(datetime.datetime.now().strftime("%Y-%m-%d"))
                horaEntrada = datetime.datetime.now()
                # matriz = matrizCRUD.consultarMatrizID(str(uid))
                GPIO.output(led3, 1)
                time.sleep(1)
                GPIO.output(led3, 0)
                numero = 0
                alimentador = 1;
                while alimentador:
                    if (GPIO.input(bot1) == 1):
                        print('Matriz {} solicitou alimento'.format(uid))
                        quanti = confinamentoCRUD.consultarQuantidade(str(uid), dataEntrada)
                        print("----------")
                        print()
                        print("Quanti = " + str(quanti))
                        print("Quantidade = " + str(quantidade))
                        print()
                        print("----------")
                        if quanti > quantidade:
                            numero = numero + 1
                            quantidade = quantidade + 400
                            GPIO.output(led2, 1)
                            print(str(time.sleep(5).__str__))
                            GPIO.output(led2, 0)
                            alimentador = 1
                    if (GPIO.input(bot2) == 1):
                        GPIO.output(led1, 1)
                        time.sleep(1)
                        GPIO.output(led1, 0)
                        dataSaida=str(datetime.datetime.now().strftime("%Y-%m-%d"))
                        horaSaida=datetime.datetime.now()
                        tempo = str(horaSaida - horaEntrada)
                        horaEntrada = str(horaEntrada.strftime("%H:%M:%S"))
                        horaSaida = str(horaSaida.strftime("%H:%M:%S"))
                        registro = Registro(matriz=matriz,dataEntrada=dataEntrada,dataSaida=dataSaida,horaEntrada=horaEntrada,horaSaida=horaSaida,tempo=tempo, quantidade=quantidade)
                        print("Data de entrada: " + str(dataEntrada) + ", " + str(type(dataEntrada)) + ", " + str(type(str(dataEntrada))))
                        print("Hora de entrada: " + str(horaEntrada) + ", " + str(type(horaEntrada)) + ", " + str(type(str(horaEntrada))))
                        print("ID da matriz:    " + str(matriz) + ", " + str(type(matriz)) + ", " + str(type(matriz)))
                        print("Data de saida:   " + str(dataSaida) + ", " + str(type(dataSaida)) + ", " + str(type(str(dataSaida))))
                        print("Hora de saida:   " + str(horaSaida) + ", " + str(type(horaSaida)) + ", " + str(type(str(horaSaida))))
                        print("Tempo:   " + str(tempo) + ", " + str(type(tempo)) + ", " + str(type(str(tempo))))
                        print("Quantidade:   " + str(quantidade) + ", " + str(type(quantidade)) + ", " + str(type(str(quantidade))))
                        print("Dia:   " + str(quanti) + ", " + str(type(quanti)) + ", " + str(type(str(quanti))))
                        if registroCRUD.cadastrarRegistro(registro):
                            quantidade = 0
                            quanti = 0
                            total = 0
                            dia=0
                            print("Sucesso")
                        else:
                            print("Falha")
                        print('Matriz {} saiu do alimentador'.format(uid))
                        print('Reiniciando sistema')
                        alimentador = 0
                        entrada = 0
            else:
                print("erro rfid")


@bp_controller.route('/consultarQuantidade', methods=['POST', 'GET'])
def consultarQuantidade():
    return planosCRUD.consultarQuantidade(request.args.get("id"))


@bp_controller.route('/teste2',)
def teste2():
    return str(confinamentoCRUD.consultarQuantidade("[160, 45, 156, 43, 58]", "2021-08-08"))

@bp_controller.route('/time')
def testeTime():
    return {"time": datetime.datetime.now().strftime("%H:%M:%S")}