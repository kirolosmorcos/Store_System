from flask import Flask,request

from flask.views import MethodView
from flask_smorest import Blueprint,abort
from schema import TagSchema,TagAndItemSchema

from models import TagModel,StoreModel,ItemTagsModel,ItemModel

from db import db
from sqlalchemy.exc import SQLAlchemyError

blp= Blueprint("tags",__name__,description="Operations on tags")

@blp.route("/store/<string:store_id>/tags")
class TagList(MethodView):
    @blp.response(200,TagSchema(many=True))
    def get(self,store_id):
        store=StoreModel.query.get_or_404(store_id)
        return store.tags.all()
    
    @blp.arguments(TagSchema)
    @blp.response(201,TagSchema)
    def post(self,tag_data,store_id):
        tag=TagModel(**tag_data,store_id =store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return tag
    
@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200,TagSchema)
    def get(self,tag_id):
        tag= TagModel.query.get_or_404(tag_id)
        return tag
    
    @blp.response(202,
                  description="deleted if it is not linked to item",
                  example={"message":"tag deleted"}
                  )
    @blp.alt_response(404,description="tag is not found")
    @blp.alt_response(400,description="tag is linked to item ")
    def delete(self,tag_id):
        tag= TagModel.query.get_or_404(tag_id)
        
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message":"tag deleted"}
        else :
            abort(400,message="tag is linked to item")
    
    
@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagToItem(MethodView):
    @blp.response(201,TagSchema)
    def post(self,item_id,tag_id):
        item=ItemModel.query.get_or_404(item_id)
        tag=TagModel.query.get_or_404(tag_id)
        
        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort (500,message="error while linking tag")
        return tag

    @blp.response(201,TagAndItemSchema)
    def delete(self,item_id,tag_id):
        item=ItemModel.query.get_or_404(item_id)
        tag=TagModel.query.get_or_404(tag_id)
        
        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort (500,message="error while  unlinking tag")

        return{"message":"ulinked successfully","item":item,"tag":tag}
