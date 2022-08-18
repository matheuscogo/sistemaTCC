from ext.site.model.Aviso import Aviso
from ext.site.model.Confinamento import Confinamento
from ext.site.model.Dia import Dia
from ext.site.model.Inseminacao import Inseminacao
from ext.site.model.Matriz import Matriz
from ext.site.model.Plano import Plano
from ext.site.model.Registro import Registro
from ext.site.model.Aviso import AvisoSchema
from ext.site.model.Confinamento import ConfinamentoSchema
from ext.site.model.Dia import DiaSchema
from ext.site.model.Inseminacao import InseminacaoSchema
from ext.site.model.Matriz import MatrizSchema
from ext.site.model.Plano import PlanoSchema
from ext.site.model.Registro import RegistroSchema


def init_app():
    Aviso()
    Confinamento()
    Dia()
    Inseminacao()
    Matriz()
    Plano()
    Registro()
    AvisoSchema()
    ConfinamentoSchema()
    DiaSchema()
    InseminacaoSchema()
    MatrizSchema()
    PlanoSchema()
    RegistroSchema()

