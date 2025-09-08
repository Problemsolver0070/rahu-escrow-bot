import os
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Set
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
import uuid
import random

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from environment
BOT_TOKEN = "8020772644:AAEF9j8c_iryT931PcQ-E422GegVxD8e2Ak"

# In-memory storage for Phase 0 (fake data)
fake_users: Dict[int, Dict] = {}
fake_deals: Dict[str, Dict] = {}
fake_groups: Dict[str, Dict] = {}
moderators: Set[int] = {123456789, 987654321}  # Fake mod IDs
admin_id = 111222333  # Fake admin ID

class RahuEscrowBot:
    def __init__(self):
        self.application = None
        
    def generate_fake_address(self, crypto):
        """Generate fake addresses for different cryptocurrencies"""
        if crypto == "BTC":
            return f"1{random.choice(['A', 'B', 'C'])}{random.randint(100000, 999999)}fakeBTCDemo"
        elif crypto == "ETH":
            return f"0x{random.randint(100000000, 999999999):x}fakETHDemo"
        elif crypto == "LTC":
            return f"L{random.choice(['t', 'M', 'L'])}{random.randint(100000, 999999)}fakeLTCDemo"
        elif crypto == "USDT_TRC20":
            return f"TR{random.randint(10000000, 99999999)}fakeTRC20Demo"
        elif crypto == "USDT_BEP20":
            return f"0x{random.randint(100000000, 999999999):x}fakeBEP20Demo"
        else:
            return f"DEMO_{crypto}_{random.randint(100000, 999999)}"
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Luxury welcome message with inline buttons"""
        user = update.effective_user
        
        # Store fake user data
        fake_users[user.id] = {
            'username': user.username,
            'first_name': user.first_name,
            'join_date': datetime.now(),
            'deals_count': random.randint(0, 5)
        }
        
        welcome_text = f"""
✨ *Welcome to Rahu Escrow* ✨

🌟 *Premium Multi-Crypto Escrow Service* 🌟

Greetings, {user.first_name}! You've entered the most sophisticated escrow ecosystem on Telegram.

🔰 *Your Elite Features:*
• Multi-cryptocurrency support
• 12-hour private escrow suites  
• Professional dispute resolution
• Premium customer support

💰 *Supported Cryptocurrencies:*
• Bitcoin (BTC)
• Ethereum (ETH) 
• Litecoin (LTC)
• USDT (TRC-20)
• USDT (BEP-20)

💎 *Status:* Verified Member
🛡️ *Security:* Military-grade encryption
⚡ *Response:* Instant processing

*Ready to create your first luxury deal?*
        """
        
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
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Elite help message"""
        help_text = """
🎯 *Rahu Escrow - Elite Support* 🎯

🌟 *For Premium Assistance:*

👨‍💼 **Elite Moderators:**
• @RahuMod1 - Senior Arbitrator
• @RahuMod2 - Dispute Specialist  
• @RahuMod3 - Technical Support

📞 *Contact Priority:*
• VIP Members: < 5 minutes
• Premium: < 15 minutes
• Standard: < 1 hour

⚡ *Emergency Support:* @RahuAdmin

*We're here to serve your escrow needs with luxury service.*
        """
        
        await update.message.reply_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN
        )

    async def rules_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Luxury rules display"""
        rules_text = """
📋 *Rahu Escrow - Premium Rules* 📋

💰 **Fee Structure:**
• Deals ≤ $100: Fixed $5 fee
• Deals > $100: 5% commission
• VIP Members: 20% discount

🌐 **Supported Networks:**
• **Bitcoin (BTC)** - Native blockchain
• **Ethereum (ETH)** - ERC-20 network
• **Litecoin (LTC)** - Native blockchain
• **USDT-TRC20** - Tron network (Recommended)
• **USDT-BEP20** - Binance Smart Chain

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
• BTC: 0.0001 BTC (network fee)
• ETH: Dynamic gas fees
• LTC: 0.001 LTC (network fee)
• USDT-TRC20: Free transfers
• USDT-BEP20: ~$0.50 network fee

