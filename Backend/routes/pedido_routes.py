from flask import Blueprint, request, jsonify
from models import db, Pedido, Menu, Agregado
from schemas import MenuSchema, AgregadoSchema
from datetime import datetime, timedelta
import pytz
from middleware.auth_middleware import login_required, check_permissions

pedido_bp = Blueprint('pedido', __name__)

menu_schema = MenuSchema()
agregado_schema = AgregadoSchema(many=True)

@pedido_bp.route('/pedidos', methods=['POST'])
def create_pedido():
    data = request.get_json()

    if isinstance(data, dict):
        data = [data]

    for pedido_data in data:
        id_menu = pedido_data.get('id_menu')
        id_mesa = pedido_data.get('id_mesa')
        agregados = pedido_data.get('agregados', [])
        cantidad = pedido_data.get('cantidad', 1)

        menu_item = Menu.query.get(id_menu)
        if not menu_item:
            return jsonify({"message": f"El menú con ID {id_menu} no existe"}), 400

        for id_agregado in agregados:
            agregado = Agregado.query.filter_by(id=id_agregado, id_menu=id_menu).first()
            if not agregado:
                return jsonify({"message": f"Opción de agregado incorrecta: el agregado con ID {id_agregado} no pertenece al menú {id_menu}"}), 400

            nuevo_pedido = Pedido(
                id_mesa=id_mesa,
                id_menu=id_menu,
                id_agregado=id_agregado,
                cantidad=cantidad,
                solicitado=datetime.utcnow(),
                entregado=False,
                hentrega=None
            )
            db.session.add(nuevo_pedido)

        if not agregados:
            nuevo_pedido = Pedido(
                id_mesa=id_mesa,
                id_menu=id_menu,
                id_agregado=None,
                cantidad=cantidad,
                solicitado=datetime.utcnow(),
                entregado=False,
                hentrega=None
            )
            db.session.add(nuevo_pedido)

    db.session.commit()

    return jsonify({"message": "Pedido(s) creado(s) con éxito"}), 201



@pedido_bp.route('/pedidos', methods=['GET'])
def get_pedidos():
    pedidos = Pedido.query.all()
    result = []

    for pedido in pedidos:
        menu_item = Menu.query.get(pedido.id_menu)
        agregados = Agregado.query.filter_by(id_menu=pedido.id_menu).all()
        
        pedido_data = {
            "id": pedido.id,
            "id_mesa": pedido.id_mesa,
            "cantidad": pedido.cantidad,
            "solicitado": pedido.solicitado,
            "entregado": pedido.entregado,
            "hentrega": pedido.hentrega,
            "producto": menu_schema.dump(menu_item),
            "agregados": agregado_schema.dump(agregados)
        }
        
        result.append(pedido_data)
    
    return jsonify(result), 200

@pedido_bp.route('/pedidos/<int:id>', methods=['GET'])
def get_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    
    menu_item = Menu.query.get(pedido.id_menu)
    agregados = Agregado.query.filter_by(id_menu=pedido.id_menu).all()

    pedido_data = {
        "id": pedido.id,
        "id_mesa": pedido.id_mesa,
        "cantidad": pedido.cantidad,
        "solicitado": pedido.solicitado,
        "entregado": pedido.entregado,
        "hentrega": pedido.hentrega,
        "producto": menu_schema.dump(menu_item),
        "agregados": agregado_schema.dump(agregados)
    }
    
    return jsonify(pedido_data), 200

@pedido_bp.route('/pedidos/<int:id>/entregar', methods=['PUT'])
@login_required
@check_permissions(1)
def marcar_entregado(id):
    pedido = Pedido.query.get_or_404(id)

    if pedido.entregado:
        return jsonify({"message": "El pedido ya ha sido entregado"}), 400

    timezone = pytz.timezone('America/Argentina/Buenos_Aires')  # Cambia esto según la zona horaria deseada
    local_time = datetime.now(timezone)

    pedido.entregado = True
    pedido.hentrega = local_time

    db.session.commit()

    return jsonify({
        "message": "Pedido marcado como entregado", 
        "pedido": {
            "id": pedido.id,
            "entregado": pedido.entregado,
            "hentrega": pedido.hentrega
        }
    }), 200

