from marshmallow import Schema, fields

class AgregadoSchema(Schema):
    id = fields.Int(dump_only=True)
    id_menu = fields.Int(required=True)
    nombre = fields.Str(required=True)
    precio = fields.Float(required=True)
    descripcion = fields.Str()
    menu = fields.Nested('MenuSchema', only=['id', 'producto'])
