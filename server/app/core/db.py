from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis
from .config import settings

client = AsyncIOMotorClient(settings.MONGODB_URI)
db = client[settings.DB_NAME]

# Redis client for caching
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

# EXPECTATION: Use Redis for caching /stats/top endpoint.
# Invalidate cache on product/order writes.

async def init_db():
    """Initialize database indexes"""
    # Users
    await db.users.create_index([("email", 1)], unique=True)
    await db.users.create_index([("role", 1)])
    
    # Products
    await db.products.create_index([("category", 1)])
    await db.products.create_index([("createdAt", -1)])
    
    # Orders
    await db.orders.create_index([("userId", 1)])
    await db.orders.create_index([("createdAt", -1)])
    
    print("✓ Database indexes created")

async def invalidate_stats_cache():
    """Invalidate cached statistics"""
    await redis_client.delete("stats:top_products")
    print("✓ Stats cache invalidated")

