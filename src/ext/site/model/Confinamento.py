from ...db import db, ma

class Confinamento(db.Model):
    __tablename__ = "confinamentos"
    __table_args__ = {"schema":"sistemaTCC"}
    id = db.Column("id", db.Integer, primary_key=True)
    planoId = db.Column(db.Integer, db.ForeignKey("planos.id"))
    matrizId = db.Column(db.Integer, db.ForeignKey("matrizes.id"))
    dataConfinamento = db.Column("dataConfinamento", db.DateTime)
    active = db.Column("active", db.Boolean, default=True)


class ConfinamentoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Confinamento
        include_fk = True

