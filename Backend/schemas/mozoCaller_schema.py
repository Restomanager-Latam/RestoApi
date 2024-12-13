from marshmallow import Schema, fields

class MozoCallerSchema(Schema):
    id = fields.Int(dump_only=True)
    id_mesa = fields.Int(required=True)
    solicitado = fields.DateTime(dump_only=True, format='%Y-%m-%d %H:%M:%S')
    atendido = fields.Bool(default=False)
    hentrega = fields.DateTime(allow_none=True, format='%Y-%m-%d %H:%M:%S')
    cuenta = fields.Bool(default=False)
    cobrado = fields.Bool(default=False)
