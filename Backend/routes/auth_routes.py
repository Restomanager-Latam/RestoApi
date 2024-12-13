from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario, Permiso
from marshmallow import ValidationError
from schemas import UsuarioSchema, UsuarioRegisterSchema
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)
usuario_schema = UsuarioSchema()
usuario_register_schema = UsuarioRegisterSchema()

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    id_permiso = data.get('id_permiso')

    if not all([nombre, email, password]):
        return jsonify({'message': 'Missing fields'}), 400

    if id_permiso is not None and not isinstance(id_permiso, int):
        return jsonify({'message': 'Invalid id_permiso'}), 400

   
    existing_user = Usuario.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 400

    user = Usuario(nombre=nombre, email=email, id_permiso=id_permiso)
    user.set_password(password)  

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created'}), 201

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = Usuario.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Credenciales inválidas'}), 401

    token = create_access_token(identity=user.id, expires_delta=timedelta(hours=24))

    return jsonify({'token': token}), 200

@auth_bp.route('/auth/permiso', methods=['GET'])
@jwt_required()
def verificar_permiso():
    current_user_id = get_jwt_identity()
    current_user = Usuario.query.get(current_user_id)
    
    if not current_user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    permiso = Permiso.query.filter_by(id=current_user.id_permiso).first()

    if not permiso:
        return jsonify({'message': 'No se encontraron permisos para este usuario'}), 404

    return jsonify({
        'id_usuario': current_user.id,
        'permiso': permiso.descripcion,
        'nivel': permiso.nivel
    }), 200

@auth_bp.route('/auth/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    user = Usuario.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'Usuario eliminado con éxito'}), 200

@auth_bp.route('/auth/users', methods=['GET'])
@jwt_required()
def get_users():
    users = Usuario.query.all()
    return jsonify([{
        'id': user.id,
        'nombre': user.nombre,
        'email': user.email,
        'id_permiso': user.id_permiso
    } for user in users]), 200
