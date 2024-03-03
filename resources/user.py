from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, get_jwt, jwt_required

from db import db
from models import UserModel, BLOCKLIST
from resources.schemas import UserSchema

blp = Blueprint('Users', __name__, description='Operations on users')

@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data['username']
        ).first()

        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            access_token = create_access_token(identity=user.id)
            return dict(access_token=access_token)
        
        abort(401, message='invalid credentials')

@blp.route('/register')
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data['username']).first():
            abort(409, message='user with that username already exists')

        user = UserModel(
            username = user_data['username'],
            password = pbkdf2_sha256.hash(user_data['password'])
        )

        db.session.add(user)
        db.session.commit()

        return dict(message='user created successfully'), 201
    

# for development purpose only
@blp.route('/user/<int:user_id>')
class User(MethodView):

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return {}, 204
    
@blp.route('/logout')
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jwt = get_jwt()['jti']
        BLOCKLIST.add(jwt)
        return dict(message='logged out successfully')