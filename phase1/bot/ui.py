"""
Luxury UI Components for Rahu Escrow Bot Phase 1
Premium message formatting and inline keyboards
"""

from typing import List, Optional, Dict, Any
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime

from models import NetworkType, GroupStatus, DealStatus, User, Group, Deal
from state import NetworkDetector

class LuxuryFormatter:
    """Premium message formatting with luxury aesthetics"""
    
    # Network symbols and display names
    NETWORK_SYMBOLS = {
        NetworkType.BTC: "₿",
        NetworkType.LTC: "Ł", 
        NetworkType.ETH: "Ξ",
        NetworkType.USDT_BEP20: "₮",
        NetworkType.USDT_TRC20: "₮"
    }
    
    NETWORK_NAMES = {
        NetworkType.BTC: "Bitcoin (BTC)",
        NetworkType.LTC: "Litecoin (LTC)",
        NetworkType.ETH: "Ethereum (ETH)", 
        NetworkType.USDT_BEP20: "USDT-BEP20 (BSC)",
        NetworkType.USDT_TRC20: "USDT-TRC20 (TRON)"
    }
    
    @staticmethod
    def format_welcome_message(user_name: str, is_returning: bool = False) -> str:
        """Luxury welcome message with multi-chain support"""
        greeting = "Welcome back" if is_returning else "Welcome"
        
        return f"""
✨ *{greeting} to Rahu Escrow* ✨

🌟 *Premium Multi-Crypto Escrow Service* 🌟

Greetings, {user_name}! You've entered the most sophisticated escrow ecosystem on Telegram.

🔰 *Your Elite Features:*
• Multi-cryptocurrency support
• 12-hour private escrow suites  
• Professional dispute resolution
• Premium customer support

💰 *Supported Cryptocurrencies:*
• {LuxuryFormatter.NETWORK_SYMBOLS[NetworkType.BTC]} Bitcoin (BTC)
• {LuxuryFormatter.NETWORK_SYMBOLS[NetworkType.ETH]} Ethereum (ETH) 
• {LuxuryFormatter.NETWORK_SYMBOLS[NetworkType.LTC]} Litecoin (LTC)
• {LuxuryFormatter.NETWORK_SYMBOLS[NetworkType.USDT_TRC20]} USDT (TRC-20)
• {LuxuryFormatter.NETWORK_SYMBOLS[NetworkType.USDT_BEP20]} USDT (BEP-20)

💎 *Status:* Verified Member
🛡️ *Security:* Military-grade encryption
⚡ *Response:* Instant processing

*Ready to create your first luxury deal?*
        """
    
    @staticmethod
    def format_rules_message() -> str:
        """Premium rules with multi-chain fee structure"""
        return """
📋 *Rahu Escrow - Premium Rules* 📋

💰 **Fee Structure:**
• **Bitcoin (BTC):** $5 or 5% + gas deducted on release
• **Litecoin (LTC):** $5 or 5% + gas deducted on release  
• **Ethereum (ETH):** $5 or 5% + gas deducted on release
• **USDT-BEP20:** $5 or 5% 
• **USDT-TRC20:** $5 or 5% + $2 gas fee

🌐 **Supported Networks:**
• **₿ Bitcoin (BTC)** - Native blockchain
• **Ξ Ethereum (ETH)** - ERC-20 network
• **Ł Litecoin (LTC)** - Native blockchain
• **₮ USDT-TRC20** - Tron network (Recommended)
• **₮ USDT-BEP20** - Binance Smart Chain

⚖️ **Dispute Policy:**
• Professional arbitration
• 48-hour resolution guarantee
• Evidence-based decisions
• Binding final judgments

🛡️ **Anti-Scam Protection:**
• Multi-signature verification
• Blockchain confirmation required
• Suspicious activity monitoring
• Immediate fund protection

🚨 **Zero Tolerance:**
• Fake payment proofs
• Address manipulation
• Threatening behavior
• External deal negotiations

💎 **Network Fees:**
• **BTC:** 0.0001 BTC (network fee)
• **ETH:** Dynamic gas fees
• **LTC:** 0.001 LTC (network fee)
• **USDT-TRC20:** Free transfers
• **USDT-BEP20:** ~$0.50 network fee

*Your security is our luxury promise.*
        """
    
    @staticmethod
    def format_deal_created_message(escrow_id: str, group_number: int) -> str:
        """Luxury deal creation confirmation"""
        return f"""
✨ *Creating Your Escrow Suite...* ✨

🔄 *Processing...*
• Generating secure group
• Configuring blockchain bridge
• Activating luxury features

⚡ *Ready!*

🏛️ **{escrow_id}** has been created!

🔗 *Private Group:* Group {group_number}
⏰ *Valid for:* 12 hours
👥 *Max participants:* 2 users

🌟 *Features Activated:*
• Military-grade encryption
• Real-time notifications
• Professional support
• Dispute protection

*Enter your private escrow suite to begin.*
        """
    
    @staticmethod
    def format_network_selection_message(role: str) -> str:
        """Premium network selection interface"""
        return f"""
🔘 *{role.upper()} Registration* 🔘

Please select your preferred cryptocurrency:

💰 *Choose your network:*
        """
    
    @staticmethod
    def format_address_registered_message(role: str, address: str, network: NetworkType) -> str:
        """Luxury address registration confirmation"""
        symbol = LuxuryFormatter.NETWORK_SYMBOLS.get(network, "💰")
        network_name = LuxuryFormatter.NETWORK_NAMES.get(network, network.value)
        
        return f"""
🔘 *Role Assignment: {role.upper()}*

✅ **Address Registered:**
`{address}`

🌐 **Network:** {symbol} {network_name}
🔍 **Verification:** Address format valid
⚡ **Status:** Ready for escrow

*Waiting for other participant to register their address...*
        """
    
    @staticmethod
    def format_escrow_active_message(deal: Deal, buyer_address: str, seller_address: str) -> str:
        """Luxury escrow activation message"""
        symbol = LuxuryFormatter.NETWORK_SYMBOLS.get(NetworkType(deal.network), "💰")
        network_name = LuxuryFormatter.NETWORK_NAMES.get(NetworkType(deal.network), deal.network)
        
        return f"""
🏛️ **ESCROW SUITE ACTIVE** 🏛️

📋 *Deal Details:*
• **Escrow ID:** {deal.escrow_id}
• **Network:** {symbol} {network_name}
• **Status:** Awaiting funding

💳 **Addresses:**
• **Buyer:** `{buyer_address}`
• **Seller:** `{seller_address}`

🏦 **Escrow Address:**
`{deal.escrow_address}`

💎 *Send {deal.network.split('-')[0] if 'USDT' in deal.network else deal.network} to the escrow address above*

⚠️ **Important:** Only send the exact amount agreed upon. Funds will be held securely until release.
        """
    
    @staticmethod
    def format_funded_message(deal: Deal, amount: float, tx_hash: str, confirmations: int = 3) -> str:
        """Luxury funding confirmation message"""
        symbol = LuxuryFormatter.NETWORK_SYMBOLS.get(NetworkType(deal.network), "💰")
        network_name = LuxuryFormatter.NETWORK_NAMES.get(NetworkType(deal.network), deal.network)
        
        return f"""
🚨 **THE ESCROW HAS BEEN FUNDED!** 🚨

💰 **Amount:** {amount} {deal.network.split('-')[0] if 'USDT' in deal.network else deal.network}
💵 **USD Value:** ${deal.amount_usd:.2f} USD
🌐 **Network:** {symbol} {network_name}
🔗 **TX Hash:** `{tx_hash}`
⏰ **Confirmed:** {confirmations}/3 blocks

🎯 **Next Steps:**
• Buyer: Complete your side of the deal
• Seller: Await buyer confirmation

*Funds are secure in escrow. Choose your action below.*
        """
    
    @staticmethod
    def format_error_message(error_type: str, network: str = None) -> str:
        """Luxury error messages"""
        if error_type == "invalid_address":
            return f"🛑 Invalid {network} address — please check and retry."
        elif error_type == "network_mismatch":
            return f"🛑 Network mismatch — please use same network as other participant."
        elif error_type == "no_groups":
            return "🚫 All escrow suites are currently occupied — please try again in a few minutes."
        elif error_type == "permission_denied":
            return "❌ *Access Denied* - Insufficient privileges for this action."
        elif error_type == "user_banned":
            return "🚫 Your account has been suspended from premium services."
        else:
            return "⚠️ An unexpected error occurred — our premium support team has been notified."
    
    @staticmethod
    def format_moderation_action(action: str, target: str, moderator: str) -> str:
        """Luxury moderation action confirmation"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if action == "ban":
            return f"""
