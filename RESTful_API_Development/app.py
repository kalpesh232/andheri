from flask import Flask, jsonify, request

app = Flask(__name__)

items = []

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify({'items': items})

@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    new_item = {'name': data['name']}
    items.append(new_item)
    return jsonify(new_item), 201

if __name__ == '__main__':
    app.run(debug=True)

     