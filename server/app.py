from flask import Flask, request, make_response, jsonify
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# ---- YOUR ROUTES HERE ---- #

# POST /baked_goods - Create a new baked good
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    # Accept both form data and JSON
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
    
    new_baked_good = BakedGood(
        name=data.get('name'),
        price=data.get('price'),
        bakery_id=data.get('bakery_id')
    )
    
    db.session.add(new_baked_good)
    db.session.commit()
    
    return jsonify({
        'id': new_baked_good.id,
        'name': new_baked_good.name,
        'price': new_baked_good.price,
        'bakery_id': new_baked_good.bakery_id
    }), 201

# PATCH /bakeries/<int:id> - Update an existing bakery
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get_or_404(id)
    # Accept both form data and JSON
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
    
    if 'name' in data:
        bakery.name = data['name']
    
    db.session.commit()
    
    return jsonify({
        'id': bakery.id,
        'name': bakery.name,
        'created_at': bakery.created_at,
        'updated_at': bakery.updated_at
    }), 200

# DELETE /baked_goods/<int:id> - Delete a baked good
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get_or_404(id)
    
    db.session.delete(baked_good)
    db.session.commit()
    
    return jsonify({
        'message': 'Baked good deleted successfully'
    }), 200

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(port=5555, debug=True)
