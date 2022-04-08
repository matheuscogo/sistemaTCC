from ...db import db, ma
from sqlalchemy.orm import relationship

class Aviso(db.Model):
    __tablename__ = "avisos"
    id = db.Column("id", db.Integer, primary_key=True)
    confinamentoId = db.Column(db.Integer, db.ForeignKey("confinamento.id"))
    dataAviso = db.Column("dataAviso", db.VARCHAR)
    separar = db.Column("separar", db.Boolean, default=False)
    active = db.Column("active", db.Boolean, default=True)

class AvisoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Aviso
        include_fk = False

