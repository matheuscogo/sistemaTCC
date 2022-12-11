import imp
from ..db import db
from ..site.model import Matriz
from ..site.model import Confinamento
from ..site.model import Dia
from ..site.model import Plano
from ..site.model import Registro
from ..site.model import Inseminacao
from ..site.model import Aviso
from ..site.model import Parametro


def create_db():
    """Creates database"""
    db.create_all()
    db.session.commit()


def drop_db():
    """Cleans database"""
    db.drop_all()
    db.session.commit()
