from marshmallow import Schema, fields

class UsuarioSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    email = fields.Str(required=True)
    id_permiso = fields.Int(missing=None)
