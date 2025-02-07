from ...db import db, ma

class Registro(db.Model):
    __tablename__ = "registros"
    # __table_args__ = {"schema":"public"}
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    confinamentoId = db.Column("confinamento_id", db.Integer, db.ForeignKey("confinamentos.id"))
    dataEntrada = db.Column("data_entrada", db.DateTime)
    dataSaida = db.Column("data_saida", db.DateTime)
    quantidade = db.Column("quantidade", db.Integer)

class RegistroSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Registro
        include_fk = True