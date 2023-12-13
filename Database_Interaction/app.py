from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'  # SQLite database file
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# Create the database tables
db.create_all()

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify({'items': [{'name': item.name} for item in items]})

@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    new_item = Item(name=data['name'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'name': new_item.name}), 201

if __name__ == '__main__':
    app.run(debug=True)
