"""
Real Blockchain Integration for Rahu Escrow Bot
Production-grade multi-chain support with free APIs
"""

import os
import asyncio
import aiohttp
import json
import logging
from typing import Dict, Optional, Tuple, List
from datetime import datetime, timedelta
from decimal import Decimal
import hashlib
import hmac
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import secrets
import base58
import binascii

from models import NetworkType

logger = logging.getLogger(__name__)

class BlockchainAPI:
    """Real blockchain API integration with free services"""
    
    # Free API endpoints
    APIS = {
        NetworkType.BTC: {
            "base_url": "https://api.blockcypher.com/v1/btc/main",
            "rate_limit": 3,  # requests per second
            "hourly_limit": 200
        },
        NetworkType.LTC: {
            "base_url": "https://api.blockcypher.com/v1/ltc/main", 
            "rate_limit": 3,
            "hourly_limit": 200
        },
        NetworkType.ETH: {
            "base_url": "https://api.etherscan.io/api",
            "rate_limit": 5,
            "hourly_limit": 100000,
            "api_key": os.getenv("ETHERSCAN_API_KEY", "YourApiKeyToken")
        },
        NetworkType.USDT_BEP20: {
            "base_url": "https://api.bscscan.com/api",
            "rate_limit": 5,
            "hourly_limit": 100000,
            "api_key": os.getenv("BSCSCAN_API_KEY", "YourApiKeyToken"),
            "contract": "0x55d398326f99059fF775485246999027B3197955"  # USDT BSC contract
        },
        NetworkType.USDT_TRC20: {
            "base_url": "https://api.trongrid.io",
            "rate_limit": 100,  # Very generous
            "contract": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"  # USDT TRC20 contract
        }
    }
    
    def __init__(self):
        self.session = None
        self.rate_limiters = {}
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def _make_request(self, network: NetworkType, endpoint: str, params: dict = None) -> dict:
        """Make rate-limited API request"""
        if not self.session:
            raise RuntimeError("BlockchainAPI must be used as async context manager")
        
        api_config = self.APIS[network]
        base_url = api_config["base_url"]
        
        # Add API key if required
        if "api_key" in api_config:
            if params is None:
                params = {}
            params["apikey"] = api_config["api_key"]
        
        # Rate limiting (simple implementation)
        await asyncio.sleep(1.0 / api_config["rate_limit"])
        
        url = f"{base_url}/{endpoint}" if not endpoint.startswith("http") else endpoint
        
        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"API error {response.status}: {await response.text()}")
                    return {}
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return {}
    
    async def get_balance(self, network: NetworkType, address: str) -> Decimal:
        """Get real balance for address"""
        try:
            if network == NetworkType.BTC:
                data = await self._make_request(network, f"addrs/{address}/balance")
                balance = data.get("balance", 0)
                return Decimal(balance) / Decimal("100000000")  # Convert satoshi to BTC
                
            elif network == NetworkType.LTC:
                data = await self._make_request(network, f"addrs/{address}/balance")
                balance = data.get("balance", 0)
                return Decimal(balance) / Decimal("100000000")  # Convert litoshi to LTC
                
            elif network == NetworkType.ETH:
                params = {
                    "module": "account",
                    "action": "balance", 
                    "address": address,
                    "tag": "latest"
                }
                data = await self._make_request(network, "", params)
                balance = data.get("result", "0")
                return Decimal(balance) / Decimal("1000000000000000000")  # Convert wei to ETH
                
            elif network == NetworkType.USDT_BEP20:
                params = {
                    "module": "account",
                    "action": "tokenbalance",
                    "contractaddress": self.APIS[network]["contract"],
                    "address": address,
                    "tag": "latest"
                }
                data = await self._make_request(network, "", params)
                balance = data.get("result", "0")
                return Decimal(balance) / Decimal("1000000000000000000")  # Convert to USDT
                
            elif network == NetworkType.USDT_TRC20:
                # TronGrid API for USDT TRC20
                endpoint = f"v1/accounts/{address}"
                data = await self._make_request(network, endpoint)
                
                # Check TRC20 tokens
                trc20_tokens = data.get("data", [{}])[0].get("trc20", [])
                for token in trc20_tokens:
                    if token.get("token_contract") == self.APIS[network]["contract"]:
                        balance = token.get("balance", "0")
                        return Decimal(balance) / Decimal("1000000")  # USDT has 6 decimals
                
                return Decimal("0")
                
        except Exception as e:
            logger.error(f"Failed to get balance for {network}: {e}")
            return Decimal("0")
    
    async def get_transactions(self, network: NetworkType, address: str, limit: int = 10) -> List[dict]:
        """Get recent transactions for address"""
        try:
            if network == NetworkType.BTC:
                data = await self._make_request(network, f"addrs/{address}")
                return data.get("txrefs", [])[:limit]
                
            elif network == NetworkType.LTC:
                data = await self._make_request(network, f"addrs/{address}")
                return data.get("txrefs", [])[:limit]
                
            elif network == NetworkType.ETH:
                params = {
                    "module": "account",
                    "action": "txlist",
                    "address": address,
                    "startblock": 0,
                    "endblock": 99999999,
                    "sort": "desc",
                    "page": 1,
                    "offset": limit
                }
                data = await self._make_request(network, "", params)
                return data.get("result", [])
                
            elif network == NetworkType.USDT_BEP20:
                params = {
                    "module": "account", 
                    "action": "tokentx",
                    "contractaddress": self.APIS[network]["contract"],
                    "address": address,
                    "sort": "desc",
                    "page": 1,
                    "offset": limit
                }
                data = await self._make_request(network, "", params)
                return data.get("result", [])
                
            elif network == NetworkType.USDT_TRC20:
                endpoint = f"v1/accounts/{address}/transactions/trc20"
                params = {"limit": limit}
                data = await self._make_request(network, endpoint, params)
                return data.get("data", [])
                
        except Exception as e:
            logger.error(f"Failed to get transactions for {network}: {e}")
            return []
    
    async def check_transaction(self, network: NetworkType, tx_hash: str) -> dict:
        """Check specific transaction status"""
        try:
            if network in [NetworkType.BTC, NetworkType.LTC]:
                data = await self._make_request(network, f"txs/{tx_hash}")
                return {
                    "confirmed": data.get("confirmations", 0) >= 3,
                    "confirmations": data.get("confirmations", 0),
                    "amount": Decimal(data.get("total", 0)) / Decimal("100000000"),
                    "timestamp": data.get("confirmed", "")
                }
                
            elif network == NetworkType.ETH:
                params = {
                    "module": "proxy",
                    "action": "eth_getTransactionByHash",
                    "txhash": tx_hash
                }
                data = await self._make_request(network, "", params)
                result = data.get("result", {})
                
                return {
                    "confirmed": result.get("blockNumber") is not None,
                    "amount": Decimal(int(result.get("value", "0"), 16)) / Decimal("1000000000000000000"),
                    "to": result.get("to"),
                    "from": result.get("from")
                }
                
            elif network in [NetworkType.USDT_BEP20, NetworkType.USDT_TRC20]:
                # Similar implementation for token transactions
                return {"confirmed": False, "amount": Decimal("0")}
                
        except Exception as e:
            logger.error(f"Failed to check transaction {tx_hash}: {e}")
            return {"confirmed": False, "amount": Decimal("0")}

