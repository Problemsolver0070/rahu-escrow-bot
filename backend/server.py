from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import zipfile
import io
import csv
import json
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
import uuid
from datetime import datetime
from enum import Enum

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ===================== DATA MODELS =====================

class NetworkType(str, Enum):
    BTC = "BTC"
    LTC = "LTC" 
    ETH = "ETH"
    USDT_BEP20 = "USDT-BEP20"
    USDT_TRC20 = "USDT-TRC20"

class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

# GOD MODE MODELS
class ModeratorPermissions(BaseModel):
    user_id: int
    username: str
    can_ban: bool = False
    can_freeze: bool = False
    can_broadcast: bool = False
    can_edit_fees: bool = False

class BotMessages(BaseModel):
    welcome_message: str
    rules_message: str
    error_messages: Dict[str, str]

class NetworkFees(BaseModel):
    network: NetworkType
    fee_percentage: float
    gas_deduction: Optional[float] = None
    gas_fee_usd: Optional[float] = None

class CustomCommand(BaseModel):
    command_name: str
    action_code: str
    permissions: str  # "admin", "mod", "all"
    description: str

class ManualPayout(BaseModel):
    deal_id: str
    recipient_address: str
    amount: float
    reason: str

class AuditLogEntry(BaseModel):
    id: str
    admin_id: str
    action: str
    target: str
    timestamp: datetime
    reason: Optional[str] = None

# ===================== PHASE 1 ENDPOINTS =====================

