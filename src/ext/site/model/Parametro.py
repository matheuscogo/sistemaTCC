from ...db import db, ma

class Parametro(db.Model):
    __tablename__ = 'parameters'
    __table_args__ = {"schema":"sistemaTCC"}
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    motorOpen = db.Column("rfid", db.Boolean)
    motorClose = db.Column("rfid", db.Boolean)
    motorFeed = db.Column("rfid", db.Boolean)
    quantity = db.Column("rfid", db.Boolean)
    time = db.Column("rfid", db.Boolean)
    rfid = db.Column("rfid", db.Boolean)
    rfid = db.Column("rfid", db.Boolean)
    rfid = db.Column("rfid", db.Boolean)
    
class ParametroSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Parametro
        include_fk = True