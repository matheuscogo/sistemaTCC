from ...db import db, ma

class Parametro(db.Model):
    __tablename__ = "parametros"
    # __table_args__ = {"schema":"public"}
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    tempoPorcao = db.Column("tempo_porcao", db.Integer)
    quantidadePorcao = db.Column("quantidade_porcao", db.Integer)
    intervaloPorcoes = db.Column("intervalo_porcoes", db.Integer)
    tempoProximaMatriz = db.Column("tempo_proxima_matriz", db.Integer)
    tempoSemBrinco = db.Column("tempo_sem_brinco", db.Integer)

class ParametroSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Parametro
        include_fk = True