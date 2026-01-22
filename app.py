from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)

# MongoDB Connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client['trend_x_shop']
products_collection = db['products']
orders_collection = db['orders']
customers_collection = db['customers']

@app.route('/')
def home():
    """Render home page"""
    return render_template('index.html')

# ==================== PRODUCTS ENDPOINTS ====================

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    try:
        products = list(products_collection.find({}))
        for product in products:
            product['_id'] = str(product['_id'])
        return jsonify({'success': True, 'products': products})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products', methods=['POST'])
def add_product():
    """Add new product"""
    try:
        data = request.get_json()
        
        if not data.get('name') or not data.get('category') or data.get('price') is None:
            return jsonify({'success': False, 'error': 'Name, category, and price are required'}), 400
        
        product = {
            'name': data['name'],
            'category': data['category'],
            'price': float(data['price']),
            'quantity': int(data.get('quantity', 0)),
            'description': data.get('description', ''),
            'size': data.get('size', ''),
            'color': data.get('color', ''),
            'created_at': datetime.now()
        }
        
        result = products_collection.insert_one(product)
        product['_id'] = str(result.inserted_id)
        
        return jsonify({'success': True, 'product': product}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete product"""
    try:
        result = products_collection.delete_one({'_id': ObjectId(product_id)})
        if result.deleted_count == 0:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
        return jsonify({'success': True, 'message': 'Product deleted'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== CUSTOMERS ENDPOINTS ====================

@app.route('/api/customers', methods=['GET'])
def get_customers():
    """Get all customers"""
    try:
        customers = list(customers_collection.find({}))
        for customer in customers:
            customer['_id'] = str(customer['_id'])
        return jsonify({'success': True, 'customers': customers})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/customers', methods=['POST'])
def add_customer():
    """Add new customer"""
    try:
        data = request.get_json()
        
        if not data.get('name') or not data.get('phone'):
            return jsonify({'success': False, 'error': 'Name and phone are required'}), 400
        
        customer = {
            'name': data['name'],
            'phone': data['phone'],
            'email': data.get('email', ''),
            'address': data.get('address', ''),
            'created_at': datetime.now()
        }
        
        result = customers_collection.insert_one(customer)
        customer['_id'] = str(result.inserted_id)
        
        return jsonify({'success': True, 'customer': customer}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== ORDERS ENDPOINTS ====================

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    try:
        orders = list(orders_collection.find({}).sort('created_at', -1))
        for order in orders:
            order['_id'] = str(order['_id'])
        return jsonify({'success': True, 'orders': orders})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/orders', methods=['POST'])
def add_order():
    """Add new order"""
    try:
        data = request.get_json()
        
        if not data.get('customer_name') or not data.get('items') or not data.get('total_price'):
            return jsonify({'success': False, 'error': 'Customer name, items, and total price are required'}), 400
        
        order = {
            'customer_name': data['customer_name'],
            'items': data['items'],
            'total_price': float(data['total_price']),
            'status': data.get('status', 'Pending'),
            'payment_method': data.get('payment_method', 'Cash'),
            'created_at': datetime.now()
        }
        
        result = orders_collection.insert_one(order)
        order['_id'] = str(result.inserted_id)
        
        return jsonify({'success': True, 'order': order}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/orders/<order_id>', methods=['PUT'])
def update_order_status(order_id):
    """Update order status"""
    try:
        data = request.get_json()
        result = orders_collection.update_one(
            {'_id': ObjectId(order_id)},
            {'$set': {'status': data.get('status', 'Pending')}}
        )
        if result.matched_count == 0:
            return jsonify({'success': False, 'error': 'Order not found'}), 404
        return jsonify({'success': True, 'message': 'Order updated'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== DASHBOARD ENDPOINTS ====================

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    """Get dashboard statistics"""
    try:
        total_products = products_collection.count_documents({})
        total_customers = customers_collection.count_documents({})
        total_orders = orders_collection.count_documents({})
        
        # Calculate total revenue
        orders = list(orders_collection.find({}))
        total_revenue = sum(order.get('total_price', 0) for order in orders)
        
        # Calculate inventory value
        products = list(products_collection.find({}))
        inventory_value = sum(product.get('quantity', 0) * product.get('price', 0) for product in products)
        
        return jsonify({
            'success': True,
            'total_products': total_products,
            'total_customers': total_customers,
            'total_orders': total_orders,
            'total_revenue': round(total_revenue, 2),
            'inventory_value': round(inventory_value, 2)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'success': False, 'error': 'Resource not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'success': False, 'error': 'Server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
