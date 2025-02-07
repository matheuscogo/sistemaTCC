from ...db import db, ma

class Confinamento(db.Model):
    __tablename__ = "confinamentos"
    # __table_args__ = {"schema":"public"}
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    planoId = db.Column("planos_id", db.Integer, db.ForeignKey('planos.id'))
    matrizId = db.Column("matrizes_id", db.Integer, db.ForeignKey('matrizes.id'))
    dataConfinamento = db.Column("data_confinamento", db.DateTime)
    active = db.Column("active", db.Boolean, default=True)
    deleted = db.Column("deleted", db.Boolean, default=False)
    
    
class ConfinamentoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Confinamento
        include_fk = True

