from flask import Blueprint
from .menu_routes import menu_bp
from .agregado_routes import agregado_bp
from .pedido_routes import pedido_bp
from .auth_routes import auth_bp
from .imagen_routes import imagen_bp
from .mozoCaller_routes import  mozoCaller_bp


def init_app(app):
    app.register_blueprint(menu_bp)
    app.register_blueprint(agregado_bp)
    app.register_blueprint(pedido_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(imagen_bp)
    app.register_blueprint(mozoCaller_bp)
