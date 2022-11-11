from ...db import db, ma

class Confinamento(db.Model):
    __tablename__ = "confinamentos"
    # __table_args__ = {"schema":"public"}
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    planoId = db.Column("plano_id", db.Integer, db.ForeignKey('planos.id'), primary_key=True)
    matrizId = db.Column("matriz_id", db.Integer, db.ForeignKey('matrizes.id'), primary_key=True)
    dataConfinamento = db.Column("data_confinamento", db.DateTime)
    active = db.Column("active", db.Boolean, default=True)
    deleted = db.Column("deleted", db.Boolean, default=True)
    
    
class ConfinamentoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Confinamento
        include_fk = True

