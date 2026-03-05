import uuid
from flask import Flask,request

from flask.views import MethodView
from flask_smorest import Blueprint,abort
from schema import ItemSchema,ItemUpdateSchema

from models import ItemModel

from db import db
from sqlalchemy.exc import SQLAlchemyError

blp= Blueprint("items",__name__,description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    
    @blp.response(200,ItemSchema)
    def get (self,item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
        # try:
        #     return items[item_id]
        # except KeyError:
        #     abort(404,message="Item Not found")
    
    def delete (self, item_id):
        try:
            del items[item_id]
            return {"message":"deleted successfully"}
        except KeyError:
            abort(404,message="Item Not found")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put (self,item_data,item_id):
       
        try:
            item=items[item_id]
            item|=item_data
            return item
        except KeyError:
            abort(404,message="Item Not found")

@blp.route("/item")
class ItemList(MethodView):
    
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return items.values()  
   
    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self,item_data):

        item=ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()

        except SQLAlchemyError:
            abort(400,message="Failed while inserting item.")

        
       
        # for dictionaries
        # for item in items:
        #     if(
        #         item["name"]==item_data["name"]
        #         and item["store_id"]==item_data["store_id"]
        #     ):
        #         abort(
        #             400,
        #             message=f"item already exist"
        #         )

        # if(item_data["store_id"]not in stores):
        #     abort(404,message="Store Not found")
        
        # item_id =uuid.uuid4().hex
        # item ={**item_data,"id":item_id}
        # items[item_id]=item
        return item,201

            