from ...db import db, ma

class Alimentador(db):
    __tablename__ = "alimentador"
    id = db.Column("id", db.Integer, primary_key=True)
    matrizId = db.Column("matrizId", db.Integer, db.ForeignKey("matrizes.id"))
    confinamentoId = db.Column("confinamentoId", db.Integer, db.ForeignKey("confinamentos.id"))
    planoId = db.Column("planoId", db.Integer, db.ForeignKey("planos.id"))
    dataEntrada = db.Column("dataEntrada", db.DateTime)
    quantidade = db.Column("quantidade", db.Integer)
    hash = db.Column("hash", db.String)
    
class AlimentadorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Alimentador
        include_fk = True

