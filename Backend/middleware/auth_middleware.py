from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify
from functools import wraps
from models import Usuario

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"message": "Unauthorized"}), 401
        return fn(*args, **kwargs)
    return wrapper

def check_permissions(required_permission):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            current_user = Usuario.query.get(current_user_id)
            
            if not current_user or (current_user.permiso and current_user.permiso.nivel < required_permission):
                return jsonify({"message": "Forbidden"}), 403
                
            return fn(*args, **kwargs)
        return wrapper
    return decorator
