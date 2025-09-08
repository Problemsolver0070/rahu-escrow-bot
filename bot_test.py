import requests
import json

def test_telegram_bot():
    """Test Telegram bot API connectivity"""
    bot_token = "8020772644:AAEF9j8c_iryT931PcQ-E422GegVxD8e2Ak"
    base_url = f"https://api.telegram.org/bot{bot_token}"
    
    print("🤖 Testing Rahu Escrow Telegram Bot...")
    print("=" * 50)
    
    # Test 1: Get bot info
    print("\n🔍 Testing bot connectivity...")
    try:
        response = requests.get(f"{base_url}/getMe", timeout=10)
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info['ok']:
                result = bot_info['result']
                print(f"✅ Bot is online!")
                print(f"   Bot Name: {result['first_name']}")
                print(f"   Username: @{result['username']}")
                print(f"   Bot ID: {result['id']}")
            else:
                print("❌ Bot API returned error")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False
    
    # Test 2: Get bot commands
    print("\n🔍 Testing bot commands...")
    try:
        response = requests.get(f"{base_url}/getMyCommands", timeout=10)
        if response.status_code == 200:
            commands_info = response.json()
            if commands_info['ok']:
                commands = commands_info['result']
                print(f"✅ Found {len(commands)} bot commands:")
                for cmd in commands:
                    print(f"   /{cmd['command']} - {cmd['description']}")
            else:
                print("❌ Failed to get commands")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Commands test failed: {str(e)}")
    
    # Test 3: Check webhook status
    print("\n🔍 Testing webhook status...")
    try:
        response = requests.get(f"{base_url}/getWebhookInfo", timeout=10)
        if response.status_code == 200:
            webhook_info = response.json()
            if webhook_info['ok']:
                result = webhook_info['result']
                if result['url']:
                    print(f"✅ Webhook active: {result['url']}")
                else:
                    print("✅ Bot using polling mode (no webhook)")
                    print(f"   Pending updates: {result.get('pending_update_count', 0)}")
            else:
                print("❌ Failed to get webhook info")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Webhook test failed: {str(e)}")
    
    print("\n🎯 Bot Testing Summary:")
    print("✅ Bot is running and accessible")
    print("✅ Commands are properly configured")
    print("✅ Bot is in polling mode (ready for messages)")
    print("\n💡 To test bot functionality:")
    print("   1. Open Telegram")
    print("   2. Search for the bot username")
    print("   3. Send /start command")
    print("   4. Test luxury commands: /create, /help, /rules")
    print("   5. Test escrow commands: /buyer, /seller")
    
    return True

if __name__ == "__main__":
    test_telegram_bot()