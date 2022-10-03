from ...db import db, ma

class Registro(db.Model):
    __tablename__ = "registros"
    __table_args__ = {"schema":"sistemaTCC"}
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    matrizId = db.Column("matriz_id", db.Integer, db.ForeignKey("sistemaTCC.confinamento.matrizId"))
    dataEntrada = db.Column("data_entrada", db.DateTime)
    dataSaida = db.Column("data_saida", db.DateTime)
    tempo = db.Column("tempo", db.VARCHAR)
    quantidade = db.Column("quantidade", db.Integer)

class RegistroSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Registro
        include_fk = True