🔨 **MODERATION ACTION**

✅ User {target} has been banned
🛡️ Action by: @{moderator}
⏰ Timestamp: {timestamp}

*User removed from all active escrow deals.*
            """
        elif action == "freeze":
            return f"""
❄️ **DEAL FROZEN**

🆔 **Target:** {target}
🛡️ **Action by:** @{moderator}
⏰ **Time:** {timestamp.split()[1]}

*All transactions suspended pending investigation.*
            """
        elif action == "unfreeze":
            return f"""
🔥 **DEAL UNFROZEN**

🆔 **Target:** {target}
🛡️ **Action by:** @{moderator}
⏰ **Time:** {timestamp.split()[1]}

*Transactions resumed.*
            """
        else:
            return f"""
⚖️ **ADMINISTRATIVE ACTION**

🎯 **Action:** {action}
🎯 **Target:** {target}
🛡️ **By:** @{moderator}
⏰ **Time:** {timestamp}
            """

class KeyboardBuilder:
    """Premium inline keyboard builder"""
    
    @staticmethod
    def build_main_menu() -> InlineKeyboardMarkup:
        """Main menu keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("🆕 Create Deal", callback_data="create_deal"),
                InlineKeyboardButton("📋 Rules", callback_data="show_rules")
            ],
            [
                InlineKeyboardButton("🙋 Help", callback_data="get_help"),
                InlineKeyboardButton("👑 VIP Support", callback_data="vip_support")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def build_network_selection(role: str) -> InlineKeyboardMarkup:
        """Network selection keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("₿ Bitcoin (BTC)", callback_data=f"{role}_crypto_BTC"),
                InlineKeyboardButton("Ξ Ethereum (ETH)", callback_data=f"{role}_crypto_ETH")
            ],
            [
                InlineKeyboardButton("Ł Litecoin (LTC)", callback_data=f"{role}_crypto_LTC"),
                InlineKeyboardButton("₮ USDT-TRC20", callback_data=f"{role}_crypto_USDT_TRC20")
            ],
            [
                InlineKeyboardButton("₮ USDT-BEP20", callback_data=f"{role}_crypto_USDT_BEP20")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def build_escrow_actions() -> InlineKeyboardMarkup:
        """Escrow action buttons"""
        keyboard = [
            [
                InlineKeyboardButton("📱 Show QR", callback_data="show_qr"),
                InlineKeyboardButton("💰 Check Balance", callback_data="check_balance")
            ],
            [InlineKeyboardButton("🆘 Need Help?", callback_data="get_help")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def build_funded_actions() -> InlineKeyboardMarkup:
        """Post-funding action buttons"""
        keyboard = [
            [
                InlineKeyboardButton("✅ Release to Seller", callback_data="release_funds"),
                InlineKeyboardButton("↩️ Refund Buyer", callback_data="refund_buyer")
            ],
            [InlineKeyboardButton("⚖️ Raise Dispute", callback_data="raise_dispute")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def build_deal_creation_keyboard(escrow_id: str) -> InlineKeyboardMarkup:
        """Deal creation result keyboard"""
        keyboard = [
            [InlineKeyboardButton("🚀 Enter Escrow Suite", callback_data=f"enter_group_{escrow_id}")],
            [InlineKeyboardButton("📋 View Deal Rules", callback_data="show_rules")]
        ]
        return InlineKeyboardMarkup(keyboard)

class MessageBuilder:
    """Premium message construction utilities"""
    
    @staticmethod
    def build_network_instruction(crypto: str) -> str:
        """Build network-specific address instruction"""
        crypto_clean = crypto.replace("_", "-")
        symbol = LuxuryFormatter.NETWORK_SYMBOLS.get(NetworkType(crypto_clean), "💰")
        
        examples = {
            "BTC": "`1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`",
            "ETH": "`0x742d35Cc6Bb78392F43E57C2A3c70ADa99c52f12`", 
            "LTC": "`LdP8Qox1VAhCzLJGqrMKxPFTVEz8CvdCg2`",
            "USDT-TRC20": "`TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t`",
            "USDT-BEP20": "`0x742d35Cc6Bb78392F43E57C2A3c70ADa99c52f12`"
        }
        
        example = examples.get(crypto_clean, "`ADDRESS_EXAMPLE`")
        
        return f"""
🔘 *{symbol} {crypto_clean} Selected*

Please send your {crypto_clean} address using:
`/buyer YOUR_{crypto.upper()}_ADDRESS` or `/seller YOUR_{crypto.upper()}_ADDRESS`

📝 *Example format:*
{example}

🔍 *We'll verify the address format automatically*
        """
    
    @staticmethod
    def build_group_list_message(groups: List[Group]) -> str:
        """Build group status list for admin"""
        message = "🏛️ **ESCROW GROUP STATUS** 🏛️\n\n"
        
        available_count = sum(1 for g in groups if g.status == GroupStatus.AVAILABLE)
        occupied_count = sum(1 for g in groups if g.status == GroupStatus.OCCUPIED)
        active_count = sum(1 for g in groups if g.status in [GroupStatus.ESCROW_CREATED, GroupStatus.FUNDED])
        
        message += f"📊 *Summary:* {available_count} Available • {occupied_count} Occupied • {active_count} Active\n\n"
        
        for group in groups[:10]:  # Show first 10 groups
            status_emoji = {
                GroupStatus.AVAILABLE: "🟢",
                GroupStatus.OCCUPIED: "🟡", 
                GroupStatus.ESCROW_CREATED: "🔵",
                GroupStatus.FUNDED: "🟠",
                GroupStatus.DISPUTED: "🔴",
                GroupStatus.COOLDOWN: "⚫"
            }
            
            emoji = status_emoji.get(group.status, "❓")
            message += f"{emoji} **Group {group.group_number}** - {group.status.value}\n"
        
        if len(groups) > 10:
            message += f"\n*... and {len(groups) - 10} more groups*"
        
        return message
    
    @staticmethod
    def build_user_list_message(users: List[User]) -> str:
        """Build user list for admin"""
        message = "👥 **PREMIUM USER REGISTRY** 👥\n\n"
        
        total_users = len(users)
        banned_users = sum(1 for u in users if u.is_banned)
        moderators = sum(1 for u in users if u.is_moderator)
        
        message += f"📊 *Summary:* {total_users} Total • {banned_users} Banned • {moderators} Moderators\n\n"
        
        for user in users[:15]:  # Show first 15 users
            status_indicators = []
            if user.is_banned:
                status_indicators.append("🚫")
            if user.is_moderator:
                status_indicators.append("🛡️")
            if user.is_admin:
                status_indicators.append("👑")
            
            status = " ".join(status_indicators) if status_indicators else "✅"
            username = f"@{user.username}" if user.username else f"User_{user.user_id}"
            
            message += f"{status} **{username}** - {user.deals_count} deals\n"
        
        if len(users) > 15:
            message += f"\n*... and {len(users) - 15} more users*"
        
        return message