def actualizar_pedido(pedido, data):
    
    pedido.id_menu = data.get('id_menu', pedido.id_menu)
    pedido.cantidad = data.get('cantidad', pedido.cantidad)

    nuevos_agregados = data.get('agregados', [])
    
    if nuevos_agregados is not None:

        agregados_actuales = Agregado.query.filter_by(id_menu=pedido.id_menu).all()

        ids_agregados_actuales = {agregado.id for agregado in agregados_actuales}
        ids_nuevos_agregados = set(nuevos_agregados)

        agregados_a_eliminar = ids_agregados_actuales - ids_nuevos_agregados
        for id_agregado in agregados_a_eliminar:
            agregado = Agregado.query.get(id_agregado)
            db.session.delete(agregado)

        for id_agregado in ids_nuevos_agregados - ids_agregados_actuales:
            nuevo_agregado = Agregado.query.get(id_agregado)
            if nuevo_agregado:
                
                nuevo_agregado.id_menu = pedido.id_menu
                db.session.add(nuevo_agregado)

    db.session.commit()

    return {
        "id": pedido.id,
        "id_menu": pedido.id_menu,
        "agregados": nuevos_agregados,
        "cantidad": pedido.cantidad,
        "solicitado": pedido.solicitado,
        "entregado": pedido.entregado,
        "hentrega": pedido.hentrega
    }

@pedido_bp.route('/pedidos/<int:id>/corregir', methods=['PUT'])
@login_required
@check_permissions(2)
def corregir_pedido(id):
    pedido = Pedido.query.get_or_404(id)

    timezone = pytz.timezone('America/Argentina/Buenos_Aires')  # Cambia según la zona horaria deseada
    current_time = datetime.now(timezone)

    tiempo_solicitado = pedido.solicitado.astimezone(timezone)
    tiempo_limite = tiempo_solicitado + timedelta(minutes=3)

    if current_time > tiempo_limite:
        return jsonify({"message": "El tiempo para corregir el pedido ha expirado"}), 403

    if pedido.entregado:
        return jsonify({"message": "No se puede corregir un pedido que ya ha sido entregado"}), 400

    data = request.get_json()

    pedido_actualizado = actualizar_pedido(pedido, data)

    return jsonify({
        "message": "Pedido corregido con éxito",
        "pedido": pedido_actualizado
    }), 200

@pedido_bp.route('/pedidos/<int:id>/corregir-forzado', methods=['PUT'])
@login_required
@check_permissions(2)
def corregir_pedido_forzado(id):
    pedido = Pedido.query.get_or_404(id)

    if pedido.entregado:
        return jsonify({"message": "No se puede corregir un pedido que ya ha sido entregado"}), 400

    data = request.get_json()

    pedido_actualizado = actualizar_pedido(pedido, data)

    return jsonify({
        "message": "Pedido corregido con éxito (sin restricción de tiempo)",
        "pedido": pedido_actualizado
    }), 200

@pedido_bp.route('/pedidos/<int:id>', methods=['DELETE'])
@login_required
@check_permissions(1)
def delete_pedido(id):
    pedido = Pedido.query.get_or_404(id)

    timezone = pytz.timezone('America/Argentina/Buenos_Aires')  # Ajusta según la zona horaria
    current_time = datetime.now(timezone)

    tiempo_solicitado = pedido.solicitado.astimezone(timezone)
    tiempo_limite = tiempo_solicitado + timedelta(minutes=3)

    if current_time > tiempo_limite:
        return jsonify({"message": "No se puede eliminar el pedido después de 3 minutos"}), 403

    if pedido.entregado:
        return jsonify({"message": "No se puede eliminar un pedido que ya ha sido entregado"}), 400

    db.session.delete(pedido)
    db.session.commit()

    return jsonify({"message": "Pedido eliminado con éxito"}), 200

@pedido_bp.route('/pedidos/<int:id>/forzar-eliminar', methods=['DELETE'])
@login_required
@check_permissions(2)
def force_delete_pedido(id):
    pedido = Pedido.query.get_or_404(id)

    if pedido.entregado:
        return jsonify({"message": "No se puede eliminar un pedido que ya ha sido entregado"}), 400

    db.session.delete(pedido)
    db.session.commit()

    return jsonify({"message": "Pedido eliminado con éxito, sin restricción de tiempo"}), 200

