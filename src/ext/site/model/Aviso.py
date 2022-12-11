from ...db import db, ma

class Aviso(db.Model):
    __tablename__ = "avisos"
    # __table_args__ = {"schema":"public"}
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    confinamentoId = db.Column("confinamentos_id",db.Integer, db.ForeignKey("confinamentos.id"))
    dataAviso = db.Column("data_aviso", db.DateTime)
    separate = db.Column("separate", db.Boolean, default=False)
    tipo = db.Column("tipo", db.Integer)
    active = db.Column("active", db.Boolean, default=True)
    deleted = db.Column("deleted", db.Boolean, default=False)
    
class AvisoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Aviso
        include_fk = True

