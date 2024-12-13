from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .menu import Menu
from .agregado import Agregado
from .pedido import Pedido
from .imagen import Imagen
from .permiso import Permiso
from .usuario import Usuario
from .mozoCaller import Llamadas