"""
MongoDB Models for Rahu Escrow Bot Phase 1
Luxury data structures for the premium escrow ecosystem
"""

import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from enum import Enum
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.getenv('DB_NAME', 'rahu_escrow')

class NetworkType(str, Enum):
    """Supported cryptocurrency networks"""
    BTC = "BTC"
    LTC = "LTC" 
    ETH = "ETH"
    USDT_BEP20 = "USDT-BEP20"
    USDT_TRC20 = "USDT-TRC20"

class GroupStatus(str, Enum):
    """Escrow group lifecycle states"""
    AVAILABLE = "Available"
    OCCUPIED = "Occupied" 
    ESCROW_CREATED = "Escrow Created"
    FUNDED = "Funded"
    DISPUTED = "Disputed"
    COOLDOWN = "Cooldown"

class DealStatus(str, Enum):
    """Deal progression states"""
    PENDING = "Pending"
    ADDRESSES_SET = "Addresses Set"
    ESCROW_GENERATED = "Escrow Generated" 
    FUNDED = "Funded"
    COMPLETED = "Completed"
    DISPUTED = "Disputed"
    CANCELLED = "Cancelled"

class User(BaseModel):
    """Premium user model with luxury tracking"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: int  # Telegram user ID
    username: Optional[str] = None
    display_name: Optional[str] = None
    first_name: str
    is_banned: bool = False
    is_moderator: bool = False
    is_admin: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_active: datetime = Field(default_factory=datetime.utcnow)
    deals_count: int = 0
    total_volume: float = 0.0
    
    class Config:
        use_enum_values = True

class Group(BaseModel):
    """Luxury escrow group with lifecycle management"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    group_number: int  # 1-50
    telegram_chat_id: Optional[int] = None
    status: GroupStatus = GroupStatus.AVAILABLE
    current_deal_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    occupied_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    cooldown_until: Optional[datetime] = None
    creator_user_id: Optional[int] = None
    participant_ids: List[int] = []
    
    class Config:
        use_enum_values = True

