from ...db import db, ma

class Inseminacao(db.Model):
    __tablename__ = "inseminacoes"
    # __table_args__ = {"schema":"public"}
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    matrizId = db.Column("matriz_id", db.Integer, db.ForeignKey("confinamentos.matrizes_id"))
    confinamentoId = db.Column("confinamento_id", db.Integer, db.ForeignKey("confinamentos.id"))
    dataInseminacao = db.Column("data_inseminacao", db.DateTime)
    active = db.Column("active", db.Boolean, default=True)
    deleted = db.Column("deleted", db.Boolean, default=False)

class InseminacaoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inseminacao
        include_fk = True