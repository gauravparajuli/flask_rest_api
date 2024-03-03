from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import stores
from db import db
from models import StoreModel
from resources.schemas import StoreSchema

blp = Blueprint('Stores', __name__, description='Operation on stores')

@blp.route('/store/<string:store_id>')
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get(store_id)
        if store:
            db.session.delete(store)
            db.session.commit()

            return {}, 204

        abort(404, message='store not found')

@blp.route('/store')
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):

        print(store_data)

        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message='store with that name already exists')
        except SQLAlchemyError:
            abort(500, message='error encountered while creating the score')

        return store