from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        'name': 'My Store',
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

@app.route('/store', methods=['GET', 'POST'])
def store():
    if request.method == 'GET':
        return jsonify(stores=stores)
    
    # post request
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)

    return new_store, 201


if __name__ == '__main__':
    app.run(debug=True)