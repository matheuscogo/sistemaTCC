from ...db import db, ma

class Registro(db.Model):
    __tablename__ = "registros"
    __table_args__ = {"schema":"sistemaTCC"}
    id = db.Column("id", db.Integer, primary_key=True)
    matrizId = db.Column(db.Integer, db.ForeignKey("confinamento.matrizId"))
    dataEntrada = db.Column("dataEntrada", db.DateTime)
    dataSaida = db.Column("dataSaida", db.DateTime)
    tempo = db.Column("tempo", db.VARCHAR)
    quantidade = db.Column("quantidade", db.Integer)

class RegistroSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Registro
        include_fk = True