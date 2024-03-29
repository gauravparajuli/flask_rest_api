from flask import Flask, request
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from db import db
import os
import models

from resources.store import blp as StoreBlueprint
from resources.store_item import blp as StoreItemBlueprint
from resources.tag import blp as TagBluePrint
from resources.user import blp as UserBluePrint

def create_app(db_url:str=None):
    app = Flask(__name__)

    # we will setup app config
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv('DATABASE_URI', 'sqlite:///data.db')
    app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'keygoeshere')

    jwt = JWTManager(app)

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return dict(message='this token is not fresh', error='fresh token required'), 401

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in models.BLOCKLIST

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return dict(is_admin=True)
        
        return dict(is_admin=False)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return dict(message='token has expired', error='token expired'), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return dict(message='signature verification failed', error='invalid token'), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return dict(message='request doesnot contain an access token', error='authorization required'), 401

    db.init_app(app)
    
    migrate = Migrate(app, db)

    api = Api(app)

    # # since we will be using flask-migrate, we donot need to tell flask-sqlachemy to create tables
    # with app.app_context():
    #     db.create_all()

    # register all the blueprints here
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(StoreItemBlueprint)
    api.register_blueprint(TagBluePrint)
    api.register_blueprint(UserBluePrint)

    return app

# @app.get('/')
# def index():
#     return {
#         'message': 'it works'
#     }

# @app.get('/store/<string:store_id>')
# def get_store(store_id):
#     try:
#         return stores[store_id]
#     except KeyError:
#         # abort(404, message='store not found')
#         return {'message': 'store not found'}, 404
    
# @app.get('/store')
# def get_stores():
#     return {'stores': list(stores.values())}

# @app.post('/store')
# def create_store():

#     store_data = request.get_json()

#     if 'name' not in store_data:
#         return {'message': "'name' should be included in json payload"}, 400
    
#     for store in stores.values():
#         if store['name'] == store_data['name']:
#             # abort(400, message=f'store already exits')
#             return {'message': 'store already exists'}, 400

#     store_id = uuid.uuid4().hex
#     store = {**store_data, 'id': store_id}
#     stores[store_id] = store

#     return store, 201

# @app.post('/item')
# def create_item():

#     item_data = request.get_json()

#     if (
#         'price' not in item_data
#         or 'store_id' not in item_data
#         or 'name' not in item_data
#     ):
#         return {'message': 'price, store_id and name should be included'}, 400

#     if item_data['store_id'] not in stores:
#         # abort(404, message='store not found')
#         return {'message': 'store not found'}, 404
    
#     item_id = uuid.uuid4().hex
#     item = {**item_data, 'id': item_id}
#     items[item_id] = item
    
#     return item, 201

# @app.get('/item')
# def get_all_items():
#     print(items)
#     return {'items': list(items.values())}

# @app.delete('/item/<string:item_id>')
# def delete_item(item_id):
#     try:
#         del items[item_id]
#         return {'message': 'deleted'}, 204
#     except KeyError:
#         return {'message': 'item not found'}, 404

# @app.get('/item/<string:item_id>')
# def get_item(item_id):
#     try:
#         return items[item_id]
#     except KeyError:
#         # abort(404, message='item not found')
#         return {'message': 'item not found'}, 404
    
# @app.put('/item/<string:item_id>')
# def update_item(item_id):
#     item_data = request.get_json()

#     if (
#         'price' not in item_data
#         or 'name' not in item_data
#     ):
#         return {
#             'mesage': "'price' and 'name' must be included in json payload"
#         }, 400
#     try:
#         item = items[item_id]
#         item |= item_data

#         return item
    
#     except KeyError:
#         # abort(404, message='item not found')
#         return {'message': 'item not found'}, 404
    
# @app.delete('/store/<string:store_id>')
# def delete_store(store_id):
#     try:
#         del stores[store_id]
#         return {}, 204
#     except KeyError:
#         return dict(message='store not found'), 404

# if __name__ == '__main__':
#     app.run(debug=True)