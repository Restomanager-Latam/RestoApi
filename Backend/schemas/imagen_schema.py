from marshmallow import Schema, fields

class ImagenSchema(Schema):
    id = fields.Int(dump_only=True)
    id_menu = fields.Int(required=True)
    url = fields.Str(required=True)
