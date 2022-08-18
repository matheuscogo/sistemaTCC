from ...db import db, ma

class Matriz(db.Model):
    __tablename__ = 'matrizes'
    __table_args__ = {"schema":"sistemaTCC"}
    id = db.Column("id", db.Integer, primary_key=True)
    rfid = db.Column("rfid", db.VARCHAR)
    numero = db.Column("numero", db.VARCHAR)
    ciclos = db.Column("ciclos", db.Integer)
    deleted = db.Column("deleted", db.Boolean, default=False)

class MatrizSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Matriz
        include_fk = True