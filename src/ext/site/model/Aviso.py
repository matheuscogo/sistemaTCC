from ...db import db, ma

class Aviso(db.Model):
    __tablename__ = "avisos"
    # __table_args__ = {"schema":"public"}
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    confinamentoId = db.Column("confinamento_id",db.Integer, db.ForeignKey("confinamentos.id"))
    dataAviso = db.Column("data_aviso", db.DateTime)
    separate = db.Column("separate", db.Boolean, default=False)
    type = db.Column("type", db.Integer)
    deleted = db.Column("deleted", db.Boolean, default=True)
    active = db.Column("active", db.Boolean, default=True)
    
class AvisoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Aviso
        include_fk = True

