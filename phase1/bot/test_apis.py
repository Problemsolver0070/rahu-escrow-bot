#!/usr/bin/env python3
"""
Test script to verify API keys and blockchain integration
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our blockchain components
from blockchain import BlockchainAPI, RealWalletGenerator
from models import NetworkType

async def test_api_keys():
    """Test all API keys and blockchain integration"""
    print("🧪 Testing API Keys and Blockchain Integration...")
    print("=" * 60)
    
    # Test wallet generation
    print("\n🔧 Testing Wallet Generation:")
    print("-" * 30)
    
    try:
        # Test BTC wallet generation
        btc_addr, btc_key = RealWalletGenerator.generate_bitcoin_wallet()
        print(f"✅ BTC Wallet: {btc_addr}")
        
        # Test ETH wallet generation
        eth_addr, eth_key = RealWalletGenerator.generate_ethereum_wallet()
        print(f"✅ ETH Wallet: {eth_addr}")
        
        # Test LTC wallet generation
        ltc_addr, ltc_key = RealWalletGenerator.generate_litecoin_wallet()
        print(f"✅ LTC Wallet: {ltc_addr}")
        
        # Test TRON wallet generation
        trx_addr, trx_key = RealWalletGenerator.generate_tron_wallet()
        print(f"✅ TRX Wallet: {trx_addr}")
        
    except Exception as e:
        print(f"❌ Wallet generation failed: {e}")
    
    # Test API connections
    print("\n🌐 Testing API Connections:")
    print("-" * 30)
    
    async with BlockchainAPI() as api:
        # Test Bitcoin API (BlockCypher)
        try:
            btc_balance = await api.get_balance(NetworkType.BTC, "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
            print(f"✅ BTC API: Genesis block balance = {btc_balance} BTC")
        except Exception as e:
            print(f"❌ BTC API failed: {e}")
        
        # Test Ethereum API (Etherscan)
        try:
            eth_balance = await api.get_balance(NetworkType.ETH, "0x742d35Cc6Bb78392F43E57C2A3c70ADa99c52f12")
            print(f"✅ ETH API: Test balance = {eth_balance} ETH")
        except Exception as e:
            print(f"❌ ETH API failed: {e}")
        
        # Test Litecoin API (BlockCypher)
        try:
            ltc_balance = await api.get_balance(NetworkType.LTC, "LdP8Qox1VAhCzLJGqrMKxPFTVEz8CvdCg2")
            print(f"✅ LTC API: Test balance = {ltc_balance} LTC")
        except Exception as e:
            print(f"❌ LTC API failed: {e}")
        
        # Test BSC API (using Etherscan V2 key)
        try:
            bsc_balance = await api.get_balance(NetworkType.USDT_BEP20, "0x742d35Cc6Bb78392F43E57C2A3c70ADa99c52f12")
            print(f"✅ BSC API: Test USDT balance = {bsc_balance} USDT")
        except Exception as e:
            print(f"❌ BSC API failed: {e}")
        
        # Test TRON API (TronGrid)
        try:
            trx_balance = await api.get_balance(NetworkType.USDT_TRC20, "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")
            print(f"✅ TRX API: Test USDT balance = {trx_balance} USDT")
        except Exception as e:
            print(f"❌ TRX API failed: {e}")
    
    print("\n✨ API Integration Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_api_keys())