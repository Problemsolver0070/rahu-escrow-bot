"""
Real-time Blockchain Monitoring Service
Production-grade transaction monitoring and webhook handling
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from decimal import Decimal
import json

from models import NetworkType, Deal, DealStatus, db_manager
from blockchain import real_wallet_manager, BlockchainAPI
from state import AuditLogger

logger = logging.getLogger(__name__)

class RealTimeMonitor:
    """Real-time blockchain monitoring service"""
    
    def __init__(self):
        self.monitored_addresses: Dict[str, Dict] = {}
        self.monitoring_tasks: Dict[str, asyncio.Task] = {}
        self.api = BlockchainAPI()
        self.running = False
    
    async def start(self):
        """Start the monitoring service"""
        if self.running:
            return
            
        self.running = True
        logger.info("🚀 Starting Real-time Blockchain Monitor")
        
        # Start background monitoring task
        asyncio.create_task(self._monitor_loop())
        
        # Load existing deals that need monitoring
        await self._load_existing_deals()
    
    async def stop(self):
        """Stop the monitoring service"""
        self.running = False
        
        # Cancel all monitoring tasks
        for task in self.monitoring_tasks.values():
            task.cancel()
        
        self.monitoring_tasks.clear()
        logger.info("🛑 Stopped Real-time Blockchain Monitor")
    
    async def add_address(self, network: NetworkType, address: str, deal_id: str, callback: Callable = None):
        """Add address to monitoring"""
        key = f"{network.value}:{address}"
        
        self.monitored_addresses[key] = {
            "network": network,
            "address": address,
            "deal_id": deal_id,
            "callback": callback,
            "added_at": datetime.utcnow(),
            "last_check": None,
            "balance": Decimal("0"),
            "transactions": []
        }
        
        logger.info(f"📍 Added {network.value} address to monitoring: {address}")
    
    async def remove_address(self, network: NetworkType, address: str):
        """Remove address from monitoring"""
        key = f"{network.value}:{address}"
        
        if key in self.monitored_addresses:
            del self.monitored_addresses[key]
            
            if key in self.monitoring_tasks:
                self.monitoring_tasks[key].cancel()
                del self.monitoring_tasks[key]
            
            logger.info(f"📍 Removed {network.value} address from monitoring: {address}")
    
    async def _load_existing_deals(self):
        """Load existing unfunded deals for monitoring"""
        try:
            # Get all deals that have escrow addresses but aren't funded yet
            active_deals = await db_manager.get_active_deals()
            
            for deal in active_deals:
                if (deal.escrow_address and 
                    deal.status in [DealStatus.ESCROW_GENERATED, DealStatus.ADDRESSES_SET] and
                    deal.network):
                    
                    await self.add_address(
                        NetworkType(deal.network),
                        deal.escrow_address,
                        deal.id,
                        self._funding_detected_callback
                    )
            
            logger.info(f"📊 Loaded {len(self.monitored_addresses)} addresses for monitoring")
            
        except Exception as e:
            logger.error(f"Failed to load existing deals: {e}")
    
    async def _monitor_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                await self._check_all_addresses()
                
                # Check every 30 seconds
                await asyncio.sleep(30)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    async def _check_all_addresses(self):
        """Check all monitored addresses"""
        if not self.monitored_addresses:
            return
        
        async with self.api as api:
            for key, monitor_data in self.monitored_addresses.items():
                try:
                    await self._check_single_address(api, monitor_data)
                    
                except Exception as e:
                    logger.error(f"Failed to check address {key}: {e}")
    
    async def _check_single_address(self, api: BlockchainAPI, monitor_data: Dict):
        """Check a single address for new transactions"""
        try:
            network = monitor_data["network"]
            address = monitor_data["address"]
            
            # Get current balance and transactions
            balance = await api.get_balance(network, address)
            transactions = await api.get_transactions(network, address, 5)
            
            # Update last check time
            monitor_data["last_check"] = datetime.utcnow()
            
            # Check if balance changed (funding detected)
            old_balance = monitor_data["balance"]
            if balance > old_balance:
                logger.info(f"💰 FUNDING DETECTED! {network.value} {address}: {balance}")
                
                # Update stored balance
                monitor_data["balance"] = balance
                monitor_data["transactions"] = transactions
                
                # Call callback if provided
                if monitor_data["callback"]:
                    funding_data = {
                        "address": address,
                        "network": network.value,
                        "old_balance": float(old_balance),
                        "new_balance": float(balance),
                        "amount_received": float(balance - old_balance),
                        "transactions": transactions,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    
                    await monitor_data["callback"](monitor_data["deal_id"], funding_data)
            
        except Exception as e:
            logger.error(f"Failed to check single address: {e}")
    
    async def _funding_detected_callback(self, deal_id: str, funding_data: Dict):
        """Handle funding detection"""
        try:
            logger.info(f"🚨 REAL FUNDING DETECTED for deal {deal_id}")
            
            # Get deal details
            deal = await db_manager.get_deal_by_id(deal_id)
            if not deal:
                logger.error(f"Deal {deal_id} not found")
                return
            
            # Update deal status
            updates = {
                "status": DealStatus.FUNDED.value,
                "amount": funding_data["amount_received"],
                "funded_at": datetime.utcnow(),
                "transaction_hash": funding_data["transactions"][0].get("tx_hash") if funding_data["transactions"] else None
            }
            
            success = await db_manager.update_deal(deal_id, updates)
            
            if success:
                # Log funding
                await AuditLogger.log_system_action(
                    action="escrow_funded",
                    target=funding_data["address"],
                    details=f"Real funding: {funding_data['amount_received']} {funding_data['network']}"
                )
                
                # TODO: Send notification to Telegram group
                # This would notify users in the escrow group about funding
                
                # Remove from monitoring (deal is now funded)
                await self.remove_address(
                    NetworkType(funding_data["network"]),
                    funding_data["address"]
                )
                
                logger.info(f"✅ Successfully processed funding for deal {deal.escrow_id}")
            
        except Exception as e:
            logger.error(f"Failed to process funding callback: {e}")
    
    def get_monitoring_stats(self) -> Dict:
        """Get current monitoring statistics"""
        stats = {
            "total_addresses": len(self.monitored_addresses),
            "networks": {},
            "oldest_monitor": None,
            "newest_monitor": None
        }
        
        if self.monitored_addresses:
            # Count by network
            for monitor_data in self.monitored_addresses.values():
                network = monitor_data["network"].value
                stats["networks"][network] = stats["networks"].get(network, 0) + 1
            
            # Find oldest and newest
            add_times = [data["added_at"] for data in self.monitored_addresses.values()]
            stats["oldest_monitor"] = min(add_times).isoformat()
            stats["newest_monitor"] = max(add_times).isoformat()
        
        return stats

class WebhookHandler:
    """Handle blockchain webhooks for instant notifications"""
    
    def __init__(self, monitor: RealTimeMonitor):
        self.monitor = monitor
    
    async def handle_bitcoin_webhook(self, webhook_data: Dict):
        """Handle Bitcoin blockchain webhooks"""
        try:
            # Parse Bitcoin webhook
            address = webhook_data.get("address")
            tx_hash = webhook_data.get("tx_hash")
            amount = webhook_data.get("amount", 0)
            
            if address and address in [data["address"] for data in self.monitor.monitored_addresses.values()]:
                logger.info(f"🔔 Bitcoin webhook received for {address}")
                
                # Trigger immediate check
                for key, monitor_data in self.monitor.monitored_addresses.items():
                    if monitor_data["address"] == address:
                        async with self.monitor.api as api:
                            await self.monitor._check_single_address(api, monitor_data)
                        break
        
        except Exception as e:
            logger.error(f"Failed to handle Bitcoin webhook: {e}")
    
    async def handle_ethereum_webhook(self, webhook_data: Dict):
        """Handle Ethereum blockchain webhooks"""
        try:
            # Parse Ethereum webhook
            to_address = webhook_data.get("to", "").lower()
            tx_hash = webhook_data.get("hash")
            value = webhook_data.get("value", "0")
            
            # Check if this is one of our monitored addresses
            for key, monitor_data in self.monitor.monitored_addresses.items():
                if (monitor_data["network"] in [NetworkType.ETH, NetworkType.USDT_BEP20] and 
                    monitor_data["address"].lower() == to_address):
                    
                    logger.info(f"🔔 Ethereum webhook received for {to_address}")
                    
                    # Trigger immediate check
                    async with self.monitor.api as api:
                        await self.monitor._check_single_address(api, monitor_data)
                    break
        
        except Exception as e:
            logger.error(f"Failed to handle Ethereum webhook: {e}")
    
    async def handle_tron_webhook(self, webhook_data: Dict):
        """Handle TRON blockchain webhooks"""
        try:
            # Parse TRON webhook
            to_address = webhook_data.get("to_address")
            tx_id = webhook_data.get("txID")
            
            # Check if this is one of our monitored addresses
            for key, monitor_data in self.monitor.monitored_addresses.items():
                if (monitor_data["network"] == NetworkType.USDT_TRC20 and 
                    monitor_data["address"] == to_address):
                    
                    logger.info(f"🔔 TRON webhook received for {to_address}")
                    
                    # Trigger immediate check
                    async with self.monitor.api as api:
                        await self.monitor._check_single_address(api, monitor_data)
                    break
        
        except Exception as e:
            logger.error(f"Failed to handle TRON webhook: {e}")

# Global monitoring service
real_monitor = RealTimeMonitor()
webhook_handler = WebhookHandler(real_monitor)

async def start_monitoring_service():
    """Start the global monitoring service"""
    await real_monitor.start()

async def stop_monitoring_service():
    """Stop the global monitoring service"""
    await real_monitor.stop()