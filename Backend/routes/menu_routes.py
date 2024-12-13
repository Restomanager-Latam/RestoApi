from flask import Blueprint, request, jsonify
from models import db, Menu, Agregado, Imagen
from schemas import MenuSchema, AgregadoSchema, ImagenSchema
from middleware.auth_middleware import login_required, check_permissions

menu_bp = Blueprint('menu', __name__)

menu_schema = MenuSchema()
menus_schema = MenuSchema(many=True)
agregado_schema = AgregadoSchema(many=True)
imagen_schema = ImagenSchema(many=True)

@menu_bp.route('/menu', methods=['GET'])
def get_menus():
    menus = Menu.query.all()
    result = menus_schema.dump(menus)
    return jsonify(result), 200

@menu_bp.route('/menu/<int:id>', methods=['GET'])
def get_menu(id):
    menu = Menu.query.get_or_404(id)
    menu_data = menu_schema.dump(menu)
    return jsonify(menu_data), 200

@menu_bp.route('/menu/<int:id>', methods=['PUT'])
@login_required
@check_permissions(2)
def update_menu(id):
    menu = Menu.query.get_or_404(id)
    data = request.get_json()

    menu.producto = data.get('producto', menu.producto)
    menu.precio = data.get('precio', menu.precio)
    menu.descripcion = data.get('descripcion', menu.descripcion)
    menu.categoria = data.get('categoria', menu.categoria)

    agregados_data = data.get('agregados', [])
    existing_agregados = {agregado.id: agregado for agregado in Agregado.query.filter_by(id_menu=menu.id).all()}

    for agregado_data in agregados_data:
        agregado_id = agregado_data.get('id')
        if agregado_id and agregado_id in existing_agregados:
            agregado = existing_agregados[agregado_id]
            agregado.nombre = agregado_data.get('nombre', agregado.nombre)
            agregado.precio = agregado_data.get('precio', agregado.precio)
            agregado.descripcion = agregado_data.get('descripcion', agregado.descripcion)
        else:
            new_agregado = Agregado(
                id_menu=menu.id,
                nombre=agregado_data['nombre'],
                precio=agregado_data['precio'],
                descripcion=agregado_data.get('descripcion', '')
            )
            db.session.add(new_agregado)

    imagenes_data = data.get('imagenes', [])
    existing_imagenes = {imagen.id: imagen for imagen in Imagen.query.filter_by(id_menu=menu.id).all()}

    for imagen_data in imagenes_data:
        imagen_id = imagen_data.get('id')
        if imagen_id and imagen_id in existing_imagenes:
            imagen = existing_imagenes[imagen_id]
            imagen.url = imagen_data.get('url', imagen.url)
        else:
            new_imagen = Imagen(
                id_menu=menu.id,
                url=imagen_data['url']
            )
            db.session.add(new_imagen)

    db.session.commit()

    menu_data = menu_schema.dump(menu)
    return jsonify(menu_data), 200

@menu_bp.route('/menu', methods=['POST'])
@login_required
@check_permissions(2)
def create_menu():
    data = request.get_json()

    if isinstance(data, dict):
        data = [data]  
    elif not isinstance(data, list):
        return jsonify({"error": "La solicitud debe contener un objeto o una lista de menús"}), 400

    created_menus = []

    for menu_data in data:

        new_menu = Menu(
            producto=menu_data['producto'],
            precio=menu_data['precio'],
            descripcion=menu_data.get('descripcion', ''),  
            categoria=menu_data.get('categoria', '')  
        )
        db.session.add(new_menu)
        db.session.commit()  

        agregados_data = menu_data.get('agregados', [])
        if agregados_data:  
            agregados = [Agregado(
                id_menu=new_menu.id,
                nombre=agregado_data['nombre'],
                precio=agregado_data['precio'],
                descripcion=agregado_data.get('descripcion', '')  
            ) for agregado_data in agregados_data]
            db.session.add_all(agregados)

        imagenes_data = menu_data.get('imagenes', [])
        if imagenes_data:  
            imagenes = [Imagen(
                id_menu=new_menu.id,
                url=imagen_data['url']
            ) for imagen_data in imagenes_data]
            db.session.add_all(imagenes)

        db.session.commit()

        created_menus.append(menu_schema.dump(new_menu))

    return jsonify(created_menus), 201

@menu_bp.route('/menu/<int:id>', methods=['DELETE'])
@login_required
@check_permissions(2)
def delete_menu(id):
    menu_item = Menu.query.get_or_404(id)

    Agregado.query.filter_by(id_menu=id).delete()
    Imagen.query.filter_by(id_menu=id).delete()

    db.session.delete(menu_item)
    db.session.commit()

    return jsonify({"message": "Producto, agregados e imágenes eliminados"}), 200
