from . import db

class Imagen(db.Model):
    __tablename__ = 'imagen'
    id = db.Column(db.Integer, primary_key=True)
    id_menu = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)

    #menu = db.relationship('Menu', backref=db.backref('imagenes', lazy=True, cascade='all, delete-orphan'))
