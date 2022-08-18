from ...db import db, ma

class Confinamento(db.Model):
    __tablename__ = "confinamentos"
    __table_args__ = {"schema":"sistemaTCC"}
    id = db.Column("id", db.Integer, primary_key=True)
    planoId = db.Column("plano_id", db.Integer, db.ForeignKey('sistemaTCC.planos.id'))
    matrizId = db.Column("matriz_id", db.Integer, db.ForeignKey('sistemaTCC.matrizes.id'))
    dataConfinamento = db.Column("data_confinamento", db.DateTime)
    active = db.Column("active", db.Boolean, default=True)


class ConfinamentoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Confinamento
        include_fk = True