class RealWalletGenerator:
    """Production-grade wallet generation with real cryptography"""
    
    @staticmethod
    def generate_bitcoin_wallet() -> Tuple[str, str]:
        """Generate real Bitcoin wallet"""
        try:
            # Generate private key (32 random bytes)
            private_key_bytes = secrets.token_bytes(32)
            
            # Create public key using secp256k1
            private_key = ec.derive_private_key(
                int.from_bytes(private_key_bytes, 'big'),
                ec.SECP256K1()
            )
            public_key = private_key.public_key()
            
            # Get public key coordinates
            public_key_bytes = public_key.public_numbers().x.to_bytes(32, 'big')
            public_key_bytes += public_key.public_numbers().y.to_bytes(32, 'big')
            
            # Create Bitcoin address (P2PKH)
            public_key_compressed = b'\x02' if public_key.public_numbers().y % 2 == 0 else b'\x03'
            public_key_compressed += public_key.public_numbers().x.to_bytes(32, 'big')
            
            # Hash160 (SHA256 then RIPEMD160)
            sha256_hash = hashlib.sha256(public_key_compressed).digest()
            ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
            
            # Add version byte (0x00 for mainnet)
            versioned_hash = b'\x00' + ripemd160_hash
            
            # Double SHA256 for checksum
            checksum = hashlib.sha256(hashlib.sha256(versioned_hash).digest()).digest()[:4]
            
            # Create final address
            address_bytes = versioned_hash + checksum
            address = base58.b58encode(address_bytes).decode('utf-8')
            
            # WIF private key
            extended_key = b'\x80' + private_key_bytes + b'\x01'  # compressed
            checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]
            wif_key = base58.b58encode(extended_key + checksum).decode('utf-8')
            
            return address, wif_key
            
        except Exception as e:
            logger.error(f"Failed to generate Bitcoin wallet: {e}")
            return None, None
    
    @staticmethod
    def generate_ethereum_wallet() -> Tuple[str, str]:
        """Generate real Ethereum wallet"""
        try:
            # Simple approach using secrets
            private_key_bytes = secrets.token_bytes(32)
            
            # Generate private key object
            private_key = ec.derive_private_key(
                int.from_bytes(private_key_bytes, 'big'), 
                ec.SECP256K1()
            )
            
            # Get public key point
            public_key = private_key.public_key()
            public_numbers = public_key.public_numbers()
            
            # Convert to uncompressed format (64 bytes)
            x_bytes = public_numbers.x.to_bytes(32, 'big')
            y_bytes = public_numbers.y.to_bytes(32, 'big')
            public_key_bytes = x_bytes + y_bytes
            
            # Keccak256 hash
            from Crypto.Hash import keccak
            keccak_hasher = keccak.new(digest_bits=256)
            keccak_hasher.update(public_key_bytes)
            keccak_hash = keccak_hasher.digest()
            
            # Take last 20 bytes as address
            address = '0x' + keccak_hash[-20:].hex()
            
            # Private key as hex
            private_key_hex = '0x' + private_key_bytes.hex()
            
            return address, private_key_hex
            
        except Exception as e:
            print(f"Failed to generate Ethereum wallet: {e}")
            import traceback
            traceback.print_exc()
            return None, None
    
    @staticmethod
    def generate_litecoin_wallet() -> Tuple[str, str]:
        """Generate real Litecoin wallet (similar to Bitcoin but different version bytes)"""
        try:
            # Similar to Bitcoin but with Litecoin version bytes
            private_key_bytes = secrets.token_bytes(32)
            
            private_key = ec.derive_private_key(
                int.from_bytes(private_key_bytes, 'big'),
                ec.SECP256K1()
            )
            public_key = private_key.public_key()
            
            # Compressed public key
            public_key_compressed = b'\x02' if public_key.public_numbers().y % 2 == 0 else b'\x03'
            public_key_compressed += public_key.public_numbers().x.to_bytes(32, 'big')
            
            # Hash160
            sha256_hash = hashlib.sha256(public_key_compressed).digest()
            ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
            
            # Litecoin version byte (0x30 for mainnet P2PKH)
            versioned_hash = b'\x30' + ripemd160_hash
            
            # Checksum
            checksum = hashlib.sha256(hashlib.sha256(versioned_hash).digest()).digest()[:4]
            
            # Final address
            address_bytes = versioned_hash + checksum
            address = base58.b58encode(address_bytes).decode('utf-8')
            
            # WIF private key (Litecoin uses 0xB0)
            extended_key = b'\xB0' + private_key_bytes + b'\x01'
            checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]
            wif_key = base58.b58encode(extended_key + checksum).decode('utf-8')
            
            return address, wif_key
            
        except Exception as e:
            logger.error(f"Failed to generate Litecoin wallet: {e}")
            return None, None
    
    @staticmethod
    def generate_tron_wallet() -> Tuple[str, str]:
        """Generate real TRON wallet"""
        try:
            # Simple approach using secrets
            private_key_bytes = secrets.token_bytes(32)
            
            # Generate private key object
            private_key = ec.derive_private_key(
                int.from_bytes(private_key_bytes, 'big'), 
                ec.SECP256K1()
            )
            
            # Get public key point
            public_key = private_key.public_key()
            public_numbers = public_key.public_numbers()
            
            # Convert to uncompressed format (64 bytes)
            x_bytes = public_numbers.x.to_bytes(32, 'big')
            y_bytes = public_numbers.y.to_bytes(32, 'big')
            public_key_bytes = x_bytes + y_bytes
            
            # Keccak256 hash
            from Crypto.Hash import keccak
            keccak_hasher = keccak.new(digest_bits=256)
            keccak_hasher.update(public_key_bytes)
            keccak_hash = keccak_hasher.digest()
            
            # Take last 20 bytes and add TRON prefix (0x41)
            address_bytes = b'\x41' + keccak_hash[-20:]
            
            # Double SHA256 for checksum
            checksum = hashlib.sha256(hashlib.sha256(address_bytes).digest()).digest()[:4]
            
            # Base58 encode
            address = base58.b58encode(address_bytes + checksum).decode('utf-8')
            
            # Private key as hex
            private_key_hex = private_key_bytes.hex()
            
            return address, private_key_hex
            
        except Exception as e:
            print(f"Failed to generate TRON wallet: {e}")
            import traceback
            traceback.print_exc()
            return None, None

