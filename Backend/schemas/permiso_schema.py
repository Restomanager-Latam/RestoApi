from marshmallow import Schema, fields

class PermisoSchema(Schema):
    id = fields.Int(dump_only=True)
    nivel = fields.Int(required=True)
    descripcion = fields.Str()
