"""
MongoDB Database Operations - Fixed and Enhanced Version
"""
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import PyMongoError, DuplicateKeyError
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
            self.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            self.db = self.client[DB_NAME]
            self._create_indexes()
            logger.info("✅ MongoDB connected successfully")
        except PyMongoError as e:
            logger.error(f"❌ MongoDB connection error: {e}")
            raise
    
    def _create_indexes(self):
        """Create database indexes for performance"""
        try:
            self.db.users.create_index([("user_id", ASCENDING)], unique=True)
            self.db.users.create_index([("username", ASCENDING)])
            self.db.families.create_index([("user_id", ASCENDING)], unique=True)
            self.db.friends.create_index([("user_id", ASCENDING)], unique=True)
            self.db.economy.create_index([("user_id", ASCENDING)], unique=True)
            self.db.gardens.create_index([("user_id", ASCENDING)], unique=True)
            self.db.factory.create_index([("user_id", ASCENDING)], unique=True)
            self.db.market.create_index([("user_id", ASCENDING)])
            self.db.market_items.create_index([("item_id", ASCENDING)], unique=True)
            self.db.auctions.create_index([("auction_id", ASCENDING)], unique=True)
            self.db.games.create_index([("user_id", ASCENDING)], unique=True)
            self.db.crime.create_index([("user_id", ASCENDING)], unique=True)
            logger.info("✅ Database indexes created")
        except Exception as e:
            logger.error(f"❌ Error creating indexes: {e}")
    
    # ============================================================================
    # USER OPERATIONS
    # ============================================================================
    
    def create_user(self, user_id, username=None, first_name=None):
        """Create new user with all required fields"""
        try:
            user_doc = {
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "money": 500,
                "bank": 0,
                "reputation": 0,
                "xp": 0,
                "level": 1,
                "partner": None,
                "children": [],
                "parents": [],
                "friends": [],
                "job": None,
                "inventory": {},
                "weapons": [],
                "insurance": False,
                "insurance_expiry": None,
                "in_jail": False,
                "jail_until": None,
                "banned": False,
                "created_at": datetime.utcnow(),
                "last_daily": None,
                "last_work": None,
                "last_rob": None,
                "last_kill": None,
                "last_medical": None,
                "total_messages": 0,
                "total_commands": 0
            }
            self.db.users.insert_one(user_doc)
            
            # Initialize related collections
            self._init_family(user_id)
            self._init_friends(user_id)
            self._init_economy(user_id)
            self._init_garden(user_id)
            self._init_factory(user_id)
            self._init_crime(user_id)
            
            logger.info(f"✅ User created: {user_id}")
            return True
        except DuplicateKeyError:
            logger.warning(f"User already exists: {user_id}")
            return False
        except Exception as e:
            logger.error(f"❌ Error creating user: {e}")
            return False
    
    def _init_family(self, user_id):
        """Initialize family document"""
        self.db.families.insert_one({
            "user_id": user_id,
            "partner": None,
            "children": [],
            "parents": [],
            "marriage_date": None,
            "adopted_by": None
        })
    
    def _init_friends(self, user_id):
        """Initialize friends document"""
        self.db.friends.insert_one({
            "user_id": user_id,
            "friends": [],
            "friend_requests_sent": [],
            "friend_requests_received": [],
            "blocked": []
        })
    
    def _init_economy(self, user_id):
        """Initialize economy document"""
        self.db.economy.insert_one({
            "user_id": user_id,
            "loan": 0,
            "loan_taken_at": None,
            "loan_interest": 0,
            "total_earned": 500,
            "total_spent": 0,
            "transactions": []
        })
    
    def _init_garden(self, user_id):
        """Initialize garden document"""
        self.db.gardens.insert_one({
            "user_id": user_id,
            "plots": [{"plot_id": i, "crop": None, "planted_at": None, "fertilized": False} for i in range(4)],
            "barn": {},
            "seeds": {},
            "total_harvested": 0
        })
    
    def _init_factory(self, user_id):
        """Initialize factory document"""
        self.db.factory.insert_one({
            "user_id": user_id,
            "level": 1,
            "workers": [],
            "production_queue": [],
            "upgrades": [],
            "total_produced": 0,
            "last_collection": None
        })
    
    def _init_crime(self, user_id):
        """Initialize crime document"""
        self.db.crime.insert_one({
            "user_id": user_id,
            "weapons": [],
            "insurance": False,
            "insurance_expiry": None,
            "in_jail": False,
            "jail_until": None,
            "crimes_committed": 0,
            "times_robbed": 0,
            "times_killed": 0
        })
    
    def get_user(self, user_id):
        """Get user by ID"""
        try:
            return self.db.users.find_one({"user_id": user_id})
        except Exception as e:
            logger.error(f"❌ Error getting user: {e}")
            return None
    
    def get_user_by_username(self, username):
        """Get user by username"""
        try:
            username = username.lstrip('@')
            return self.db.users.find_one({"username": username})
        except Exception as e:
            logger.error(f"❌ Error getting user by username: {e}")
            return None
    
    def update_user(self, user_id, updates):
        """Update user fields"""
        try:
            result = self.db.users.update_one(
                {"user_id": user_id},
                {"$set": updates}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"❌ Error updating user: {e}")
            return False
    
    def add_money(self, user_id, amount):
        """Add money to user's wallet"""
        try:
            self.db.users.update_one(
                {"user_id": user_id},
                {"$inc": {"money": amount, "total_earned": amount}}
            )
            return True
        except Exception as e:
            logger.error(f"❌ Error adding money: {e}")
            return False
    
    def withdraw_money(self, user_id, amount):
        """Remove money from user's wallet"""
        try:
            user = self.get_user(user_id)
            if user and user.get('money', 0) >= amount:
                self.db.users.update_one(
                    {"user_id": user_id},
                    {"$inc": {"money": -amount, "total_spent": amount}}
                )
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Error withdrawing money: {e}")
            return False
    
    def deposit_bank(self, user_id, amount):
        """Deposit money to bank"""
        try:
            user = self.get_user(user_id)
            if user and user.get('money', 0) >= amount:
                self.db.users.update_one(
                    {"user_id": user_id},
                    {"$inc": {"money": -amount, "bank": amount}}
                )
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Error depositing to bank: {e}")
            return False
    
    def withdraw_bank(self, user_id, amount):
        """Withdraw money from bank"""
        try:
            user = self.get_user(user_id)
            if user and user.get('bank', 0) >= amount:
                self.db.users.update_one(
                    {"user_id": user_id},
                    {"$inc": {"bank": -amount, "money": amount}}
                )
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Error withdrawing from bank: {e}")
            return False
    
    def transfer_money(self, from_user_id, to_user_id, amount):
        """Transfer money between users"""
        try:
            if self.withdraw_money(from_user_id, amount):
                self.add_money(to_user_id, amount)
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Error transferring money: {e}")
            return False
    
    def user_exists(self, user_id):
        """Check if user exists"""
        return self.db.users.find_one({"user_id": user_id}) is not None
    
    # ============================================================================
    # FAMILY OPERATIONS
    # ============================================================================
    
    def get_family(self, user_id):
        """Get family information"""
        try:
            return self.db.families.find_one({"user_id": user_id})
        except Exception as e:
            logger.error(f"❌ Error getting family: {e}")
            return None
    
    def marry(self, user1_id, user2_id):
        """Create marriage between two users"""
        try:
            marriage_date = datetime.utcnow()
            self.db.families.update_one(
                {"user_id": user1_id},
                {"$set": {"partner": user2_id, "marriage_date": marriage_date}}
            )
            self.db.families.update_one(
                {"user_id": user2_id},
                {"$set": {"partner": user1_id, "marriage_date": marriage_date}}
            )
            self.db.users.update_one(
                {"user_id": user1_id},
                {"$set": {"partner": user2_id}}
            )
            self.db.users.update_one(
                {"user_id": user2_id},
                {"$set": {"partner": user1_id}}
            )
            return True
        except Exception as e:
            logger.error(f"❌ Error creating marriage: {e}")
            return False
    
    def divorce(self, user_id):
        """End marriage"""
        try:
            family = self.get_family(user_id)
            if family and family.get('partner'):
                partner_id = family['partner']
                self.db.families.update_one(
                    {"user_id": user_id},
                    {"$set": {"partner": None, "marriage_date": None}}
                )
                self.db.families.update_one(
                    {"user_id": partner_id},
                    {"$set": {"partner": None, "marriage_date": None}}
                )
                self.db.users.update_one(
                    {"user_id": user_id},
                    {"$set": {"partner": None}}
                )
                self.db.users.update_one(
                    {"user_id": partner_id},
                    {"$set": {"partner": None}}
                )
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Error processing divorce: {e}")
            return False
    
    def adopt(self, parent_id, child_id):
        """Adopt a child"""
        try:
            self.db.families.update_one(
                {"user_id": parent_id},
                {"$push": {"children": child_id}}
            )
            self.db.families.update_one(
                {"user_id": child_id},
                {"$push": {"parents": parent_id}, "$set": {"adopted_by": parent_id}}
            )
            self.db.users.update_one(
                {"user_id": parent_id},
                {"$push": {"children": child_id}}
            )
            self.db.users.update_one(
                {"user_id": child_id},
                {"$push": {"parents": parent_id}}
            )
            return True
        except Exception as e:
            logger.error(f"❌ Error processing adoption: {e}")
            return False
    
    def disown(self, parent_id, child_id):
        """Disown a child"""
        try:
            self.db.families.update_one(
                {"user_id": parent_id},
                {"$pull": {"children": child_id}}
            )
            self.db.families.update_one(
                {"user_id": child_id},
                {"$pull": {"parents": parent_id}, "$set": {"adopted_by": None}}
            )
            self.db.users.update_one(
                {"user_id": parent_id},
                {"$pull": {"children": child_id}}
            )
            self.db.users.update_one(
                {"user_id": child_id},
                {"$pull": {"parents": parent_id}}
            )
            return True
        except Exception as e:
            logger.error(f"❌ Error disowning child: {e}")
            return False
    
    # ============================================================================
    # FRIENDS OPERATIONS
    # ============================================================================
    
    def get_friends(self, user_id):
        """Get friends information"""
        try:
            return self.db.friends.find_one({"user_id": user_id})
        except Exception as e:
            logger.error(f"❌ Error getting friends: {e}")
            return None
    
    def add_friend(self, user_id, friend_id):
        """Add friend"""
        try:
            self.db.friends.update_one(
                {"user_id": user_id},
                {"$push": {"friends": friend_id}}
            )
            self.db.friends.update_one(
                {"user_id": friend_id},
                {"$push": {"friends": user_id}}
            )
            return True
        except Exception as e:
            logger.error(f"❌ Error adding friend: {e}")
            return False
    
    def remove_friend(self, user_id, friend_id):
        """Remove friend"""
        try:
            self.db.friends.update_one(
                {"user_id": user_id},
                {"$pull": {"friends": friend_id}}
            )
            self.db.friends.update_one(
                {"user_id": friend_id},
                {"$pull": {"friends": user_id}}
            )
            return True
        except Exception as e:
            logger.error(f"❌ Error removing friend: {e}")
            return False
    
    def send_friend_request(self, user_id, target_id):
        """Send friend request"""
        try:
            self.db.friends.update_one(
                {"user_id": user_id},
                {"$push": {"friend_requests_sent": target_id}}
            )
            self.db.friends.update_one(
                {"user_id": target_id},
                {"$push": {"friend_requests_received": user_id}}
            )
            return True
        except Exception as e:
            logger.error(f"❌ Error sending friend request: {e}")
            return False
    
    def cancel_friend_request(self, user_id, target_id):
        """Cancel friend request"""
        try:
            self.db.friends.update_one(
                {"user_id": user_id},
                {"$pull": {"friend_requests_sent": target_id}}
            )
            self.db.friends.update_one(
                {"user_id": target_id},
                {"$pull": {"friend_requests_received": user_id}}
            )
            return True
        except Exception as e:
            logger.error(f"❌ Error canceling friend request: {e}")
            return False
    
    # ============================================================================
    # ECONOMY OPERATIONS
    # ============================================================================
    
    def get_economy(self, user_id):
        """Get economy information"""
        try:
            return self.db.economy.find_one({"user_id": user_id})
        except Exception as e:
            logger.error(f"❌ Error getting economy: {e}")
            return None
    
    def take_loan(self, user_id, amount, interest):
        """Take a loan"""
        try:
            self.db.economy.update_one(
                {"user_id": user_id},
                {"$set": {
                    "loan": amount,
                    "loan_taken_at": datetime.utcnow(),
                    "loan_interest": interest
                }}
            )
            self.add_money(user_id, amount)
            return True
        except Exception as e:
            logger.error(f"❌ Error taking loan: {e}")
            return False
    
    def repay_loan(self, user_id, amount):
        """Repay loan"""
        try:
            economy = self.get_economy(user_id)
            if economy and economy.get('loan', 0) >= amount:
                if self.withdraw_money(user_id, amount):
                    self.db.economy.update_one(
                        {"user_id": user_id},
                        {"$inc": {"loan": -amount}}
                    )
                    return True
            return False
        except Exception as e:
            logger.error(f"❌ Error repaying loan: {e}")
            return False
    
    def add_transaction(self, user_id, transaction_type, amount, description=""):
        """Add transaction record"""
        try:
            transaction = {
                "type": transaction_type,
                "amount": amount,
                "description": description,
                "timestamp": datetime.utcnow()
            }
            self.db.economy.update_one(
                {"user_id": user_id},
                {"$push": {"transactions": {"$each": [transaction], "$slice": -100}}}
            )
            return True
        except Exception as e:
            logger.error(f"❌ Error adding transaction: {e}")
            return False
    
    # ============================================================================
    # GARDEN OPERATIONS
    # ============================================================================
    
    def get_garden(self, user_id):
        """Get garden information"""
        try:
            return self.db.gardens.find_one({"user_id": user_id})
        except Exception as e:
            logger.error(f"❌ Error getting garden: {e}")
            return None
    
    def plant_crop(self, user_id, plot_id, crop, growth_time):
        """Plant a crop"""
        try:
            self.db.gardens.update_one(
                {"user_id": user_id, "plots.plot_id": plot_id},
                {"$set": {
                    "plots.$.crop": crop,
                    "plots.$.planted_at": datetime.utcnow(),
                    "plots.$.growth_time": growth_time,
                    "plots.$.fertilized": False
                }}
            )
            return True
        except Exception as e:
            logger.error(f"❌ Error planting crop: {e}")
            return False
    
    def harvest_crop(self, user_id, plot_id):
        """Harvest a crop"""
        try:
            garden = self.get_garden(user_id)
            if garden:
                for plot in garden.get('plots', []):
                    if plot['plot_id'] == plot_id and plot.get('crop'):
                        crop = plot['crop']
                        # Add to barn
                        self.db.gardens.update_one(
                            {"user_id": user_id},
                            {"$inc": {f"barn.{crop}": 1, "total_harvested": 1}}
                        )
                        # Clear plot
                        self.db.gardens.update_one(
                            {"user_id": user_id, "plots.plot_id": plot_id},
                            {"$set": {
                                "plots.$.crop": None,
                                "plots.$.planted_at": None,
                                "plots.$.growth_time": None,
                                "plots.$.fertilized": False
                            }}
                        )
                        return crop
            return None
        except Exception as e:
            logger.error(f"❌ Error harvesting crop: {e}")
            return None
    
    def fertilize_plot(self, user_id, plot_id):
        """Fertilize a plot"""
        try:
            self.db.gardens.update_one(
                {"user_id": user_id, "plots.plot_id": plot_id},
                {"$set": {"plots.$.fertilized": True}}
            )
            return True
        except Exception as e:
            logger.error(f"❌ Error fertilizing plot: {e}")
            return False
    
    def add_seed(self, user_id, seed_type, quantity=1):
        """Add seeds"""
        try:
            self.db.gardens.update_one(
                {"user_id": user_id},
                {"$inc": {f"seeds.{seed_type}": quantity}}
            )
            return True
        except Exception as e:
            logger.error(f"❌ Error adding seed: {e}")
            return False
    
    def remove_seed(self, user_id, seed_type, quantity=1):
        """Remove seeds"""
        try:
            garden = self.get_garden(user_id)
            if garden and garden.get('seeds', {}).get(seed_type, 0) >= quantity:
                self.db.gardens.update_one(
                    {"user_id": user_id},
                    {"$inc": {f"seeds.{seed_type}": -quantity}}
                )
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Error removing seed: {e}")
            return False
    
    def add_plot(self, user_id):
        """Add new plot to garden"""
        try:
            garden = self.get_garden(user_id)
            if garden:
                new_plot_id = len(garden.get('plots', []))
                self.db.gardens.update_one(
                    {"user_id": user_id},
                    {"$push": {"plots": {
                        "plot_id": new_plot_id,
                        "crop": None,
                        "planted_at": None,
                        "fertilized": False
                    }}}
                )
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Error adding plot: {e}")
            return False
    
    # ============================================================================
    # FACTORY OPERATIONS
    # ============================================================================
    
    def get_factory(self, user_id):
        """Get factory information"""
        try:
            return self.db.factory.find_one({"user_id": user_id})
        except Exception as e:
            logger.error(f"❌ Error getting factory: {e}")
            return None
    
    def hire_worker(self, user_id, worker_type, salary):
        """Hire a worker"""
        try:
            worker = {
                "worker_id": datetime.utcnow().timestamp(),
                "type": worker_type,
                "salary": salary,
                "hired_at": datetime.utcnow(),
                "productivity": 1.0
            }
            self.db.factory.update_one(
                {"user_id": user_id},
                {"$push": {"workers": worker}}
            )
            return True
        except Exception as e:
            logger.error(f"❌ Error hiring worker: {e}")
            return False
    
    def fire_worker(self, user_id, worker_id):
        """Fire a worker"""
        try:
            self.db.factory.update_one(
                {"user_id": user_id},
                {"$pull": {"workers": {"worker_id": worker_id}}}
            )
            return True
        except Exception as e:
            logger.error(f"❌ Error firing worker: {e}")
            return False
    
    def upgrade_factory(self, user_id, upgrade_type, cost):
        """Upgrade factory"""
        try:
            if self.withdraw_money(user_id, cost):
                self.db.factory.update_one(
                    {"user_id": user_id},
                    {"$push": {"upgrades": upgrade_type}, "$inc": {"level": 1}}
                )
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Error upgrading factory: {e}")
            return False
    
    def add_production(self, user_id, item, quantity, time_required):
        """Add item to production queue"""
        try:
            production = {
                "item": item,
                "quantity": quantity,
                "started_at": datetime.utcnow(),
                "completed_at": datetime.utcnow() + timedelta(seconds=time_required),
                "completed": False
            }
            self.db.factory.update_one(
                {"user_id": user_id},
                {"$push": {"production_queue": production}}
            )
            return True
        except Exception as e:
            logger.error(f"❌ Error adding production: {e}")
            return False
    
    # ============================================================================
    # CRIME OPERATIONS
    # ============================================================================
    
    def get_crime(self, user_id):
        """Get crime information"""
        try:
            return self.db.crime.find_one({"user_id": user_id})
        except Exception as e:
            logger.error(f"❌ Error getting crime data: {e}")
            return None
    
    def buy_weapon(self, user_id, weapon, cost):
        """Buy weapon"""
        try:
            if self.withdraw_money(user_id, cost):
                self.db.crime.update_one(
                    {"user_id": user_id},
                    {"$push": {"weapons": weapon}}
                )
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Error buying weapon: {e}")
            return False
    
    def buy_insurance(self, user_id, duration_hours, cost):
        """Buy insurance"""
        try:
            if self.withdraw_money(user_id, cost):
                expiry = datetime.utcnow() + timedelta(hours=duration_hours)
                self.db.crime.update_one(
                    {"user_id": user_id},
                    {"$set": {"insurance": True, "insurance_expiry": expiry}}
                )
                self.db.users.update_one(
                    {"user_id": user_id},
                    {"$set": {"insurance": True, "insurance_expiry": expiry}}
                )
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Error buying insurance: {e}")
            return False
    
    def send_to_jail(self, user_id, duration_minutes):
        """Send user to jail"""
        try:
            jail_until = datetime.utcnow() + timedelta(minutes=duration_minutes)
            self.db.crime.update_one(
                {"user_id": user_id},
                {"$set": {"in_jail": True, "jail_until": jail_until}}
            )
            self.db.users.update_one(
                {"user_id": user_id},
                {"$set": {"in_jail": True, "jail_until": jail_until}}
            )
            return True
        except Exception as e:
            logger.error(f"❌ Error sending to jail: {e}")
            return False
    
    def release_from_jail(self, user_id):
        """Release user from jail"""
        try:
            self.db.crime.update_one(
                {"user_id": user_id},
                {"$set": {"in_jail": False, "jail_until": None}}
            )
            self.db.users.update_one(
                {"user_id": user_id},
                {"$set": {"in_jail": False, "jail_until": None}}
            )
            return True
        except Exception as e:
            logger.error(f"❌ Error releasing from jail: {e}")
            return False
    
    def is_in_jail(self, user_id):
        """Check if user is in jail"""
        try:
            crime = self.get_crime(user_id)
            if crime and crime.get('in_jail'):
                jail_until = crime.get('jail_until')
                if jail_until and jail_until > datetime.utcnow():
                    return True
                else:
                    # Auto-release if time is up
                    self.release_from_jail(user_id)
            return False
        except Exception as e:
            logger.error(f"❌ Error checking jail status: {e}")
            return False
    
    def record_crime(self, user_id, crime_type, target_id=None, success=True):
        """Record a crime"""
        try:
            self.db.crime.update_one(
                {"user_id": user_id},
                {"$inc": {"crimes_committed": 1}}
            )
            if crime_type == 'rob' and target_id:
                self.db.crime.update_one(
                    {"user_id": target_id},
                    {"$inc": {"times_robbed": 1}}
                )
            elif crime_type == 'kill' and target_id:
                self.db.crime.update_one(
                    {"user_id": target_id},
                    {"$inc": {"times_killed": 1}}
                )
            return True
        except Exception as e:
            logger.error(f"❌ Error recording crime: {e}")
            return False
    
    # ============================================================================
    # MARKET OPERATIONS
    # ============================================================================
    
    def create_market_item(self, user_id, item_name, price, quantity=1):
        """Create market listing"""
        try:
            item_id = f"{user_id}_{datetime.utcnow().timestamp()}"
            self.db.market_items.insert_one({
                "item_id": item_id,
                "seller_id": user_id,
                "item_name": item_name,
                "price": price,
                "quantity": quantity,
                "created_at": datetime.utcnow(),
                "sold": False
            })
            return item_id
        except Exception as e:
            logger.error(f"❌ Error creating market item: {e}")
            return None
    
    def get_market_items(self, limit=50):
        """Get all market items"""
        try:
            return list(self.db.market_items.find({"sold": False}).limit(limit))
        except Exception as e:
            logger.error(f"❌ Error getting market items: {e}")
            return []
    
    def buy_market_item(self, item_id, buyer_id):
        """Buy a market item"""
        try:
            item = self.db.market_items.find_one({"item_id": item_id})
            if item and not item.get('sold'):
                if self.withdraw_money(buyer_id, item['price']):
                    self.add_money(item['seller_id'], item['price'])
                    self.db.market_items.update_one(
                        {"item_id": item_id},
                        {"$set": {"sold": True, "buyer_id": buyer_id, "sold_at": datetime.utcnow()}}
                    )
                    return True
            return False
        except Exception as e:
            logger.error(f"❌ Error buying market item: {e}")
            return False
    
    def create_auction(self, user_id, item_name, starting_bid, duration_hours):
        """Create auction"""
        try:
            auction_id = f"auction_{user_id}_{datetime.utcnow().timestamp()}"
            ends_at = datetime.utcnow() + timedelta(hours=duration_hours)
            self.db.auctions.insert_one({
                "auction_id": auction_id,
                "seller_id": user_id,
                "item_name": item_name,
                "starting_bid": starting_bid,
                "current_bid": starting_bid,
                "highest_bidder": None,
                "created_at": datetime.utcnow(),
                "ends_at": ends_at,
                "ended": False,
                "bids": []
            })
            return auction_id
        except Exception as e:
            logger.error(f"❌ Error creating auction: {e}")
            return None
    
    def place_bid(self, auction_id, bidder_id, amount):
        """Place bid on auction"""
        try:
            auction = self.db.auctions.find_one({"auction_id": auction_id})
            if auction and not auction.get('ended') and auction.get('ends_at') > datetime.utcnow():
                if amount > auction.get('current_bid', 0):
                    if self.withdraw_money(bidder_id, amount):
                        # Refund previous bidder
                        if auction.get('highest_bidder'):
                            self.add_money(auction['highest_bidder'], auction['current_bid'])
                        
                        bid = {
                            "bidder_id": bidder_id,
                            "amount": amount,
                            "timestamp": datetime.utcnow()
                        }
                        self.db.auctions.update_one(
                            {"auction_id": auction_id},
                            {"$set": {
                                "current_bid": amount,
                                "highest_bidder": bidder_id
                            }, "$push": {"bids": bid}}
                        )
                        return True
            return False
        except Exception as e:
            logger.error(f"❌ Error placing bid: {e}")
            return False
    
    def end_auction(self, auction_id):
        """End auction and transfer item"""
        try:
            auction = self.db.auctions.find_one({"auction_id": auction_id})
            if auction and not auction.get('ended'):
                if auction.get('highest_bidder'):
                    self.add_money(auction['seller_id'], auction['current_bid'])
                self.db.auctions.update_one(
                    {"auction_id": auction_id},
                    {"$set": {"ended": True, "ended_at": datetime.utcnow()}}
                )
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Error ending auction: {e}")
            return False
    
    # ============================================================================
    # INVENTORY OPERATIONS
    # ============================================================================
    
    def add_item(self, user_id, item_name, quantity=1):
        """Add item to inventory"""
        try:
            self.db.users.update_one(
                {"user_id": user_id},
                {"$inc": {f"inventory.{item_name}": quantity}}
            )
            return True
        except Exception as e:
            logger.error(f"❌ Error adding item: {e}")
            return False
    
    def remove_item(self, user_id, item_name, quantity=1):
        """Remove item from inventory"""
        try:
            user = self.get_user(user_id)
            if user and user.get('inventory', {}).get(item_name, 0) >= quantity:
                self.db.users.update_one(
                    {"user_id": user_id},
                    {"$inc": {f"inventory.{item_name}": -quantity}}
                )
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Error removing item: {e}")
            return False
    
    def get_inventory(self, user_id):
        """Get user inventory"""
        try:
            user = self.get_user(user_id)
            if user:
                return user.get('inventory', {})
            return {}
        except Exception as e:
            logger.error(f"❌ Error getting inventory: {e}")
            return {}
    
    def has_item(self, user_id, item_name, quantity=1):
        """Check if user has item"""
        try:
            user = self.get_user(user_id)
            if user:
                return user.get('inventory', {}).get(item_name, 0) >= quantity
            return False
        except Exception as e:
            logger.error(f"❌ Error checking item: {e}")
            return False
    
    # ============================================================================
    # LEADERBOARD OPERATIONS
    # ============================================================================
    
    def get_money_leaderboard(self, limit=10):
        """Get money leaderboard"""
        try:
            return list(self.db.users.find(
                {"banned": {"$ne": True}}
            ).sort("money", DESCENDING).limit(limit))
        except Exception as e:
            logger.error(f"❌ Error getting money leaderboard: {e}")
            return []
    
    def get_family_leaderboard(self, limit=10):
        """Get family leaderboard by number of children"""
        try:
            pipeline = [
                {"$match": {"banned": {"$ne": True}}},
                {"$project": {
                    "user_id": 1,
                    "first_name": 1,
                    "username": 1,
                    "partner": 1,
                    "children_count": {"$size": {"$ifNull": ["$children", []]}}
                }},
                {"$sort": {"children_count": -1}},
                {"$limit": limit}
            ]
            return list(self.db.users.aggregate(pipeline))
        except Exception as e:
            logger.error(f"❌ Error getting family leaderboard: {e}")
            return []
    
    def get_factory_leaderboard(self, limit=10):
        """Get factory leaderboard"""
        try:
            pipeline = [
                {"$lookup": {
                    "from": "factory",
                    "localField": "user_id",
                    "foreignField": "user_id",
                    "as": "factory_data"
                }},
                {"$unwind": "$factory_data"},
                {"$match": {"banned": {"$ne": True}}},
                {"$project": {
                    "user_id": 1,
                    "first_name": 1,
                    "username": 1,
                    "factory_level": "$factory_data.level",
                    "total_produced": "$factory_data.total_produced",
                    "workers_count": {"$size": {"$ifNull": ["$factory_data.workers", []]}}
                }},
                {"$sort": {"factory_level": -1, "total_produced": -1}},
                {"$limit": limit}
            ]
            return list(self.db.users.aggregate(pipeline))
        except Exception as e:
            logger.error(f"❌ Error getting factory leaderboard: {e}")
            return []
    
    def get_activity_leaderboard(self, limit=10):
        """Get activity leaderboard"""
        try:
            return list(self.db.users.find(
                {"banned": {"$ne": True}}
            ).sort("total_commands", DESCENDING).limit(limit))
        except Exception as e:
            logger.error(f"❌ Error getting activity leaderboard: {e}")
            return []
    
    # ============================================================================
    # ADMIN OPERATIONS
    # ============================================================================
    
    def ban_user(self, user_id):
        """Ban user"""
        try:
            self.db.users.update_one(
                {"user_id": user_id},
                {"$set": {"banned": True}}
            )
            return True
        except Exception as e:
            logger.error(f"❌ Error banning user: {e}")
            return False
    
    def unban_user(self, user_id):
        """Unban user"""
        try:
            self.db.users.update_one(
                {"user_id": user_id},
                {"$set": {"banned": False}}
            )
            return True
        except Exception as e:
            logger.error(f"❌ Error unbanning user: {e}")
            return False
    
    def is_banned(self, user_id):
        """Check if user is banned"""
        try:
            user = self.get_user(user_id)
            return user.get('banned', False) if user else False
        except Exception as e:
            logger.error(f"❌ Error checking ban status: {e}")
            return False
    
    def get_all_users(self):
        """Get all users"""
        try:
            return list(self.db.users.find({"banned": {"$ne": True}}))
        except Exception as e:
            logger.error(f"❌ Error getting all users: {e}")
            return []
    
    def get_stats(self):
        """Get bot statistics"""
        try:
            return {
                "total_users": self.db.users.count_documents({}),
                "active_users": self.db.users.count_documents({"banned": {"$ne": True}}),
                "banned_users": self.db.users.count_documents({"banned": True}),
                "total_marriages": self.db.families.count_documents({"partner": {"$ne": None}}),
                "total_market_items": self.db.market_items.count_documents({"sold": False}),
                "total_auctions": self.db.auctions.count_documents({"ended": False})
            }
        except Exception as e:
            logger.error(f"❌ Error getting stats: {e}")
            return {}

# Create global database instance
db = Database()
