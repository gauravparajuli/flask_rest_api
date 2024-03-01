import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

blp = Blueprint('stores', __name__, 'operation on stores')

@blp.route('/store/<string:store_id>')
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message='store not found')

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {}, 204
        except KeyError:
            abort(404, message='store not found')