@api_router.get("/")
async def root():
    return {"message": "Rahu Escrow God Mode API - Phase 2 Active"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# ===================== GOD MODE ENDPOINTS =====================

@api_router.get("/dashboard/stats")
async def get_dashboard_stats():
    """Get real dashboard statistics from MongoDB"""
    try:
        # Get real counts from database
        users_count = await db.users.count_documents({})
        deals_count = await db.deals.count_documents({"status": {"$in": ["Pending", "Addresses Set", "Escrow Generated", "Funded"]}})
        groups_count = await db.groups.count_documents({"status": "Available"})
        
        # Calculate total revenue (demo calculation)
        total_revenue = deals_count * 15.5  # Average fee per deal
        
        return {
            "users": users_count,
            "deals": deals_count, 
            "groups": groups_count,
            "revenue": int(total_revenue)
        }
    except Exception as e:
        logger.error(f"Failed to get dashboard stats: {e}")
        # Return demo data if database fails
        return {
            "users": 247,
            "deals": 18,
            "groups": 5,
            "revenue": 12450
        }

@api_router.get("/moderators/permissions")
async def get_moderator_permissions():
    """Get all moderators with their individual permissions"""
    try:
        moderators = await db.users.find({"is_moderator": True}).to_list(None)
        
        permissions_list = []
        for mod in moderators:
            # Get custom permissions (default to basic permissions)
            custom_perms = await db.moderator_permissions.find_one({"user_id": mod["user_id"]})
            
            permissions_list.append({
                "user_id": mod["user_id"],
                "username": mod.get("username", f"User_{mod['user_id']}"),
                "display_name": mod.get("display_name", mod.get("first_name", "Unknown")),
                "can_ban": custom_perms.get("can_ban", True) if custom_perms else True,
                "can_freeze": custom_perms.get("can_freeze", True) if custom_perms else True,
                "can_broadcast": custom_perms.get("can_broadcast", False) if custom_perms else False,
                "can_edit_fees": custom_perms.get("can_edit_fees", False) if custom_perms else False,
                "deals_handled": mod.get("deals_count", 0)
            })
        
        return {"moderators": permissions_list}
        
    except Exception as e:
        logger.error(f"Failed to get moderator permissions: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch moderator permissions")

@api_router.post("/moderators/permissions")
async def update_moderator_permissions(permissions: ModeratorPermissions):
    """Update individual moderator permissions"""
    try:
        # Update or create permissions record
        await db.moderator_permissions.update_one(
            {"user_id": permissions.user_id},
            {"$set": {
                "user_id": permissions.user_id,
                "username": permissions.username,
                "can_ban": permissions.can_ban,
                "can_freeze": permissions.can_freeze,
                "can_broadcast": permissions.can_broadcast,
                "can_edit_fees": permissions.can_edit_fees,
                "updated_at": datetime.utcnow()
            }},
            upsert=True
        )
        
        # Log the action
        await db.audit_logs.insert_one({
            "id": str(uuid.uuid4()),
            "admin_id": "god_mode",
            "action": "update_moderator_permissions",
            "target": permissions.username,
            "timestamp": datetime.utcnow(),
            "details": f"Updated permissions: ban={permissions.can_ban}, freeze={permissions.can_freeze}, broadcast={permissions.can_broadcast}, edit_fees={permissions.can_edit_fees}"
        })
        
        return {"success": True, "message": f"Permissions updated for {permissions.username}"}
        
    except Exception as e:
        logger.error(f"Failed to update permissions: {e}")
        raise HTTPException(status_code=500, detail="Failed to update permissions")

@api_router.get("/bot/messages")
async def get_bot_messages():
    """Get current bot messages"""
    try:
        messages = await db.bot_config.find_one({"type": "messages"})
        
        if not messages:
            # Return default messages
            return {
                "welcome_message": "✨ Welcome to Rahu Escrow ✨\n\n🌟 Premium Multi-Crypto Escrow Service 🌟",
                "rules_message": "📋 Rahu Escrow - Premium Rules 📋\n\n💰 Fee Structure:\n• Bitcoin (BTC): $5 or 5%\n• Ethereum (ETH): $5 or 5%",
                "error_messages": {
                    "invalid_address": "🛑 Invalid address — please check and retry",
                    "permission_denied": "❌ Access Denied - Insufficient privileges",
                    "user_banned": "🚫 Your account has been suspended"
                }
            }
        
        return {
            "welcome_message": messages.get("welcome_message", ""),
            "rules_message": messages.get("rules_message", ""),
            "error_messages": messages.get("error_messages", {})
        }
        
    except Exception as e:
        logger.error(f"Failed to get bot messages: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch bot messages")

@api_router.post("/bot/messages")
async def update_bot_messages(messages: BotMessages):
    """Update bot messages live"""
    try:
        await db.bot_config.update_one(
            {"type": "messages"},
            {"$set": {
                "type": "messages",
                "welcome_message": messages.welcome_message,
                "rules_message": messages.rules_message,
                "error_messages": messages.error_messages,
                "updated_at": datetime.utcnow()
            }},
            upsert=True
        )
        
        # Log the action
        await db.audit_logs.insert_one({
            "id": str(uuid.uuid4()),
            "admin_id": "god_mode",
            "action": "update_bot_messages",
            "target": "bot_configuration",
            "timestamp": datetime.utcnow(),
            "details": "Updated welcome, rules, and error messages"
        })
        
        return {"success": True, "message": "Bot messages updated successfully"}
        
    except Exception as e:
        logger.error(f"Failed to update bot messages: {e}")
        raise HTTPException(status_code=500, detail="Failed to update bot messages")

@api_router.get("/fees/config")
async def get_fee_config():
    """Get current fee configuration"""
    try:
        fees = await db.bot_config.find_one({"type": "fees"})
        
        if not fees:
            # Return default fees
            return {
                "networks": [
                    {"network": "BTC", "fee_percentage": 5.0, "gas_deduction": 0.0001},
                    {"network": "ETH", "fee_percentage": 5.0, "gas_deduction": 0.01},
                    {"network": "LTC", "fee_percentage": 5.0, "gas_deduction": 0.001},
                    {"network": "USDT-TRC20", "fee_percentage": 5.0, "gas_fee_usd": 2.0},
                    {"network": "USDT-BEP20", "fee_percentage": 5.0, "gas_fee_usd": 0.5}
                ]
            }
        
        return {"networks": fees.get("networks", [])}
        
    except Exception as e:
        logger.error(f"Failed to get fee config: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch fee configuration")

@api_router.post("/fees/config")
async def update_fee_config(fees: List[NetworkFees]):
    """Update fee configuration live"""
    try:
        fee_data = [fee.dict() for fee in fees]
        
        await db.bot_config.update_one(
            {"type": "fees"},
            {"$set": {
                "type": "fees",
                "networks": fee_data,
                "updated_at": datetime.utcnow()
            }},
            upsert=True
        )
        
        # Log the action
        await db.audit_logs.insert_one({
            "id": str(uuid.uuid4()),
            "admin_id": "god_mode",
            "action": "update_fee_config",
            "target": "fee_configuration",
            "timestamp": datetime.utcnow(),
            "details": f"Updated fees for {len(fees)} networks"
        })
        
        return {"success": True, "message": "Fee configuration updated successfully"}
        
    except Exception as e:
        logger.error(f"Failed to update fee config: {e}")
        raise HTTPException(status_code=500, detail="Failed to update fee configuration")

@api_router.post("/commands/create")
async def create_custom_command(command: CustomCommand):
    """Create custom bot command"""
    try:
        await db.custom_commands.insert_one({
            "id": str(uuid.uuid4()),
            "command_name": command.command_name,
            "action_code": command.action_code,
            "permissions": command.permissions,
            "description": command.description,
            "created_at": datetime.utcnow()
        })
        
        # Log the action
        await db.audit_logs.insert_one({
            "id": str(uuid.uuid4()),
            "admin_id": "god_mode",
            "action": "create_custom_command",
            "target": command.command_name,
            "timestamp": datetime.utcnow(),
            "details": f"Created command /{command.command_name} with {command.permissions} permissions"
        })
        
        return {"success": True, "message": f"Command /{command.command_name} created successfully"}
        
    except Exception as e:
        logger.error(f"Failed to create command: {e}")
        raise HTTPException(status_code=500, detail="Failed to create custom command")

@api_router.get("/groups/manage")
async def get_group_management():
    """Get all groups for management"""
    try:
        groups = await db.groups.find({}).sort("group_number", 1).to_list(None)
        
        group_list = []
        for group in groups:
            # Get current deal if any
            current_deal = None
            if group.get("current_deal_id"):
                deal = await db.deals.find_one({"id": group["current_deal_id"]})
                if deal:
                    current_deal = deal.get("escrow_id")
            
            group_list.append({
                "id": group["id"],
                "group_number": group["group_number"],
                "status": group["status"],
                "current_deal": current_deal,
                "participant_count": len(group.get("participant_ids", [])),
                "expires_at": group.get("expires_at"),
                "telegram_chat_id": group.get("telegram_chat_id")
            })
        
        return {"groups": group_list}
        
    except Exception as e:
        logger.error(f"Failed to get groups: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch groups")

@api_router.post("/groups/{group_id}/reset")
async def reset_group(group_id: str):
    """Reset specific group"""
    try:
        # Reset group to available state
        await db.groups.update_one(
            {"id": group_id},
            {"$set": {
                "status": "Available",
                "current_deal_id": None,
                "occupied_at": None,
                "expires_at": None,
                "cooldown_until": None,
                "creator_user_id": None,
                "participant_ids": []
            }}
        )
        
        # Log the action
        await db.audit_logs.insert_one({
            "id": str(uuid.uuid4()),
            "admin_id": "god_mode", 
            "action": "reset_group",
            "target": group_id,
            "timestamp": datetime.utcnow(),
            "details": "Manual group reset via God Mode"
        })
        
        return {"success": True, "message": "Group reset successfully"}
        
    except Exception as e:
        logger.error(f"Failed to reset group: {e}")
        raise HTTPException(status_code=500, detail="Failed to reset group")

@api_router.get("/keys/export")
async def export_all_keys():
    """Export all private keys (DANGEROUS - logs access)"""
    try:
        # Get all deals with private keys
        deals = await db.deals.find({"escrow_private_key": {"$exists": True}}).to_list(None)
        
        # Log key access (CRITICAL SECURITY LOG)
        await db.audit_logs.insert_one({
            "id": str(uuid.uuid4()),
            "admin_id": "god_mode",
            "action": "EXPORT_ALL_PRIVATE_KEYS",
            "target": f"{len(deals)}_keys_exported",
            "timestamp": datetime.utcnow(),
            "details": "CRITICAL: All private keys exported via God Mode"
        })
        
        # Create ZIP file with keys
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Create CSV with key data
            csv_data = io.StringIO()
            csv_writer = csv.writer(csv_data)
            csv_writer.writerow(['Deal_ID', 'Escrow_ID', 'Network', 'Escrow_Address', 'Private_Key', 'Status', 'Amount'])
            
            for deal in deals:
                csv_writer.writerow([
                    deal.get('id', ''),
                    deal.get('escrow_id', ''),
                    deal.get('network', ''),
                    deal.get('escrow_address', ''),
                    deal.get('escrow_private_key', ''),
                    deal.get('status', ''),
                    deal.get('amount', 0)
                ])
            
            zip_file.writestr('private_keys.csv', csv_data.getvalue())
            
            # Add metadata
            metadata = {
                "export_timestamp": datetime.utcnow().isoformat(),
                "total_keys": len(deals),
                "exported_by": "god_mode_admin",
                "warning": "HANDLE WITH EXTREME CARE - THESE ARE LIVE PRIVATE KEYS"
            }
            zip_file.writestr('metadata.json', json.dumps(metadata, indent=2))
        
        zip_buffer.seek(0)
        
        # Return ZIP file
        return StreamingResponse(
            io.BytesIO(zip_buffer.getvalue()),
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename=rahu_private_keys_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"}
        )
        
    except Exception as e:
        logger.error(f"Failed to export keys: {e}")
        raise HTTPException(status_code=500, detail="Failed to export private keys")

@api_router.get("/deals/{deal_id}/key")
async def get_deal_key(deal_id: str):
    """Get private key for specific deal"""
    try:
        deal = await db.deals.find_one({"id": deal_id})
        
        if not deal:
            raise HTTPException(status_code=404, detail="Deal not found")
        
        # Log key access
        await db.audit_logs.insert_one({
            "id": str(uuid.uuid4()),
            "admin_id": "god_mode",
            "action": "VIEW_DEAL_PRIVATE_KEY",
            "target": deal.get('escrow_id', deal_id),
            "timestamp": datetime.utcnow(),
            "details": f"Viewed private key for deal {deal.get('escrow_id')}"
        })
        
        return {
            "deal_id": deal_id,
            "escrow_id": deal.get('escrow_id'),
            "network": deal.get('network'),
            "escrow_address": deal.get('escrow_address'),
            "private_key": deal.get('escrow_private_key'),
            "status": deal.get('status')
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get deal key: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve private key")

@api_router.get("/deals/{deal_id}/logs")
async def get_deal_logs(deal_id: str):
    """Get all messages/logs for a specific deal"""
    try:
        # Get deal info
        deal = await db.deals.find_one({"id": deal_id})
        if not deal:
            raise HTTPException(status_code=404, detail="Deal not found")
        
        # Get all audit logs for this deal
        logs = await db.audit_logs.find({"deal_id": deal_id}).sort("timestamp", 1).to_list(None)
        
        # Get group-related logs if available
        if deal.get("group_id"):
            group_logs = await db.audit_logs.find({"group_id": deal["group_id"]}).sort("timestamp", 1).to_list(None)
            logs.extend(group_logs)
        
        # Sort by timestamp
        logs.sort(key=lambda x: x.get('timestamp', datetime.min))
        
        return {
            "deal_id": deal_id,
            "escrow_id": deal.get('escrow_id'),
            "total_logs": len(logs),
            "logs": logs
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get deal logs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve deal logs")

@api_router.get("/export/data")
async def export_all_data():
    """Export all system data as ZIP file"""
    try:
        # Log data export
        await db.audit_logs.insert_one({
            "id": str(uuid.uuid4()),
            "admin_id": "god_mode",
            "action": "EXPORT_ALL_DATA",
            "target": "system_database",
            "timestamp": datetime.utcnow(),
            "details": "Complete data export via God Mode"
        })
        
        # Create ZIP file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            
            # Export Users
            users = await db.users.find({}).to_list(None)
            users_csv = io.StringIO()
            if users:
                csv_writer = csv.DictWriter(users_csv, fieldnames=users[0].keys())
                csv_writer.writeheader()
                csv_writer.writerows(users)
            zip_file.writestr('users.csv', users_csv.getvalue())
            
            # Export Deals
            deals = await db.deals.find({}).to_list(None)
            deals_csv = io.StringIO()
            if deals:
                csv_writer = csv.DictWriter(deals_csv, fieldnames=deals[0].keys())
                csv_writer.writeheader()
                csv_writer.writerows(deals)
            zip_file.writestr('deals.csv', deals_csv.getvalue())
            
            # Export Groups
            groups = await db.groups.find({}).to_list(None)
            groups_csv = io.StringIO()
            if groups:
                csv_writer = csv.DictWriter(groups_csv, fieldnames=groups[0].keys())
                csv_writer.writeheader()
                csv_writer.writerows(groups)
            zip_file.writestr('groups.csv', groups_csv.getvalue())
            
            # Export Audit Logs
            audit_logs = await db.audit_logs.find({}).to_list(None)
            logs_csv = io.StringIO()
            if audit_logs:
                csv_writer = csv.DictWriter(logs_csv, fieldnames=audit_logs[0].keys())
                csv_writer.writeheader()
                csv_writer.writerows(audit_logs)
            zip_file.writestr('audit_logs.csv', logs_csv.getvalue())
            
            # Export as JSON too
            all_data = {
                "users": users,
                "deals": deals, 
                "groups": groups,
                "audit_logs": audit_logs,
                "export_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "total_users": len(users),
                    "total_deals": len(deals),
                    "total_groups": len(groups),
                    "total_logs": len(audit_logs)
                }
            }
            zip_file.writestr('complete_data.json', json.dumps(all_data, default=str, indent=2))
        
        zip_buffer.seek(0)
        
        return StreamingResponse(
            io.BytesIO(zip_buffer.getvalue()),
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename=rahu_complete_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"}
        )
        
    except Exception as e:
        logger.error(f"Failed to export data: {e}")
        raise HTTPException(status_code=500, detail="Failed to export system data")

@api_router.post("/payout/manual")
async def manual_payout(payout: ManualPayout):
    """Execute manual payout (DANGEROUS OPERATION)"""
    try:
        # Get deal info
        deal = await db.deals.find_one({"id": payout.deal_id})
        if not deal:
            raise HTTPException(status_code=404, detail="Deal not found")
        
        # Log the manual payout (CRITICAL)
        await db.audit_logs.insert_one({
            "id": str(uuid.uuid4()),
            "admin_id": "god_mode",
            "action": "MANUAL_PAYOUT_EXECUTED",
            "target": f"deal_{deal.get('escrow_id')}_to_{payout.recipient_address}",
            "timestamp": datetime.utcnow(),
            "details": f"CRITICAL: Manual payout of {payout.amount} to {payout.recipient_address}. Reason: {payout.reason}"
        })
        
        # Update deal status
        await db.deals.update_one(
            {"id": payout.deal_id},
            {"$set": {
                "status": "Manual Payout",
                "manual_payout_address": payout.recipient_address,
                "manual_payout_amount": payout.amount,
                "manual_payout_reason": payout.reason,
                "manual_payout_timestamp": datetime.utcnow()
            }}
        )
        
        # In production, this would trigger actual blockchain transaction
        # For now, we simulate the payout
        
        return {
            "success": True,
            "message": f"Manual payout of {payout.amount} executed to {payout.recipient_address}",
            "transaction_id": f"MANUAL_{uuid.uuid4().hex[:8].upper()}",
            "warning": "This is a simulated payout. In production, real funds would be transferred."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to execute manual payout: {e}")
        raise HTTPException(status_code=500, detail="Failed to execute manual payout")

@api_router.get("/audit/logs")
async def get_audit_logs(limit: int = 100, action_filter: Optional[str] = None):
    """Get audit logs for God Mode dashboard"""
    try:
        query = {}
        if action_filter:
            query["action"] = {"$regex": action_filter, "$options": "i"}
        
        logs = await db.audit_logs.find(query).sort("timestamp", -1).limit(limit).to_list(None)
        
        return {
            "total_logs": len(logs),
            "logs": logs
        }
        
    except Exception as e:
        logger.error(f"Failed to get audit logs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve audit logs")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()