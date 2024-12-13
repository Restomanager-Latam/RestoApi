from marshmallow import Schema, fields
from datetime import datetime

class PedidoSchema(Schema):
    id = fields.Int(dump_only=True)
    id_mesa = fields.Int(required=True)
    id_menu = fields.Int(required=True)
    id_agregado = fields.Int(allow_none=True)
    cantidad = fields.Int(required=True)
    solicitado = fields.DateTime(dump_only=True, format='%Y-%m-%d %H:%M:%S')
    entregado = fields.Bool(default=False)
    hentrega = fields.DateTime(allow_none=True, format='%Y-%m-%d %H:%M:%S')
    menu = fields.Nested('MenuSchema', only=['id', 'producto'])
    agregado = fields.Nested('AgregadoSchema', only=['id', 'nombre'])
