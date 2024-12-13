from . import db
from datetime import datetime

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    id_mesa = db.Column(db.Integer, nullable=False)
    id_menu = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    id_agregado = db.Column(db.Integer, db.ForeignKey('agregados.id'), nullable=True)
    cantidad = db.Column(db.Integer, nullable=False)
    solicitado = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    entregado = db.Column(db.Boolean, default=False)
    hentrega = db.Column(db.DateTime)

    menu = db.relationship('Menu', backref=db.backref('pedidos', lazy=True))

    agregado = db.relationship('Agregado', backref=db.backref('pedidos', lazy=True))

    def __init__(self, id_mesa, id_menu, id_agregado=None, cantidad=1, solicitado=None, entregado=False, hentrega=None):
        self.id_mesa = id_mesa
        self.id_menu = id_menu
        self.id_agregado = id_agregado
        self.cantidad = cantidad
        self.solicitado = solicitado or datetime.utcnow()
        self.entregado = entregado
        self.hentrega = hentrega
