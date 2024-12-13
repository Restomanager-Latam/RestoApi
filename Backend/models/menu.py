from . import db

class Menu(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    producto = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.String(255))
    categoria = db.Column(db.String(100))

    agregados = db.relationship('Agregado', backref='menu', lazy=True, cascade='all, delete-orphan')
    imagenes = db.relationship('Imagen', backref='menu', lazy=True, cascade='all, delete-orphan')
