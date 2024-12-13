from . import db

class Permiso(db.Model):
    __tablename__ = 'permisos'
    id = db.Column(db.Integer, primary_key=True)
    nivel = db.Column(db.Integer, nullable=False)  # Nivel de permiso (ej. 1 = básico, 2 = admin)
    descripcion = db.Column(db.String(255))

