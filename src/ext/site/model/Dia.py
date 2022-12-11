from ...db import db, ma

class Dia(db.Model):
    __tablename__ = "dias"
    # __table_args__ = {"schema":"public"}
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    planoId = db.Column("planos_id", db.Integer,  db.ForeignKey("planos.id"))
    dia = db.Column("dia", db.Integer)
    quantidade = db.Column("quantidade", db.Integer)

class DiaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Dia
        include_fk = True

