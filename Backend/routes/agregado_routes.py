from flask import Blueprint, request, jsonify
from models import db, Agregado, Menu
from schemas import AgregadoSchema
from middleware.auth_middleware import login_required, check_permissions

agregado_bp = Blueprint('agregado', __name__)

agregado_schema = AgregadoSchema()
agregados_schema = AgregadoSchema(many=True)

@agregado_bp.route('/agregados', methods=['POST'])
@login_required
@check_permissions(2)
def create_agregado():
    data = request.get_json()

    id_menu = data.get('id_menu')
    menu = Menu.query.get(id_menu)
    
    if not menu:
        return jsonify({"message": "Producto no encontrado"}), 404

    nuevo_agregado = Agregado(
        id_menu=id_menu,
        nombre=data['nombre'],
        precio=data['precio'],
        descripcion=data.get('descripcion', '')
    )

    db.session.add(nuevo_agregado)
    db.session.commit()

    return jsonify(agregado_schema.dump(nuevo_agregado)), 201

@agregado_bp.route('/agregados/<int:id>', methods=['PUT'])
@login_required
@check_permissions(2)
def update_agregado(id):
    agregado = Agregado.query.get_or_404(id)
    data = request.get_json()

    id_menu = data.get('id_menu', agregado.id_menu)
    menu = Menu.query.get(id_menu)

    if not menu:
        return jsonify({"message": "Producto no encontrado"}), 404

    agregado.nombre = data.get('nombre', agregado.nombre)
    agregado.precio = data.get('precio', agregado.precio)
    agregado.descripcion = data.get('descripcion', agregado.descripcion)
    agregado.id_menu = id_menu

    db.session.commit()

    return jsonify(agregado_schema.dump(agregado)), 200

@agregado_bp.route('/agregados/<int:id>', methods=['DELETE'])
@login_required
@check_permissions(2)
def delete_agregado(id):
    agregado = Agregado.query.get_or_404(id)

    db.session.delete(agregado)
    db.session.commit()

    return jsonify({"message": "Agregado eliminado con éxito"}), 200

@agregado_bp.route('/agregados', methods=['GET'])
def get_agregados():
    agregados = Agregado.query.all()
    return jsonify(agregados_schema.dump(agregados)), 200

@agregado_bp.route('/agregados/<int:id>', methods=['GET'])
def get_agregado(id):
    agregado = Agregado.query.get_or_404(id)
    return jsonify(agregado_schema.dump(agregado)), 200
