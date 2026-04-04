from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class Database:
    """
    MongoDB database connection manager
    """
    client: AsyncIOMotorClient = None
    
    @classmethod
    async def connect_db(cls):
        """Initialize database connection"""
        cls.client = AsyncIOMotorClient(settings.MONGODB_URL)
        print(f"✅ Connected to MongoDB at {settings.MONGODB_URL}")
    
    @classmethod
    async def close_db(cls):
        """Close database connection"""
        if cls.client:
            cls.client.close()
            print("❌ Closed MongoDB connection")
    
    @classmethod
    def get_database(cls):
        """Get database instance"""
        return cls.client[settings.DATABASE_NAME]
    
    @classmethod
    def get_collection(cls, collection_name: str):
        """Get specific collection"""
        db = cls.get_database()
        return db[collection_name]

# Convenience functions
def get_doctors_collection():
    """Get doctors collection"""
    return Database.get_collection("doctors")

def get_patients_collection():
    """Get patients collection"""
    return Database.get_collection("patients")

def get_assignments_collection():
    """Get assignments collection"""
    return Database.get_collection("assignments")

def get_chatbot_collection():
    """Get chatbot history collection"""
    return Database.get_collection("chatbot_history")
