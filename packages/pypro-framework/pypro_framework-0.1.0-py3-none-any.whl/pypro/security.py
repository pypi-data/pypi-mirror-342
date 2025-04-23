"""
Security module for PyPro.

This module provides security features like password hashing,
token generation and verification, and CSRF protection.
"""

import os
import hmac
import hashlib
import base64
import json
import time
import random
import string
from typing import Dict, Any, Optional, Union, Tuple

# Default security settings
DEFAULT_PBKDF2_ITERATIONS = 150000  # Recommended minimum as of 2023
DEFAULT_SALT_SIZE = 16  # 16 bytes = 128 bits
DEFAULT_KEY_LENGTH = 32  # 32 bytes = 256 bits
DEFAULT_TOKEN_EXPIRY = 3600  # 1 hour


def generate_password_hash(password: str, salt_size: int = DEFAULT_SALT_SIZE,
                           iterations: int = DEFAULT_PBKDF2_ITERATIONS) -> str:
    """
    Hash a password using PBKDF2 with HMAC-SHA256.
    
    Args:
        password: The password to hash
        salt_size: Size of the salt in bytes
        iterations: Number of iterations for PBKDF2
        
    Returns:
        String representation of the hash in the format:
        algorithm$iterations$salt$hash
    """
    # Generate a random salt
    salt = os.urandom(salt_size)
    
    # Hash the password using PBKDF2
    password_hash = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt, 
        iterations,
        dklen=DEFAULT_KEY_LENGTH
    )
    
    # Format the components for storage
    algorithm = 'pbkdf2:sha256'
    salt_b64 = base64.b64encode(salt).decode('ascii')
    hash_b64 = base64.b64encode(password_hash).decode('ascii')
    
    return f"{algorithm}${iterations}${salt_b64}${hash_b64}"


def check_password_hash(password_hash: str, password: str) -> bool:
    """
    Verify a password against a hash.
    
    Args:
        password_hash: The stored hash
        password: The password to check
        
    Returns:
        True if the password matches, False otherwise
    """
    try:
        # Parse the hash components
        algorithm, iterations, salt_b64, hash_b64 = password_hash.split('$')
        
        # Check algorithm
        if not algorithm.startswith('pbkdf2:'):
            return False
            
        # Get hash parameters
        hash_algo = algorithm.split(':')[1]
        iterations = int(iterations)
        salt = base64.b64decode(salt_b64)
        stored_hash = base64.b64decode(hash_b64)
        
        # Generate hash from the input password
        password_hash = hashlib.pbkdf2_hmac(
            hash_algo,
            password.encode('utf-8'),
            salt,
            iterations,
            dklen=len(stored_hash)
        )
        
        # Compare hashes using constant-time comparison
        return hmac.compare_digest(password_hash, stored_hash)
        
    except (ValueError, IndexError, TypeError):
        # Invalid hash format
        return False


def create_token(data: Dict[str, Any], secret_key: str, 
                 expires_in: int = DEFAULT_TOKEN_EXPIRY) -> str:
    """
    Create a signed token with expiration.
    
    Args:
        data: Data to encode in the token
        secret_key: Secret key for signing
        expires_in: Token validity in seconds
        
    Returns:
        Base64-encoded token string
    """
    # Prepare payload with expiration
    payload = {
        'data': data,
        'exp': int(time.time()) + expires_in
    }
    
    # Convert payload to JSON and encode
    payload_bytes = json.dumps(payload).encode('utf-8')
    payload_b64 = base64.urlsafe_b64encode(payload_bytes).decode('ascii').rstrip('=')
    
    # Create signature
    signature = hmac.new(
        secret_key.encode('utf-8'),
        payload_b64.encode('ascii'),
        hashlib.sha256
    ).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode('ascii').rstrip('=')
    
    # Combine into token
    return f"{payload_b64}.{signature_b64}"


def verify_token(token: str, secret_key: str) -> Optional[Dict[str, Any]]:
    """
    Verify and decode a token.
    
    Args:
        token: The token to verify
        secret_key: Secret key for verification
        
    Returns:
        The decoded data if the token is valid, None otherwise
    """
    try:
        # Split token into parts
        if '.' not in token:
            return None
            
        payload_b64, signature_b64 = token.split('.')
        
        # Verify signature
        expected_signature = hmac.new(
            secret_key.encode('utf-8'),
            payload_b64.encode('ascii'),
            hashlib.sha256
        ).digest()
        
        # Add back padding if needed
        signature_b64_padded = signature_b64 + '=' * (-len(signature_b64) % 4)
        received_signature = base64.urlsafe_b64decode(signature_b64_padded)
        
        if not hmac.compare_digest(expected_signature, received_signature):
            return None
            
        # Decode payload
        payload_b64_padded = payload_b64 + '=' * (-len(payload_b64) % 4)
        payload_bytes = base64.urlsafe_b64decode(payload_b64_padded)
        payload = json.loads(payload_bytes.decode('utf-8'))
        
        # Check expiration
        if 'exp' in payload and payload['exp'] < time.time():
            return None
            
        return payload['data']
    
    except (ValueError, KeyError, json.JSONDecodeError, TypeError):
        return None


def generate_csrf_token() -> str:
    """
    Generate a random CSRF token.
    
    Returns:
        Random token string
    """
    # Generate 32 random bytes
    random_bytes = os.urandom(32)
    return base64.urlsafe_b64encode(random_bytes).decode('ascii').rstrip('=')


def validate_csrf(request_token: str, session_token: str) -> bool:
    """
    Validate a CSRF token against the session token.
    
    Args:
        request_token: Token from request
        session_token: Token from session
        
    Returns:
        True if the tokens match, False otherwise
    """
    if not request_token or not session_token:
        return False
        
    return hmac.compare_digest(request_token, session_token)


def hash_data(data: Union[str, bytes], salt: Optional[bytes] = None) -> Tuple[bytes, bytes]:
    """
    Hash arbitrary data with a salt.
    
    Args:
        data: Data to hash
        salt: Optional salt, generated if not provided
        
    Returns:
        Tuple of (hash, salt)
    """
    if salt is None:
        salt = os.urandom(DEFAULT_SALT_SIZE)
        
    if isinstance(data, str):
        data = data.encode('utf-8')
        
    data_hash = hashlib.pbkdf2_hmac(
        'sha256',
        data,
        salt,
        10000,  # Fewer iterations than for passwords
        dklen=DEFAULT_KEY_LENGTH
    )
    
    return data_hash, salt
