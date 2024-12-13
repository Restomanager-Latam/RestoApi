from flask import Blueprint, request, jsonify
from models import db, Imagen, Menu
from schemas import ImagenSchema
from middleware.auth_middleware import login_required, check_permissions

imagen_bp = Blueprint('imagen', __name__)

imagen_schema = ImagenSchema()
imagenes_schema = ImagenSchema(many=True)

@imagen_bp.route('/imagen', methods=['POST'])
@login_required
@check_permissions(2)
def create_imagen():
    data = request.get_json()
    id_menu = data.get('id_menu')
    
    
    menu = Menu.query.get(id_menu)
    if not menu:
        return jsonify({"message": "Producto de menú no encontrado"}), 404

    nueva_imagen = Imagen(
        id_menu=id_menu,
        url=data['url']
    )

    db.session.add(nueva_imagen)
    db.session.commit()

    return imagen_schema.jsonify(nueva_imagen), 201

@imagen_bp.route('/imagen/menu/<int:id_menu>', methods=['GET'])
def get_imagenes_by_menu(id_menu):
   
    menu = Menu.query.get(id_menu)
    if not menu:
        return jsonify({"message": "Producto de menú no encontrado"}), 404

    imagenes = Imagen.query.filter_by(id_menu=id_menu).all()
    return jsonify(imagenes_schema.dump(imagenes)), 200


@imagen_bp.route('/imagen/<int:id>', methods=['GET'])
def get_imagen(id):
    imagen = Imagen.query.get_or_404(id)
    return imagen_schema.jsonify(imagen), 200


@imagen_bp.route('/imagen/<int:id>', methods=['PUT'])
@login_required
@check_permissions(2)
def update_imagen(id):
    imagen = Imagen.query.get_or_404(id)
    data = request.get_json()

    imagen.url = data.get('url', imagen.url)

    db.session.commit()

    return imagen_schema.jsonify(imagen), 200

@imagen_bp.route('/imagen/<int:id>', methods=['DELETE'])
@login_required
@check_permissions(2)
def delete_imagen(id):
    imagen = Imagen.query.get_or_404(id)

    db.session.delete(imagen)
    db.session.commit()

    return jsonify({"message": "Imagen eliminada con éxito"}), 200
