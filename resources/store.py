import uuid
from flask import Flask,request

from flask.views import MethodView
from flask_smorest import Blueprint,abort
from schema import StoreSchema

from models import StoreModel
from db import db
from sqlalchemy.exc import IntegrityError,SQLAlchemyError

blp= Blueprint("stores",__name__,description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store (MethodView):
 
    @blp.response(200,StoreSchema)
    def get (self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store 
        # try:
        #     return stores[store_id]
        # except KeyError:
        #     abort(404,message="Store Not found") 
    

    def delete (self,store_id):

        store =StoreModel.query.get_or_404(store_id)

        db.session.delete(store)
        db.session.commit()
        return {"message":"deleted successfully"}
        # try:
        #     del stores[store_id]
        #     return {"message":"deleted successfully"}
        # except KeyError:
        #     abort(404,message="Store Not found") 

@blp.route("/store")
class StoreList (MethodView):

    @blp.response(200,StoreSchema(many=True))
    def get (self) :
        return StoreModel.query.all()
    
        # return stores.values()
    
    @blp.arguments(StoreSchema)
    @blp.response(201,StoreSchema)
    def post(self,store_data):
        store =StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message=f"store already exist")
        except SQLAlchemyError:
            abort(400,message="Failed while inserting store.")



        # request_data=request.get_json()
        # if(
        #     "name" not in request_data
        # ):
        #     abort(
        #         400,
        #         message="Bad Request, incorrect payload"
        #         )
        # for store in stores:
        #     if(store["name"]==request_data["name"]):
        #         abort(400, message=f"store already exist")

        # store_id =uuid.uuid4().hex
        # store ={**request_data,"id":store_id}
        # stores[store_id]=store
        return store,201
