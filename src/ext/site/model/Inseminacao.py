from ...db import db, ma

class Inseminacao(db.Model):
    __tablename__ = "inseminacoes"
    __table_args__ = {"schema":"sistemaTCC"}
    id = db.Column("id", db.Integer, primary_key=True)
    planoId = db.Column(db.Integer, db.ForeignKey("planos.id"))
    matrizId = db.Column(db.Integer, db.ForeignKey("matrizes.id"))
    confinamentoId = db.Column(db.Integer, db.ForeignKey("confinamentos.id"))
    dataInseminacao = db.Column("dataInseminacao", db.VARCHAR)
    active = db.Column("active", db.Boolean, default=True)

class InseminacaoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inseminacao
        include_fk = True