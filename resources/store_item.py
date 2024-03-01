import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint

from resources.schemas import ItemSchema, ItemUpdateSchema

from db import items

blp = Blueprint('Store Items', __name__, description='Operation on store item')

@blp.route('/item')
class StoreItemList(MethodView):

    def get(self):
        return {'items': list(items.values())}

    @blp.arguments(ItemSchema)
    def post(self, item_data):
        # item_data = request.get_json()

        # if (
        #     'price' not in item_data
        #     or 'store_id' not in item_data
        #     or 'name' not in item_data
        # ):
        #     abort(400, message="'name', 'price' and 'store_id' must be included in json payload")

        # check if the given item already exists
        for item in items.values():
            if item_data['name'] == item['name'] and item_data['store_id'] == item['store_id']:
                abort(400, message=f'item already exists')

        item_id = uuid.uuid4().hex
        item = {**item_data, 'id': item_id}
        items[item_id] = item

        return item
    
@blp.route('/item/<string:item_id>')
class StoreItem(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message='item not found')

    @blp.arguments(ItemUpdateSchema)
    def put(self, item_data, item_id):
        # item_data = request.get_json()

        # if 'price' not in item_data or 'name' not in item_data:
        #     abort(400, message="'name' and 'price' must be included in json payload")

        try:
            item = items[item_id]

            item |= item_data # merge two dictionaries

            return item
        except KeyError:
            abort(404, message='item not found')

    def delete(self, item_id):
        try:
            del items[item_id]
            return {}, 204
        except KeyError:
            abort(404, message='item not found')