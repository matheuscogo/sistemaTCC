from ...db import db, ma

class Inseminacao(db.Model):
    __tablename__ = "inseminacoes"
    __table_args__ = {"schema":"sistemaTCC"}
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    planoId = db.Column("plano_id", db.Integer, db.ForeignKey("sistemaTCC.planos.id"))
    matrizId = db.Column("matriz_id", db.Integer, db.ForeignKey("sistemaTCC.matrizes.id"))
    confinamentoId = db.Column("confinamento_id", db.Integer, db.ForeignKey("sistemaTCC.confinamentos.id"))
    dataInseminacao = db.Column("data_inseminacao", db.DateTime)
    active = db.Column("active", db.Boolean, default=True)

class InseminacaoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inseminacao
        include_fk = True