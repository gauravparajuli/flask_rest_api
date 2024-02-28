from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        'name': 'my_store',
        'items': [
            {
                'name': 'my item',
                'price': 15.99
            }
        ]
    }
]

@app.route('/')
def index():
    return jsonify({
        'message': 'It works!'
    })

@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return store
    
    return {'error': 'store not found'}, 404

@app.route('/store', methods=['GET', 'POST'])
def store():
    if request.method == 'GET':
        return {'stores': stores}
    
    # post request
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)

    return new_store, 201

@app.route('/store/<string:name>/item', methods=['POST', 'GET'])
def store_item(name):
    if request.method == 'GET':
        for store in stores:
            if store['name'] == name:
                return {'items': store['items']}
            
        return {'error': 'store not found'}, 404

    # post
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }

            store['items'].append(new_item)
            return new_item
        
    return {'error': 'store not found'}, 404

if __name__ == '__main__':
    app.run(debug=True)