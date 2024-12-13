from flask import Blueprint, request, jsonify
from models import db, Llamadas
from datetime import datetime
import pytz
from middleware.auth_middleware import login_required, check_permissions 

mozoCaller_bp = Blueprint('mozoCaller', __name__)

URL_ENDPOINT = '/mozocall'

@mozoCaller_bp.route(URL_ENDPOINT, methods=['GET'])
@login_required
@check_permissions(1)
def get_all_mozoCalls():
    mozoCalls = Llamadas.query.all()
    mozoCalls_data = [
        {
            "id": mozoCall.id,
            "mesa": mozoCall.id_mesa,
            "solicitado": mozoCall.solicitado,
            "atendido": mozoCall.atendido,
            "hentrega": mozoCall.hentrega,
            "cuenta": mozoCall.cuenta,
            "cobrado": mozoCall.cobrado
        } for mozoCall in mozoCalls
    ]
    return jsonify(mozoCalls_data), 200

@mozoCaller_bp.route(URL_ENDPOINT, methods=['POST'])
def create_mozocall():
    data = request.get_json()

    if isinstance(data, dict):
        data = [data]

    for mozocall_data in data:
        id_mesa = mozocall_data.get('id_mesa')

        if not id_mesa:
            return jsonify({"message": 'Número de mesa inválido'}), 400

        mozoCall = Llamadas.query.filter_by(id_mesa=id_mesa).first()

        if mozoCall:
            if mozoCall.cobrado:
                nuevo_mozoCall = Llamadas(
                    id_mesa=id_mesa,
                    solicitado=datetime.utcnow(),
                    atendido=False,
                    hentrega=None,
                    cuenta=False,
                    cobrado=False
                )
                db.session.add(nuevo_mozoCall)
            elif mozoCall.atendido and not mozoCall.cuenta:
                mozoCall.solicitado = datetime.utcnow()
                mozoCall.atendido = False
            elif not mozoCall.atendido:
                mozoCall.solicitado = mozoCall.solicitado 
            elif mozoCall.cuenta and not mozoCall.cobrado:
                mozoCall.solicitado = datetime.utcnow()
                mozoCall.atendido = False
        else:
            nuevo_mozoCall = Llamadas(
                id_mesa=id_mesa,
                solicitado=datetime.utcnow(),
                atendido=False,
                hentrega=None,
                cuenta=False,
                cobrado=False
            )
            db.session.add(nuevo_mozoCall)

    db.session.commit()

    return jsonify({"message": "El mozo ha sido llamado"}), 201



@mozoCaller_bp.route(URL_ENDPOINT + '/cuenta', methods=['POST'])
def create_or_update_cuenta():
    data = request.get_json()
    id_mesa = data.get('id_mesa')

    if not id_mesa:
        return jsonify({"message": "Número de mesa inválido"}), 400

    mozoCall = Llamadas.query.filter_by(id_mesa=id_mesa, cobrado=False).first()

    if mozoCall:
        if mozoCall.cobrado:
            nueva_cuenta = Llamadas(
                id_mesa=id_mesa,
                solicitado=datetime.utcnow(),
                atendido=False,
                hentrega=None,
                cuenta=True,
                cobrado=False
            )
            db.session.add(nueva_cuenta)
            db.session.commit()
            return jsonify({"message": "Se ha creado un nuevo registro porque la cuenta ya ha sido cobrada"}), 201

        if mozoCall.cuenta:
            return jsonify({"message": "La cuenta ya ha sido solicitada"}), 200

        if mozoCall.atendido and not mozoCall.cuenta:
            actualizar_cuenta(id_mesa)
            return jsonify({"message": "Se ha actualizado el estado de la cuenta a solicitado."}), 200

        mozoCall.cuenta = True
        db.session.commit()
        return jsonify({"message": "Se ha actualizado el estado de la cuenta a solicitado."}), 200

    nueva_cuenta = Llamadas(
        id_mesa=id_mesa,
        solicitado=datetime.utcnow(),
        atendido=False,
        hentrega=None,
        cuenta=True,
        cobrado=False
    )
    db.session.add(nueva_cuenta)
    db.session.commit()

    return jsonify({"message": "Se ha creado un nuevo registro para el número de mesa proporcionado"}), 201

def actualizar_cuenta(id_mesa):
    mozoCall = Llamadas.query.filter_by(id_mesa=id_mesa).first()
    if mozoCall:
        mozoCall.cuenta = True
        db.session.commit()
        return True
    return False

def actualizar_pedido(id_mesa):
    mozoCall = Llamadas.query.filter_by(id_mesa=id_mesa, cobrado=False).first()
    if mozoCall:
        mozoCall.solicitado = datetime.utcnow()
        mozoCall.atendido = False
        db.session.commit()
        return True
    return False



@mozoCaller_bp.route(URL_ENDPOINT + '/<int:id>', methods=['GET'])
@login_required
@check_permissions(1)
def get_mozoCall(id):
    mozoCall = Llamadas.query.get_or_404(id)

    mozoCall_data = {
        "id": mozoCall.id,
        "mesa": mozoCall.id_mesa,
        "solicitado": mozoCall.solicitado,
        "atendido": mozoCall.atendido,
        "hentrega": mozoCall.hentrega,
        "cuenta": mozoCall.cuenta,
        "cobrado": mozoCall.cobrado
    }
    
    return jsonify(mozoCall_data), 200

@mozoCaller_bp.route(URL_ENDPOINT + '/<int:id>/entregar', methods=['PUT'])
@login_required
@check_permissions(1)
def marcar_atendido(id):
    mozoCall = Llamadas.query.get_or_404(id)

    if mozoCall.atendido:
        return jsonify({"message": "El mozo ya atendió esta mesa"}), 400

    timezone = pytz.timezone('America/Argentina/Buenos_Aires')
    local_time = datetime.now(timezone)

    mozoCall.atendido = True
    mozoCall.hentrega = local_time

    db.session.commit()

    return jsonify({
        "message": "MozoCall marcado como atendido",
        "mozoCall": {
            "id": mozoCall.id,
            "mesa": mozoCall.id_mesa,
            "atendido": mozoCall.atendido,
            "hentrega": mozoCall.hentrega
        }
    }), 200

@mozoCaller_bp.route(URL_ENDPOINT + '/<int:id>/cobrar', methods=['PUT'])
@login_required
@check_permissions(1)
def cobrar(id):
    mozoCall = Llamadas.query.get_or_404(id)

    if mozoCall.cuenta:
        if not mozoCall.atendido:
            timezone = pytz.timezone('America/Argentina/Buenos_Aires')
            local_time = datetime.now(timezone)
            mozoCall.atendido = True
            mozoCall.hentrega = local_time

        mozoCall.cobrado = True
        db.session.commit()

        return jsonify({
            "message": "La cuenta ha sido cobrada",
            "mozoCall": {
                "id": mozoCall.id,
                "mesa": mozoCall.id_mesa,
                "atendido": mozoCall.atendido,
                "hentrega": mozoCall.hentrega,
                "cuenta": mozoCall.cuenta,
                "cobrado": mozoCall.cobrado
            }
        }), 200

    return jsonify({"message": "La cuenta no ha sido solicitada"}), 400

@mozoCaller_bp.route(URL_ENDPOINT + '/<int:id>', methods=['DELETE'])
@login_required
@check_permissions(1)
def delete_mozoCall(id):
    mozoCall = Llamadas.query.get_or_404(id)

    db.session.delete(mozoCall)
    db.session.commit()

    return jsonify({"message": "MozoCall eliminado con éxito"}), 200
