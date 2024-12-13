from marshmallow import Schema, fields

class UsuarioRegisterSchema(Schema):
    nombre = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)  
    id_permiso = fields.Int(required=False, missing=None)
