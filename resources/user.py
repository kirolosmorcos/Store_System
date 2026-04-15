from flask import Flask,request

from flask.views import MethodView
from flask_smorest import Blueprint,abort
from schema import UserSchema

from models import UserModel

from db import db
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

from passlib.hash import pbkdf2_sha256

from flask_jwt_extended import create_access_token,create_refresh_token,get_jwt_identity

from flask_jwt_extended import jwt_required,get_jwt

from blocklist import BLOCKLIST

blp= Blueprint("users",__name__,description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201,UserSchema)
    def post(self,user_data):
        user=UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )

        try:
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError:
            abort(400, message=f"user already exist")
        except SQLAlchemyError:
            abort(400,message="Failed with registering user")




@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post (self ,user_data):
        user=UserModel.query.filter(UserModel.username==user_data["username"]).first()

        if user and pbkdf2_sha256.verify(user_data["password"],user.password):
            access_token=create_access_token(identity=str(user.id),fresh=True)
            refresh_token=create_refresh_token(identity=str(user.id))
            return {"access_token":access_token,
                    "refresh_token":refresh_token
                    }
        else:
            abort(400,message="Error while logging in")


@blp.route("/refresh")
class UserRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        new_token=create_access_token(identity=get_jwt_identity(),fresh=False)
        jti=get_jwt()['jti']
        BLOCKLIST.add(jti)

        return {"access_token":new_token}


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post (self):
        jti=get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message":"logged out "}




@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200,UserSchema)
    def get(self,user_id):
        user=UserModel.query.get_or_404(user_id)
        return user
    
    @blp.response(202,
                  description="deleted if it is not linked to item",
                  example={"message":"user is deleted"}
                  )
    def delete(self,user_id):
        user=UserModel.query.get_or_404(user_id)

    
        db.session.delete(user)
        db.session.commit()
        return {"message":"user is deleted"}
       