"""Seed database with sample data"""
import asyncio
from datetime import datetime, timedelta
import random
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import sys
sys.path.append('..')
from app.core.auth import hash_password

MONGODB_URI = "mongodb://localhost:27017"
DB_NAME = "interview_db"

async def seed_data():
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]
    
    # Clear existing data
    await db.users.delete_many({})
    await db.products.delete_many({})
    await db.orders.delete_many({})
    
    # Create users
    admin_result = await db.users.insert_one({
        "email": "admin@example.com",
        "password": hash_password("admin123"),
        "role": "admin",
        "createdAt": datetime.utcnow()
    })
    
    user_result = await db.users.insert_one({
        "email": "user@example.com",
        "password": hash_password("user123"),
        "role": "user",
        "createdAt": datetime.utcnow()
    })
    
    print(f"✓ Created users: admin_id={admin_result.inserted_id}, user_id={user_result.inserted_id}")
    
    # Create products
    products = []
    for i in range(20):
        products.append({
            "name": f"Product {i+1}",
            "description": f"Description for product {i+1}",
            "priceCents": random.randint(1000, 50000),
            "stock": random.randint(10, 100),
            "category": random.choice(["Electronics", "Books", "Apparel", "Home"]),
            "createdAt": datetime.utcnow() - timedelta(days=random.randint(0, 90)),
            "updatedAt": datetime.utcnow()
        })
    
    product_result = await db.products.insert_many(products)
    product_ids = list(product_result.inserted_ids)
    print(f"✓ Created {len(product_ids)} products")
    
    # Create orders
    orders = []
    for i in range(100):
        # Random 1-3 items per order
        num_items = random.randint(1, 3)
        order_items = []
        
        for _ in range(num_items):
            product_id = random.choice(product_ids)
            product = await db.products.find_one({"_id": product_id})
            order_items.append({
                "productId": str(product_id),
                "productName": product["name"],
                "qty": random.randint(1, 3),
                "priceCents": product["priceCents"]
            })
        
        orders.append({
            "userId": str(random.choice([admin_result.inserted_id, user_result.inserted_id])),
            "items": order_items,
            "totalCents": sum(item["qty"] * item["priceCents"] for item in order_items),
            "status": "confirmed",
            "createdAt": datetime.utcnow() - timedelta(days=random.randint(0, 30))
        })
    
    await db.orders.insert_many(orders)
    print(f"✓ Created {len(orders)} orders")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_data())