class Deal(BaseModel):
    """Premium escrow deal with multi-chain support"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    escrow_id: str  # ESCROW-XXXXXX format
    group_id: str
    buyer_user_id: Optional[int] = None
    seller_user_id: Optional[int] = None
    buyer_address: Optional[str] = None
    seller_address: Optional[str] = None
    network: Optional[NetworkType] = None
    escrow_address: Optional[str] = None
    escrow_private_key: Optional[str] = None  # Encrypted in production
    amount: Optional[float] = None
    amount_usd: Optional[float] = None
    fee_amount: Optional[float] = None
    status: DealStatus = DealStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    funded_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    transaction_hash: Optional[str] = None
    is_frozen: bool = False
    dispute_reason: Optional[str] = None
    
    class Config:
        use_enum_values = True

class AuditLog(BaseModel):
    """Comprehensive audit logging for all actions"""  
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    log_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: int
    username: Optional[str] = None
    action: str  # Command or action performed
    target: Optional[str] = None  # Target user, group, or deal
    group_id: Optional[str] = None
    deal_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    details: Optional[str] = None  # Additional context
    ip_address: Optional[str] = None
    success: bool = True
    
    class Config:
        use_enum_values = True

class DatabaseManager:
    """Luxury database manager for premium operations"""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[AsyncIOMotorDatabase] = None
    
    async def connect(self):
        """Establish premium database connection"""
        self.client = AsyncIOMotorClient(MONGO_URL)
        self.db = self.client[DB_NAME]
        
        # Create indexes for performance
        await self.create_indexes()
    
    async def disconnect(self):
        """Gracefully close database connection"""
        if self.client:
            self.client.close()
    
    async def create_indexes(self):
        """Create database indexes for optimal performance"""
        if self.db is None:
            return
            
        # User indexes
        await self.db.users.create_index("user_id", unique=True)
        await self.db.users.create_index("username")
        await self.db.users.create_index([("is_banned", 1), ("is_moderator", 1)])
        
        # Group indexes  
        await self.db.groups.create_index("group_number", unique=True)
        await self.db.groups.create_index("status")
        await self.db.groups.create_index("expires_at")
        
        # Deal indexes
        await self.db.deals.create_index("escrow_id", unique=True)
        await self.db.deals.create_index("group_id")
        await self.db.deals.create_index([("buyer_user_id", 1), ("seller_user_id", 1)])
        await self.db.deals.create_index("status")
        await self.db.deals.create_index("network")
        
        # Audit log indexes
        await self.db.audit_logs.create_index("user_id")
        await self.db.audit_logs.create_index("timestamp") 
        await self.db.audit_logs.create_index("action")
        await self.db.audit_logs.create_index("log_id", unique=True)
    
    # User operations
    async def create_user(self, user: User) -> User:
        """Create premium user account"""
        await self.db.users.insert_one(user.dict())
        return user
    
    async def get_user_by_telegram_id(self, user_id: int) -> Optional[User]:
        """Retrieve user by Telegram ID"""
        user_data = await self.db.users.find_one({"user_id": user_id})
        return User(**user_data) if user_data else None
    
    async def update_user(self, user_id: int, updates: Dict) -> bool:
        """Update user information"""
        result = await self.db.users.update_one(
            {"user_id": user_id}, 
            {"$set": updates}
        )
        return result.modified_count > 0
    
    async def ban_user(self, user_id: int) -> bool:
        """Ban user from premium service"""
        return await self.update_user(user_id, {"is_banned": True})
    
    async def unban_user(self, user_id: int) -> bool:
        """Restore user access to premium service"""
        return await self.update_user(user_id, {"is_banned": False})
    
    async def set_moderator(self, user_id: int, is_moderator: bool) -> bool:
        """Grant or revoke moderator privileges"""
        return await self.update_user(user_id, {"is_moderator": is_moderator})
    
    async def get_moderators(self) -> List[User]:
        """Get all premium moderators"""
        moderators = await self.db.users.find({"is_moderator": True}).to_list(None)
        return [User(**mod) for mod in moderators]
    
    async def get_all_users(self) -> List[User]:
        """Get all premium users"""
        users = await self.db.users.find({}).to_list(None)
        return [User(**user) for user in users]
    
    # Group operations
    async def create_groups(self, count: int = 50) -> List[Group]:
        """Create premium escrow groups"""
        groups = []
        for i in range(1, count + 1):
            group = Group(group_number=i)
            groups.append(group)
        
        if groups:
            await self.db.groups.insert_many([group.dict() for group in groups])
        return groups
    
    async def get_available_group(self) -> Optional[Group]:
        """Get next available premium group"""
        group_data = await self.db.groups.find_one(
            {"status": GroupStatus.AVAILABLE},
            sort=[("group_number", 1)]
        )
        return Group(**group_data) if group_data else None
    
    async def update_group_status(self, group_id: str, status: GroupStatus, **kwargs) -> bool:
        """Update group status with luxury precision"""
        status_value = status.value if hasattr(status, 'value') else status
        updates = {"status": status_value}
        updates.update(kwargs)
        
        result = await self.db.groups.update_one(
            {"id": group_id},
            {"$set": updates}
        )
        return result.modified_count > 0
    
    async def get_group_by_id(self, group_id: str) -> Optional[Group]:
        """Retrieve premium group by ID"""
        group_data = await self.db.groups.find_one({"id": group_id})
        return Group(**group_data) if group_data else None
    
    async def get_expired_groups(self) -> List[Group]:
        """Get groups ready for cooldown reset"""
        now = datetime.utcnow()
        groups = await self.db.groups.find({
            "cooldown_until": {"$lte": now},
            "status": GroupStatus.COOLDOWN
        }).to_list(None)
        return [Group(**group) for group in groups]
    
    async def reset_group(self, group_id: str) -> bool:
        """Reset group to available state"""
        updates = {
            "status": GroupStatus.AVAILABLE,
            "current_deal_id": None,
            "occupied_at": None,
            "expires_at": None,
            "cooldown_until": None,
            "creator_user_id": None,
            "participant_ids": []
        }
        
        result = await self.db.groups.update_one(
            {"id": group_id},
            {"$set": updates}
        )
        return result.modified_count > 0
    
    async def get_all_groups(self) -> List[Group]:
        """Get all premium groups"""
        groups = await self.db.groups.find({}).sort("group_number", 1).to_list(None)
        return [Group(**group) for group in groups]
    
    # Deal operations
    async def create_deal(self, deal: Deal) -> Deal:
        """Create premium escrow deal"""
        await self.db.deals.insert_one(deal.dict())
        return deal
    
    async def get_deal_by_escrow_id(self, escrow_id: str) -> Optional[Deal]:
        """Retrieve deal by escrow ID"""
        deal_data = await self.db.deals.find_one({"escrow_id": escrow_id})
        return Deal(**deal_data) if deal_data else None
    
    async def get_deal_by_group_id(self, group_id: str) -> Optional[Deal]:
        """Retrieve deal by group ID"""
        deal_data = await self.db.deals.find_one({"group_id": group_id})
        return Deal(**deal_data) if deal_data else None
    
    async def get_deal_by_id(self, deal_id: str) -> Optional[Deal]:
        """Retrieve deal by deal ID"""
        deal_data = await self.db.deals.find_one({"id": deal_id})
        return Deal(**deal_data) if deal_data else None
    
    async def update_deal(self, deal_id: str, updates: Dict) -> bool:
        """Update deal with luxury precision"""
        result = await self.db.deals.update_one(
            {"id": deal_id},
            {"$set": updates}
        )
        return result.modified_count > 0
    
    async def freeze_deal(self, deal_id: str) -> bool:
        """Freeze premium deal"""
        return await self.update_deal(deal_id, {"is_frozen": True})
    
    async def unfreeze_deal(self, deal_id: str) -> bool:
        """Unfreeze premium deal"""
        return await self.update_deal(deal_id, {"is_frozen": False})
    
    async def get_active_deals(self) -> List[Deal]:
        """Get all active premium deals"""
        deals = await self.db.deals.find({
            "status": {"$in": [DealStatus.PENDING, DealStatus.ADDRESSES_SET, 
                              DealStatus.ESCROW_GENERATED, DealStatus.FUNDED]}
        }).to_list(None)
        return [Deal(**deal) for deal in deals]
    
    # Audit log operations
    async def log_action(self, log: AuditLog) -> AuditLog:
        """Log premium action for audit trail"""
        await self.db.audit_logs.insert_one(log.dict())
        return log
    
    async def get_audit_logs(self, limit: int = 100, user_id: Optional[int] = None) -> List[AuditLog]:
        """Retrieve premium audit logs"""
        query = {}
        if user_id:
            query["user_id"] = user_id
            
        logs = await self.db.audit_logs.find(query).sort("timestamp", -1).limit(limit).to_list(None)
        return [AuditLog(**log) for log in logs]

# Global database manager instance
db_manager = DatabaseManager()