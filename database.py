"""
MongoDB Database Operations
"""
from pymongo import MongoClient, ASCENDING
from pymongo.errors import PyMongoError
from config import MONGO_URI, DB_NAME
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance
    
    def initialize(self):
        """Initialize MongoDB connection and create indexes"""
        try:
            self.client = MongoClient(MONGO_URI)
            self.db = self.client[DB_NAME]
            self._create_indexes()
            logger.info("✅ MongoDB connected successfully")
        except PyMongoError as e:
            logger.error(f"❌ MongoDB connection error: {e}")
            raise
    
    def _create_indexes(self):
        """Create database indexes for performance"""
        self.db.users.create_index([("user_id", ASCENDING)], unique=True)
        self.db.families.create_index([("user_id", ASCENDING)])
        self.db.friends.create_index([("user_id", ASCENDING)])
        self.db.economy.create_index([("user_id", ASCENDING)])
        self.db.gardens.create_index([("user_id", ASCENDING)])
        self.db.factory.create_index([("user_id", ASCENDING)])
        self.db.market.create_index([("user_id", ASCENDING)])
        logger.info("✅ Database indexes created")
    
    # USER OPERATIONS
    def create_user(self, user_id, username, first_name):
        """Create new user"""
        try:
            user_doc = {
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "money": 500,
                "bank": 0,
                "reputation": 0,
                "partner": None,
                "children": [],
                "parents": [],
                "friends": [],
                "job": None,
                "inventory": {},
                "garden": {"plots": [], "barn": []},
                "factory_workers": [],
                "weapons": [],
                "insurance": 0,
                "level": 1,
                "experience": 0,
                "jail_time": 0,
                "medical_cooldown": 0,
                "created_at": datetime.utcnow(),
                "last_daily": None,
                "last_rob": None,
                "last_kill": None,
                "banned": False,
                "ban_reason": None,
            }
            result = self.db.users.insert_one(user_doc)
            
            # Create family document
            self.db.families.insert_one({
                "user_id": user_id,
                "partner": None,
                "children": [],
                "parents": [],
                "grandparents": [],
                "grandchildren": [],
                "siblings": [],
            })
            
            logger.info(f"✅ User {user_id} created")
            return user_doc
        except Exception as e:
            logger.error(f"❌ Error creating user: {e}")
            return None
    
    def get_user(self, user_id):
        """Get user by ID"""
        return self.db.users.find_one({"user_id": user_id})
    
    def update_user(self, user_id, updates):
        """Update user data"""
        result = self.db.users.update_one({"user_id": user_id}, {"$set": updates})
        return result.modified_count > 0
    
    # FAMILY OPERATIONS
    def get_family(self, user_id):
        """Get user's family"""
        return self.db.families.find_one({"user_id": user_id})
    
    def add_child(self, parent_id, child_id):
        """Add child to family"""
        self.db.families.update_one(
            {"user_id": parent_id},
            {"$addToSet": {"children": child_id}}
        )
        self.db.families.update_one(
            {"user_id": child_id},
            {"$addToSet": {"parents": parent_id}}
        )
        logger.info(f"✅ Child {child_id} added to {parent_id}")
    
    def add_partner(self, user_id, partner_id):
        """Set partner"""
        self.db.families.update_one(
            {"user_id": user_id},
            {"$set": {"partner": partner_id}}
        )
        self.db.families.update_one(
            {"user_id": partner_id},
            {"$set": {"partner": user_id}}
        )
    
    def remove_partner(self, user_id):
        """Divorce/remove partner"""
        family = self.db.families.find_one({"user_id": user_id})
        if family and family.get("partner"):
            partner_id = family["partner"]
            self.db.families.update_one(
                {"user_id": user_id},
                {"$set": {"partner": None}}
            )
            self.db.families.update_one(
                {"user_id": partner_id},
                {"$set": {"partner": None}}
            )
    
    # ECONOMY OPERATIONS
    def add_money(self, user_id, amount):
        """Add money to user"""
        self.db.users.update_one(
            {"user_id": user_id},
            {"$inc": {"money": amount}}
        )
    
    def withdraw_money(self, user_id, amount):
        """Withdraw money from user"""
        user = self.get_user(user_id)
        if user and user["money"] >= amount:
            self.db.users.update_one(
                {"user_id": user_id},
                {"$inc": {"money": -amount}}
            )
            return True
        return False
    
    def add_bank(self, user_id, amount):
        """Add to bank"""
        self.db.users.update_one(
            {"user_id": user_id},
            {"$inc": {"bank": amount, "money": -amount}}
        )
    
    def withdraw_bank(self, user_id, amount):
        """Withdraw from bank"""
        user = self.get_user(user_id)
        if user and user["bank"] >= amount:
            self.db.users.update_one(
                {"user_id": user_id},
                {"$inc": {"bank": -amount, "money": amount}}
            )
            return True
        return False
    
    # INVENTORY OPERATIONS
    def add_item(self, user_id, item_name, quantity=1):
        """Add item to inventory"""
        self.db.users.update_one(
            {"user_id": user_id},
            {"$inc": {f"inventory.{item_name}": quantity}}
        )
    
    def remove_item(self, user_id, item_name, quantity=1):
        """Remove item from inventory"""
        user = self.get_user(user_id)
        if user and user["inventory"].get(item_name, 0) >= quantity:
            self.db.users.update_one(
                {"user_id": user_id},
                {"$inc": {f"inventory.{item_name}": -quantity}}
            )
            return True
        return False
    
    # LEADERBOARD OPERATIONS
    def get_leaderboard(self, field, limit=10):
        """Get top users by field"""
        return list(self.db.users.find(
            {"banned": False},
            {
                "user_id": 1,
                "username": 1,
                "first_name": 1,          # Added this line → अब नाम दिखेगा
                field: 1
            }
        ).sort(field, -1).limit(limit))
    
    def get_user_rank(self, user_id, field):
        """Get user's rank"""
        user = self.get_user(user_id)
        if not user:
            return 0
        rank = self.db.users.count_documents({
            field: {"$gt": user.get(field, 0)},
            "banned": False
        })
        return rank + 1
    
    # UTILITY
    def ban_user(self, user_id, reason):
        """Ban user"""
        self.db.users.update_one(
            {"user_id": user_id},
            {"$set": {"banned": True, "ban_reason": reason}}
        )
    
    def unban_user(self, user_id):
        """Unban user"""
        self.db.users.update_one(
            {"user_id": user_id},
            {"$set": {"banned": False, "ban_reason": None}}
        )

# Singleton instance
db = Database()