*Your security is our luxury promise.*
        """
        
        await update.message.reply_text(
            rules_text,
            parse_mode=ParseMode.MARKDOWN
        )

    async def create_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Create luxury escrow deal"""
        user = update.effective_user
        
        # Generate fake escrow ID
        escrow_id = f"ESCROW-{random.choice(['ABC', 'DEF', 'GHI', 'JKL'])}{random.randint(100, 999)}"
        
        # Create fake group data
        fake_groups[escrow_id] = {
            'creator': user.id,
            'status': 'active',
            'created': datetime.now(),
            'expires': datetime.now() + timedelta(hours=12)
        }
        
        create_text = f"""
✨ *Creating Your Escrow Suite...* ✨

🔄 *Processing...*
• Generating secure group
• Configuring blockchain bridge
• Activating luxury features

⚡ *Ready!*

🏛️ **{escrow_id}** has been created!

🔗 *Private Group:* t.me/RahuEscrow_{escrow_id[-6:]}
⏰ *Valid for:* 12 hours
👥 *Max participants:* 2 users

🌟 *Features Activated:*
• Military-grade encryption
• Real-time notifications
• Professional support
• Dispute protection

*Click the link above to enter your private escrow suite.*
        """
        
        keyboard = [
            [InlineKeyboardButton("🚀 Enter Escrow Suite", url=f"https://t.me/RahuEscrow_Demo")],
            [InlineKeyboardButton("📋 View Deal Rules", callback_data="show_rules")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            create_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    # Fake escrow group commands
    async def buyer_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set buyer address with crypto selection"""
        if not context.args:
            # Show crypto selection if no address provided
            crypto_text = """
🔘 *BUYER Registration* 🔘

Please select your preferred cryptocurrency:

💰 *Choose your network:*
            """
            
            keyboard = [
                [
                    InlineKeyboardButton("₿ Bitcoin (BTC)", callback_data="buyer_crypto_BTC"),
                    InlineKeyboardButton("Ξ Ethereum (ETH)", callback_data="buyer_crypto_ETH")
                ],
                [
                    InlineKeyboardButton("Ł Litecoin (LTC)", callback_data="buyer_crypto_LTC"),
                    InlineKeyboardButton("₮ USDT-TRC20", callback_data="buyer_crypto_USDT_TRC20")
                ],
                [
                    InlineKeyboardButton("₮ USDT-BEP20", callback_data="buyer_crypto_USDT_BEP20")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(crypto_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
            return
            
        # If address provided, assume USDT-TRC20 for backward compatibility
        address = context.args[0]
        
        response_text = f"""
🔘 *Role Assignment: BUYER*

✅ **Address Registered:**
`{address}`

🌐 **Network:** USDT-TRC20 (Default)
🔍 **Verification:** Address format valid
⚡ **Status:** Ready for escrow

*Waiting for seller to register their address...*
        """
        
        await update.message.reply_text(response_text, parse_mode=ParseMode.MARKDOWN)

    async def seller_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set seller address with crypto selection"""
        if not context.args:
            # Show crypto selection if no address provided
            crypto_text = """
🔘 *SELLER Registration* 🔘

Please select your preferred cryptocurrency:

💰 *Choose your network:*
            """
            
            keyboard = [
                [
                    InlineKeyboardButton("₿ Bitcoin (BTC)", callback_data="seller_crypto_BTC"),
                    InlineKeyboardButton("Ξ Ethereum (ETH)", callback_data="seller_crypto_ETH")
                ],
                [
                    InlineKeyboardButton("Ł Litecoin (LTC)", callback_data="seller_crypto_LTC"),
                    InlineKeyboardButton("₮ USDT-TRC20", callback_data="seller_crypto_USDT_TRC20")
                ],
                [
                    InlineKeyboardButton("₮ USDT-BEP20", callback_data="seller_crypto_USDT_BEP20")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(crypto_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
            return
            
        # If address provided, assume USDT-TRC20 for backward compatibility
        address = context.args[0]
        crypto = "USDT-TRC20"
        
        response_text = f"""
🔘 *Role Assignment: SELLER*

✅ **Address Registered:**
`{address}`

🌐 **Network:** {crypto} (Default)
🔍 **Verification:** Address format valid
⚡ **Status:** Ready for escrow

🎯 **Addresses Matched!**

*Generating escrow address...*
        """
        
        # Generate fake escrow details with selected crypto
        escrow_address = self.generate_fake_address(crypto)
        
        details_text = f"""
🏛️ **ESCROW SUITE ACTIVE** 🏛️

📋 *Deal Details:*
• **Escrow ID:** ESCROW-ABC123
• **Network:** {crypto}
• **Buyer:** @{update.effective_user.username}
• **Seller:** @DemoSeller

💳 **Addresses:**
• **Buyer:** `{context.args[0]}`
• **Seller:** `DEMO_SELLER_ADDRESS`

🏦 **Escrow Address:**
`{escrow_address}`

💎 *Send {crypto.split('-')[0] if 'USDT' in crypto else crypto} to the escrow address above*
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📱 Show QR", callback_data="show_qr"),
                InlineKeyboardButton("💰 Check Balance", callback_data="check_balance")
            ],
            [InlineKeyboardButton("🆘 Need Help?", callback_data="get_help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(details_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

    # Moderator commands (fake)
    async def ban_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Fake ban command for mods"""
        user_id = update.effective_user.id
        
        if user_id not in moderators and user_id != admin_id:
            await update.message.reply_text("❌ *Access Denied* - Moderator privileges required", parse_mode=ParseMode.MARKDOWN)
            return
            
        if not context.args:
            await update.message.reply_text("Usage: `/ban @username`", parse_mode=ParseMode.MARKDOWN)
            return
            
        target = context.args[0]
        
        response_text = f"""
🔨 **MODERATION ACTION**

✅ User {target} has been banned
🛡️ Action by: @{update.effective_user.username}
⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

*User removed from all active escrow deals.*
        """
        
        await update.message.reply_text(response_text, parse_mode=ParseMode.MARKDOWN)

    async def freeze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Fake freeze command"""
        user_id = update.effective_user.id
        
        if user_id not in moderators and user_id != admin_id:
            await update.message.reply_text("❌ *Access Denied*", parse_mode=ParseMode.MARKDOWN)
            return
            
        if not context.args:
            await update.message.reply_text("Usage: `/freeze ESCROW-ID`", parse_mode=ParseMode.MARKDOWN)
            return
            
        escrow_id = context.args[0]
        
        response_text = f"""
❄️ **DEAL FROZEN**

🆔 **Escrow:** {escrow_id}
🛡️ **Action by:** @{update.effective_user.username}
⏰ **Time:** {datetime.now().strftime('%H:%M:%S')}

*All transactions suspended pending investigation.*
        """
        
        await update.message.reply_text(response_text, parse_mode=ParseMode.MARKDOWN)

    # Callback handlers
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "create_deal":
            await query.edit_message_text(
                "✨ *Deal Creation Process* ✨\n\nUse `/create` command to generate your private escrow suite.",
                parse_mode=ParseMode.MARKDOWN
            )
            
        elif query.data == "show_rules":
            await self.rules_command(update, context)
            
        elif query.data == "get_help":
            await self.help_command(update, context)
            
        elif query.data == "show_qr":
            await query.edit_message_text(
                "📱 *QR Code Generated*\n\n[QR Code would be displayed here]\n\n*Scan to send crypto to escrow address*",
                parse_mode=ParseMode.MARKDOWN
            )
            
        elif query.data == "check_balance":
            balance = random.uniform(0, 1000)
            await query.edit_message_text(
                f"💰 *Escrow Balance*\n\n**Current:** ${balance:.2f} USD\n⏰ *Last updated:* {datetime.now().strftime('%H:%M:%S')}",
                parse_mode=ParseMode.MARKDOWN
            )
            
        # Handle cryptocurrency selection for buyer
        elif query.data.startswith("buyer_crypto_"):
            crypto = query.data.replace("buyer_crypto_", "").replace("_", "-")
            crypto_symbols = {
                "BTC": "₿",
                "ETH": "Ξ", 
                "LTC": "Ł",
                "USDT-TRC20": "₮",
                "USDT-BEP20": "₮"
            }
            
            response_text = f"""
🔘 *BUYER - {crypto_symbols.get(crypto, '💰')} {crypto} Selected*

Please send your {crypto} address using:
`/buyer YOUR_{crypto.replace('-', '_')}_ADDRESS`

📝 *Example formats:*
• **BTC:** `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`
• **ETH:** `0x742d35Cc6Bb78392F43E57C2A3c70ADa99c52f12`
• **LTC:** `LdP8Qox1VAhCzLJGqrMKxPFTVEz8CvdCg2`
• **USDT-TRC20:** `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t`
• **USDT-BEP20:** `0x742d35Cc6Bb78392F43E57C2A3c70ADa99c52f12`

🔍 *We'll verify the address format automatically*
            """
            
            await query.edit_message_text(response_text, parse_mode=ParseMode.MARKDOWN)
            
        # Handle cryptocurrency selection for seller
        elif query.data.startswith("seller_crypto_"):
            crypto = query.data.replace("seller_crypto_", "").replace("_", "-")
            crypto_symbols = {
                "BTC": "₿",
                "ETH": "Ξ", 
                "LTC": "Ł",
                "USDT-TRC20": "₮",
                "USDT-BEP20": "₮"
            }
            
            response_text = f"""
🔘 *SELLER - {crypto_symbols.get(crypto, '💰')} {crypto} Selected*

Please send your {crypto} address using:
`/seller YOUR_{crypto.replace('-', '_')}_ADDRESS`

📝 *Example formats:*
• **BTC:** `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`
• **ETH:** `0x742d35Cc6Bb78392F43E57C2A3c70ADa99c52f12`
• **LTC:** `LdP8Qox1VAhCzLJGqrMKxPFTVEz8CvdCg2`
• **USDT-TRC20:** `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t`
• **USDT-BEP20:** `0x742d35Cc6Bb78392F43E57C2A3c70ADa99c52f12`

🔍 *We'll verify the address format and generate escrow*
            """
            
            await query.edit_message_text(response_text, parse_mode=ParseMode.MARKDOWN)

    async def simulate_funding(self, context: ContextTypes.DEFAULT_TYPE):
        """Simulate escrow funding notification for multiple cryptos"""
        crypto_options = ["BTC", "ETH", "LTC", "USDT-TRC20", "USDT-BEP20"]
        selected_crypto = random.choice(crypto_options)
        
        amounts = {
            "BTC": f"{random.uniform(0.001, 0.1):.6f} BTC",
            "ETH": f"{random.uniform(0.05, 5.0):.4f} ETH", 
            "LTC": f"{random.uniform(1, 100):.2f} LTC",
            "USDT-TRC20": f"{random.uniform(50, 1000):.2f} USDT",
            "USDT-BEP20": f"{random.uniform(50, 1000):.2f} USDT"
        }
        
        tx_prefixes = {
            "BTC": "a1b2c3d4e5f6",
            "ETH": "0xabc123def456", 
            "LTC": "c4d5e6f7a8b9",
            "USDT-TRC20": "tr789abc123def",
            "USDT-BEP20": "0x123abc456def"
        }
        
        funding_text = f"""
🚨 **THE ESCROW HAS BEEN FUNDED!** 🚨

💰 **Amount:** {amounts[selected_crypto]}
🌐 **Network:** {selected_crypto}
🔗 **TX Hash:** {tx_prefixes[selected_crypto]}...demo_transaction
⏰ **Confirmed:** 3/3 blocks

🎯 **Next Steps:**
• Buyer: Complete your side of the deal
• Seller: Await buyer confirmation

*Funds are secure in escrow. Choose your action below.*
        """
        
        keyboard = [
            [
                InlineKeyboardButton("✅ Release to Seller", callback_data="release_funds"),
                InlineKeyboardButton("↩️ Refund Buyer", callback_data="refund_buyer")
            ],
            [InlineKeyboardButton("⚖️ Raise Dispute", callback_data="raise_dispute")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # This would be sent to the escrow group
        # For demo purposes, we'll just log it
        logger.info(f"Funding notification sent to escrow group for {selected_crypto}")

    def setup_handlers(self):
        """Setup all command and callback handlers"""
        # Basic commands
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("rules", self.rules_command))
        self.application.add_handler(CommandHandler("create", self.create_command))
        
        # Escrow commands
        self.application.add_handler(CommandHandler("buyer", self.buyer_command))
        self.application.add_handler(CommandHandler("seller", self.seller_command))
        
        # Moderation commands
        self.application.add_handler(CommandHandler("ban", self.ban_command))
        self.application.add_handler(CommandHandler("freeze", self.freeze_command))
        
        # Callback handlers
        self.application.add_handler(CallbackQueryHandler(self.button_handler))

    async def setup_bot_commands(self):
        """Set bot commands menu"""
        commands = [
            BotCommand("start", "🌟 Welcome to Rahu Escrow"),
            BotCommand("create", "🆕 Create new escrow deal"),
            BotCommand("help", "🙋 Get premium support"),
            BotCommand("rules", "📋 View escrow rules"),
            BotCommand("buyer", "🔘 Set buyer address"),
            BotCommand("seller", "🔘 Set seller address"),
        ]
        
        await self.application.bot.set_my_commands(commands)

    async def run(self):
        """Run the bot"""
        # Create application
        self.application = Application.builder().token(BOT_TOKEN).build()
        
        # Setup handlers
        self.setup_handlers()
        
        # Set bot commands
        await self.setup_bot_commands()
        
        # Start polling
        logger.info("🚀 Rahu Escrow Bot starting...")
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        
        # Keep running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Bot stopping...")
        finally:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()

async def main():
    """Main function"""
    bot = RahuEscrowBot()
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())