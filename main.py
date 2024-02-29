from flask import Flask, jsonify, request
from flask_smorest import abort
from db import stores, items
import uuid

app = Flask(__name__)

@app.get('/')
def index():
    return {
        'message': 'it works'
    }

@app.get('/store/<string:store_id>')
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        # abort(404, message='store not found')
        return {'message': 'store not found'}, 404
    
@app.get('/store')
def get_stores():
    return {'stores': list(stores.values())}

@app.post('/store')
def create_store():

    store_data = request.get_json()

    if 'name' not in store_data:
        return {'message': "'name' should be included in json payload"}, 400
    
    for store in stores.values():
        if store['name'] == store_data['name']:
            # abort(400, message=f'store already exits')
            return {'message': 'store already exists'}, 400

    store_id = uuid.uuid4().hex
    store = {**store_data, 'id': store_id}
    stores[store_id] = store

    return store, 201

@app.post('/item')
def create_item():

    item_data = request.get_json()

    if (
        'price' not in item_data
        or 'store_id' not in item_data
        or 'name' not in item_data
    ):
        return {'message': 'price, store_id and name should be included'}, 400

    if item_data['store_id'] not in stores:
        # abort(404, message='store not found')
        return {'message': 'store not found'}, 404
    
    item_id = uuid.uuid4().hex
    item = {**item_data, 'id': item_id}
    items[item_id] = item
    
    return item, 201

@app.get('/item')
def get_all_items():
    return {'items': list(items.values())}

@app.get('/item/<string:item_id>')
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        # abort(404, message='item not found')
        return {'message': 'item not found'}, 404

if __name__ == '__main__':
    app.run(debug=True)