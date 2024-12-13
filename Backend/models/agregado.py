from . import db

class Agregado(db.Model):
    __tablename__ = 'agregados'
    id = db.Column(db.Integer, primary_key=True)
    id_menu = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.String(255))

    #menu = db.relationship('Menu', backref=db.backref('agregados', lazy=True))
