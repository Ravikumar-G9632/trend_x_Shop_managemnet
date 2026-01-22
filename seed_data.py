"""
Seed script to populate Trend_X shop database with sample data
"""

from pymongo import MongoClient
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB Connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client['trend_x_shop']

# Clear existing data
db.products.delete_many({})
db.customers.delete_many({})
db.orders.delete_many({})

print("Cleared existing data...")

# Sample Data
CATEGORIES = ['T-Shirts', 'Jeans', 'Dresses', 'Jackets', 'Hoodies', 'Accessories']
SIZES = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
COLORS = ['Black', 'White', 'Blue', 'Red', 'Green', 'Yellow', 'Purple', 'Pink', 'Gray', 'Navy']
FIRST_NAMES = ['John', 'Emma', 'Michael', 'Sarah', 'James', 'Jessica', 'David', 'Laura', 'Robert', 'Maria',
               'William', 'Lisa', 'Richard', 'Karen', 'Joseph', 'Nancy', 'Thomas', 'Betty', 'Charles', 'Sandra',
               'Christopher', 'Ashley', 'Daniel', 'Katherine', 'Matthew', 'Brenda', 'Mark', 'Donna', 'Donald', 'Carol']
LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
              'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']
CITIES = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
PAYMENT_METHODS = ['Cash', 'Card', 'Online', 'Check']
STATUSES = ['Pending', 'Processing', 'Completed', 'Shipped']

PRODUCT_NAMES = {
    'T-Shirts': ['Classic Cotton Tee', 'Premium Blend T-Shirt', 'Graphic Print Tee', 'V-Neck T-Shirt', 'Pocket T-Shirt',
                 'Striped T-Shirt', 'Oversized Tee', 'Fitted T-Shirt', 'Long Sleeve Tee', 'Athletic T-Shirt'],
    'Jeans': ['Classic Blue Jeans', 'Slim Fit Denim', 'Skinny Jeans', 'Bootcut Jeans', 'Straight Leg Jeans',
              'Distressed Jeans', 'Black Jeans', 'White Denim', 'Ripped Jeans', 'Flare Jeans'],
    'Dresses': ['Summer Dress', 'Cocktail Dress', 'Evening Gown', 'Casual Day Dress', 'Party Dress',
                'Maxi Dress', 'Mini Dress', 'Midi Dress', 'Bodycon Dress', 'Sundress'],
    'Jackets': ['Leather Jacket', 'Denim Jacket', 'Bomber Jacket', 'Sports Jacket', 'Winter Coat',
                'Blazer', 'Rain Jacket', 'Wool Jacket', 'Suede Jacket', 'Puffer Jacket'],
    'Hoodies': ['Classic Hoodie', 'Zip Hoodie', 'Pullover Hoodie', 'Oversized Hoodie', 'Sports Hoodie',
                'Fleece Hoodie', 'Lightweight Hoodie', 'Graphic Hoodie', 'Solid Hoodie', 'Tech Hoodie'],
    'Accessories': ['Baseball Cap', 'Beanie', 'Scarf', 'Belt', 'Sunglasses', 'Watch', 'Backpack', 'Socks', 'Gloves', 'Hat']
}

# Generate Products (50-60)
print("\n🛍️ Generating 55 products...")
products = []
product_ids = []

for i in range(55):
    category = random.choice(CATEGORIES)
    product_name = random.choice(PRODUCT_NAMES[category])
    
    product = {
        'name': f"{product_name} #{i+1}",
        'category': category,
        'price': round(random.uniform(15, 150), 2),
        'quantity': random.randint(5, 50),
        'description': f"High-quality {category.lower()} item perfect for everyday wear.",
        'size': random.choice(SIZES),
        'color': random.choice(COLORS),
        'created_at': datetime.now() - timedelta(days=random.randint(0, 90))
    }
    products.append(product)

result = db.products.insert_many(products)
product_ids = result.inserted_ids
print(f"✅ Added {len(products)} products")

# Generate Customers (50-60)
print("\n👥 Generating 58 customers...")
customers = []
customer_names = []

for i in range(58):
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    full_name = f"{first_name} {last_name}"
    customer_names.append(full_name)
    
    customer = {
        'name': full_name,
        'phone': f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
        'email': f"{first_name.lower()}.{last_name.lower()}{i}@email.com",
        'address': f"{random.randint(1, 999)} Main St, {random.choice(CITIES)}",
        'created_at': datetime.now() - timedelta(days=random.randint(0, 180))
    }
    customers.append(customer)

result = db.customers.insert_many(customers)
print(f"✅ Added {len(customers)} customers")

# Generate Orders (50-60)
print("\n📦 Generating 52 orders...")
orders = []

for i in range(52):
    num_items = random.randint(1, 5)
    items = []
    total_price = 0
    
    for _ in range(num_items):
        selected_product = random.choice(products)
        quantity = random.randint(1, 3)
        item_total = selected_product['price'] * quantity
        items.append(f"{selected_product['name']} (Qty: {quantity}, ${item_total:.2f})")
        total_price += item_total
    
    order = {
        'customer_name': random.choice(customer_names),
        'items': items,
        'total_price': round(total_price, 2),
        'status': random.choice(STATUSES),
        'payment_method': random.choice(PAYMENT_METHODS),
        'created_at': datetime.now() - timedelta(days=random.randint(0, 60))
    }
    orders.append(order)

result = db.orders.insert_many(orders)
print(f"✅ Added {len(orders)} orders")

# Print Statistics
print("\n" + "="*50)
print("📊 DATABASE STATISTICS")
print("="*50)
print(f"Total Products:  {db.products.count_documents({})}")
print(f"Total Customers: {db.customers.count_documents({})}")
print(f"Total Orders:    {db.orders.count_documents({})}")

# Calculate Revenue
total_revenue = sum(order['total_price'] for order in db.orders.find({}))
print(f"Total Revenue:   ${total_revenue:.2f}")

# Calculate Inventory Value
inventory_value = sum(product['quantity'] * product['price'] for product in db.products.find({}))
print(f"Inventory Value: ${inventory_value:.2f}")

print("="*50)
print("✅ Database seeded successfully!")
print("🌐 Visit http://localhost:5000 to see the data")
print("="*50)