class RealEscrowWalletManager:
    """Production escrow wallet management"""
    
    def __init__(self):
        self.blockchain_api = BlockchainAPI()
    
    async def generate_escrow_wallet(self, network: NetworkType, deal_id: str) -> Tuple[Optional[str], Optional[str]]:
        """Generate real escrow wallet for network"""
        try:
            if network == NetworkType.BTC:
                return RealWalletGenerator.generate_bitcoin_wallet()
            elif network == NetworkType.LTC:
                return RealWalletGenerator.generate_litecoin_wallet()
            elif network in [NetworkType.ETH, NetworkType.USDT_BEP20]:
                return RealWalletGenerator.generate_ethereum_wallet()
            elif network == NetworkType.USDT_TRC20:
                return RealWalletGenerator.generate_tron_wallet()
            else:
                logger.error(f"Unsupported network: {network}")
                return None, None
                
        except Exception as e:
            logger.error(f"Failed to generate escrow wallet: {e}")
            return None, None
    
    async def check_funding(self, network: NetworkType, address: str, expected_amount: Decimal = None) -> dict:
        """Check if escrow wallet has been funded"""
        try:
            async with self.blockchain_api as api:
                balance = await api.get_balance(network, address)
                transactions = await api.get_transactions(network, address, 5)
                
                # Check for recent deposits
                recent_deposits = []
                for tx in transactions:
                    # Parse transaction based on network
                    if network in [NetworkType.BTC, NetworkType.LTC]:
                        if tx.get("tx_output_n", -1) >= 0:  # Incoming transaction
                            amount = Decimal(tx.get("value", 0)) / Decimal("100000000")
                            recent_deposits.append({
                                "tx_hash": tx.get("tx_hash"),
                                "amount": amount,
                                "confirmations": tx.get("confirmations", 0),
                                "confirmed": tx.get("confirmations", 0) >= 3
                            })
                    elif network == NetworkType.ETH:
                        if tx.get("to", "").lower() == address.lower():
                            amount = Decimal(tx.get("value", "0")) / Decimal("1000000000000000000")
                            recent_deposits.append({
                                "tx_hash": tx.get("hash"),
                                "amount": amount,
                                "confirmed": True  # Etherscan only returns confirmed txs
                            })
                
                return {
                    "funded": balance > 0,
                    "balance": balance,
                    "deposits": recent_deposits,
                    "network": network.value
                }
                
        except Exception as e:
            logger.error(f"Failed to check funding: {e}")
            return {"funded": False, "balance": Decimal("0"), "deposits": [], "network": network.value}
    
    async def monitor_address(self, network: NetworkType, address: str, callback_func=None) -> bool:
        """Start monitoring address for incoming transactions"""
        try:
            logger.info(f"Starting monitoring for {network.value} address: {address}")
            
            # For production, this would run in a background task
            # For now, we'll implement polling-based monitoring
            while True:
                funding_status = await self.check_funding(network, address)
                
                if funding_status["funded"] and callback_func:
                    await callback_func(address, funding_status)
                    break
                
                # Check every 30 seconds
                await asyncio.sleep(30)
                
        except Exception as e:
            logger.error(f"Failed to monitor address: {e}")
            return False

# Global instance
real_wallet_manager = RealEscrowWalletManager()