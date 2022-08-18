# # -*- coding: utf-8 -*-

# import RPi.GPIO as GPIO
# from pirc522 import RFID
# from datetime import datetime
# import time

# import sys
# sys.path.insert(1, '../model')
# sys.path.insert(2, '../view')
# sys.path.insert(3, '../controller')

# bot1 = 37
# bot2 = 35
# led1 = 40
# led2 = 38
# led3 = 36

# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)
# GPIO.setup(bot1, GPIO.IN)
# GPIO.setup(bot2, GPIO.IN)
# GPIO.setup(led1, GPIO.OUT)
# GPIO.setup(led2, GPIO.OUT)
# GPIO.setup(led3, GPIO.OUT)
# rc522 = RFID()


# def leitorRFID():
#     print("\nInsira a tag RFID: ")
#     while True:
#         rc522.wait_for_tag()
#         (error, tag_type) = rc522.request()

#         if not error:
#             (error, uid) = rc522.anticoll()
#         if not error:
#             if str(uid) == 'None':
#                 return True
#             elif str(uid) != 'None':
#                 return str(uid)
#             else:
#                 return False


# def iniciarAlimentador():
#     from ..model import Registro
#     from ..model import Matriz
#     while True:
#         rc522.wait_for_tag()
#         (error, tag_type) = rc522.request()

#         if not error:
#             (error, uid) = rc522.anticoll()
#         if not error:
#             entrada = 1
#             while entrada:
#                 if Matriz.verificaRFID(str(uid)):
#                     registro = Registro()
#                     print('Matriz {} identificada'.format(uid))
#                     registro.setDataEntrada(str(datetime.now().strftime("%d/%m/%Y")))
#                     registro.setHoraEntrada(str(datetime.now().strftime("%H:%M:%S")))
#                     registro.setMatriz(Matriz.consultarID(str(uid)))
#                     GPIO.output(led1, 1)
#                     time.sleep(1)
#                     GPIO.output(led1, 0)
#                     numero = 0
#                     registro.setAcoes(str(numero))
#                     alimentador = 1;
#                     while alimentador:
#                         if (GPIO.input(bot1) == 1):
#                             print('Matriz {} solicitou alimento'.format(uid))
#                             numero = numero + 1
#                             GPIO.output(led3, 1)
#                             time.sleep(1)
#                             GPIO.output(led3, 0)
#                             registro.setAcoes(str(numero))
#                             alimentador = 1
#                         if (GPIO.input(bot2) == 1):
#                             GPIO.output(led2, 1)
#                             time.sleep(1)
#                             GPIO.output(led2, 0)
#                             registro.setDataSaida(str(datetime.now().strftime("%d/%m/%Y")))
#                             registro.setHoraSaida(str(datetime.now().strftime("%H:%M:%S")))
#                             registro.inserir()
#                             print(str(registro.getMatriz()) + " " + registro.getDataEntrada() + " " + registro.getDataSaida() + " " + registro.getHoraEntrada() + " " + registro.getHoraSaida() + " " + registro.getAcoes())
#                             print('Matriz {} saiu do alimentador'.format(uid))
#                             print('Reiniciando sistema')
#                             alimentador = 0
#                             entrada = 0
#                 else:
#                     print("erro rfid")