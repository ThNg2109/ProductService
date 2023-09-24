from flask import Flask, jsonify, request
app = Flask(__name__)


# # Product Model
# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     price = db.Column(db.Float)
#     quantity = db.Column(db.Integer, default = 0)

# Sample Product Data 
products = [
    {"id": 1, "name": "Iphone8", "price": "199.99", "quantity": 5},
    {"id": 2, "name": "Iphone9", "price": "119.99", "quantity": 10},
    {"id": 3, "name": "Iphone10", "price": "99.99", "quantity": 20},
    {"id": 4, "name": "Iphone11", "price": "1199.00", "quantity": 30},
    {"id": 5, "name": "Iphone12", "price": "1009.99", "quantity": 40},
    {"id": 6, "name": "Iphone13", "price": "1119.99", "quantity": 50}    
]

# Endpoint 1: Get all products
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify({"products": products})

# Endpoint 2: Get a specific product by ID 
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((product for product in products if product["id"] == product_id), None)
    if product:
        return jsonify({"product": product})
    else:
        return jsonify({"error": "Product not found"}), 404

# Endpoint 3: Add a new product
@app.route('/products', methods=['POST'])
def create_product():
    new_product = {
        "id": len(products) + 1,
        "name": request.json.get('name'),
        "price": request.json.get('price'),
        "quantity": request.json.get('quantity')
    }
    products.append(new_product)

    return jsonify({"message": "Product added", "Product": new_product}), 201

# Support Endpoint 1: Add quantity to an existing product 
@app.route('/products/add/<int:product_id>', methods=['POST'])
def add_product(product_id):
    update_quantity = request.json.get('quantity')
    product = next((product for product in products if product["id"] == product_id))
    if product:
        quantity = int(product["quantity"]) + int(update_quantity) 
        product["quantity"] = str(quantity)
        return jsonify({"message": "Product inventory changed", "Product": product})
    else:
        return jsonify({"error": "Product not found"}), 404
    
# Support Endpoint 2: Remove quantity to an existing product
@app.route('/products/remove/<int:product_id>', methods=['POST'])
def remove_product(product_id):
    update_quantity = request.json.get('quantity')
    product = next((product for product in products if product["id"] == product_id))
    if product:
        if int(update_quantity) < 0 and int(update_quantity) > int(product["quantity"]):
            return jsonify({"error": "Product quantity is not enough"}), 400
        else:
            quantity = int(product["quantity"]) - int(update_quantity) 
            product["quantity"] = str(quantity)
            return jsonify({"message": "Product inventory changed", "Product": product})
    else:
        return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)
    
