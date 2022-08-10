from ...db import db, ma

class Aviso(db.Model):
    __tablename__ = "avisos"
    __table_args__ = {"schema":"sistemaTCC"}
    id = db.Column("id", db.Integer, primary_key=True)
    confinamentoId = db.Column(db.Integer, db.ForeignKey("confinamentos.id"))
    dataAviso = db.Column("dataAviso", db.DateTime)
    separar = db.Column("separar", db.Boolean, default=False)
    status = db.Column("status", db.Integer)
    active = db.Column("active", db.Boolean, default=True)

class AvisoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Aviso
        include_fk = True

