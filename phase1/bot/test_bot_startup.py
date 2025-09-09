#!/usr/bin/env python3
"""
Test script to verify the Phase 1 bot can start properly
"""

import asyncio
import logging
from models import db_manager, GroupStatus
from state import GroupLifecycleManager, BackgroundTasks

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_bot_initialization():
    """Test bot initialization components"""
    print("🧪 Testing Phase 1 Bot Initialization...")
    print("=" * 60)
    
    try:
        # Test database connection
        print("\n🔌 Testing Database Connection:")
        await db_manager.connect()
        print("✅ Database connected successfully")
        
        # Test group initialization
        print("\n🏛️ Testing Group Initialization:")
        groups = await GroupLifecycleManager.initialize_groups()
        print(f"✅ Initialized {len(groups)} escrow groups")
        
        # Show first few groups
        for group in groups[:5]:
            status_str = group.status if isinstance(group.status, str) else group.status.value
            print(f"   • Group {group.group_number}: {status_str}")
        
        # Test background tasks
        print("\n⚡ Testing Background Tasks:")
        await BackgroundTasks.start_background_tasks()
        print("✅ Background tasks started")
        
        # Test database operations
        print("\n💾 Testing Database Operations:")
        all_groups = await db_manager.get_all_groups()
        available_groups = [g for g in all_groups if (g.status == "Available" or g.status == GroupStatus.AVAILABLE)]
        print(f"✅ Found {len(all_groups)} total groups, {len(available_groups)} available")
        
        # Test audit logging
        print("\n📜 Testing Audit Logging:")
        from state import AuditLogger
        await AuditLogger.log_system_action(
            action="test_initialization",
            details="Testing bot initialization"
        )
        print("✅ Audit logging working")
        
        print("\n✨ Bot Initialization Test Complete!")
        print("🚀 Phase 1 bot is ready to run!")
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await db_manager.disconnect()
        print("🔌 Database disconnected")
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_bot_initialization())