#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Secure configuration module for storing sensitive API keys.
Provides basic obfuscation for API keys without external dependencies.
"""

import os
import json
import base64
import hashlib
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class SecureLLMConfig:
    """Secure storage for LLM API keys using native Python libraries"""
    
    def __init__(self):
        # Config path - stored securely in user's home directory
        self.config_dir = os.path.join(os.path.expanduser("~"), ".audio_to_topics")
        self.config_path = os.path.join(self.config_dir, "llm_config.enc")
        
        # Create directory if it doesn't exist
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Default values
        self.anthropic_key = ""
        self.openai_key = ""
        self.provider = "anthropic"
        self.temperature = 0.7
        self.max_tokens = 1000
    
    def _get_key(self, password: str = "audio2topics") -> bytes:
        """Generate a simple encryption key from password"""
        # Ensure password is not None
        if password is None:
            password = "audio2topics"
            
        # Use a salt that's specific to this application
        salt = b"AudioToTopics_2024"
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    
    def _simple_encrypt(self, data: str, key: bytes) -> bytes:
        """Simple XOR-based encryption with key stretching"""
        # Validate inputs
        if data is None:
            data = ""
        if key is None or len(key) == 0:
            logger.error("Invalid encryption key")
            return b""
            
        # Convert data to bytes
        data_bytes = data.encode()
        
        # Create a repeating key to match data length
        full_key = (key * (len(data_bytes) // len(key) + 1))[:len(data_bytes)]
        
        # XOR each byte
        encrypted = bytes(a ^ b for a, b in zip(data_bytes, full_key))
        
        # Base64 encode for storage
        return base64.b64encode(encrypted)
    
    def _simple_decrypt(self, encrypted_data: bytes, key: bytes) -> str:
        """Simple XOR-based decryption"""
        try:
            # Validate inputs
            if encrypted_data is None or len(encrypted_data) == 0:
                return ""
            if key is None or len(key) == 0:
                logger.error("Invalid decryption key")
                return ""
                
            # Base64 decode
            data_bytes = base64.b64decode(encrypted_data)
            
            # Create a repeating key to match data length
            full_key = (key * (len(data_bytes) // len(key) + 1))[:len(data_bytes)]
            
            # XOR each byte to decrypt
            decrypted = bytes(a ^ b for a, b in zip(data_bytes, full_key))
            
            # Convert back to string
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Error decrypting data: {str(e)}")
            return ""
    
    def load(self, master_password: Optional[str] = None) -> bool:
        """Load and decrypt API keys from config file"""
        try:
            if not os.path.exists(self.config_path):
                logger.info("No config file found, using default values")
                return False
                
            key = self._get_key(master_password)
            
            with open(self.config_path, 'rb') as f:
                encrypted_data = f.read()
                
            decrypted_json = self._simple_decrypt(encrypted_data, key)
            if not decrypted_json:
                return False
                
            config = json.loads(decrypted_json)
            
            self.anthropic_key = config.get('anthropic_key', '')
            self.openai_key = config.get('openai_key', '')
            self.provider = config.get('provider', 'anthropic')
            self.temperature = config.get('temperature', 0.7)
            self.max_tokens = config.get('max_tokens', 1000)
            
            return True
        except Exception as e:
            logger.error(f"Error loading encrypted config: {str(e)}")
            return False
            
    def save(self, anthropic_key: str, openai_key: str, provider: str,
             temperature: Optional[float] = None, max_tokens: Optional[int] = None,
             master_password: Optional[str] = None) -> bool:
        """Encrypt and save API keys to config file"""
        try:
            # Validate inputs
            if anthropic_key is None:
                anthropic_key = ""
            if openai_key is None:
                openai_key = ""
            if provider is None:
                provider = "anthropic"
                
            # Update values if provided
            if temperature is not None:
                self.temperature = temperature
            if max_tokens is not None:
                self.max_tokens = max_tokens
                
            config = {
                'anthropic_key': anthropic_key,
                'openai_key': openai_key,
                'provider': provider,
                'temperature': self.temperature,
                'max_tokens': self.max_tokens
            }
            
            # Update current instance
            self.anthropic_key = anthropic_key
            self.openai_key = openai_key
            self.provider = provider
            
            # Encrypt the data
            key = self._get_key(master_password)
            if key is None:
                logger.error("Failed to generate encryption key")
                return False
                
            json_data = json.dumps(config)
            encrypted_data = self._simple_encrypt(json_data, key)
            
            if not encrypted_data:
                logger.error("Failed to encrypt data")
                return False
                
            with open(self.config_path, 'wb') as f:
                f.write(encrypted_data)
                
            # Secure the config file permissions (on Unix systems)
            try:
                os.chmod(self.config_path, 0o600)  # Read/write for owner only
            except Exception:
                pass  # Ignore on Windows
                
            logger.info(f"Successfully saved encrypted config to {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving encrypted config: {str(e)}")
            return False
            
    def is_configured(self) -> bool:
        """Check if the service is configured with API keys"""
        if self.provider == "anthropic":
            return bool(self.anthropic_key)
        else:  # openai
            return bool(self.openai_key)
            
    def clear(self) -> bool:
        """Clear saved API keys"""
        try:
            if os.path.exists(self.config_path):
                os.remove(self.config_path)
            
            self.anthropic_key = ""
            self.openai_key = ""
            
            return True
        except Exception as e:
            logger.error(f"Error clearing config: {str(e)}")
            return False