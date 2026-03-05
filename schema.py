from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    id = fields.Str(dump_default=True)
    name=fields.Str(required=True)
    price=fields.Str(required=True)

class PlainStoreSchema(Schema):
    id= fields.Str(dump_only=True)
    name =fields.Str(required=True)

class ItemSchema(PlainItemSchema):
   
    store_id = fields.Int(required=True,load_only=True) # i dont want it to be returned 
    store = fields.Nested(PlainStoreSchema(),dump_only=True)


class ItemUpdateSchema(Schema):
    name =fields.Str()
    price = fields.Str()

class StoreSchema(PlainStoreSchema):
    items = fields.List( fields.Nested(PlainItemSchema()),dump_only=True)

   
