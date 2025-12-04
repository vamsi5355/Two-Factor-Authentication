#!/usr/bin/env python3
"""
Generate encrypted commit signature for PKI-2FA project submission
This script signs your latest commit hash and encrypts it with the instructor's public key
"""

import subprocess
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend

def get_latest_commit_hash():
    """
    Get the latest commit hash from git repository
    
    Returns:
        str: 40-character hexadecimal commit hash
    """
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%H'],
            capture_output=True,
            text=True,
            check=True
        )
        commit_hash = result.stdout.strip()
        print(f"✓ Commit Hash: {commit_hash}")
        return commit_hash
    except subprocess.CalledProcessError as e:
        print(f"✗ Error getting commit hash: {e}")
        exit(1)

def load_private_key(filepath='student_private.pem'):
    """
    Load student's RSA private key from PEM file
    
    Args:
        filepath: Path to private key file
        
    Returns:
        RSA private key object
    """
    try:
        with open(filepath, 'rb') as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )
        print(f"✓ Loaded private key from {filepath}")
        return private_key
    except Exception as e:
        print(f"✗ Error loading private key: {e}")
        exit(1)

def load_public_key(filepath='instructor_public.pem'):
    """
    Load instructor's RSA public key from PEM file
    
    Args:
        filepath: Path to public key file
        
    Returns:
        RSA public key object
    """
    try:
        with open(filepath, 'rb') as f:
            public_key = serialization.load_pem_public_key(
                f.read(),
                backend=default_backend()
            )
        print(f"✓ Loaded instructor public key from {filepath}")
        return public_key
    except Exception as e:
        print(f"✗ Error loading public key: {e}")
        exit(1)

def sign_commit_hash(commit_hash, private_key):
    """
    Sign commit hash using RSA-PSS with SHA-256
    
    CRITICAL: Signs the ASCII string of the commit hash, NOT binary hex
    
    Args:
        commit_hash: 40-character hex string (commit hash)
        private_key: RSA private key object
        
    Returns:
        bytes: Digital signature
    """
    try:
        # CRITICAL: Sign the ASCII/UTF-8 bytes of the commit hash string
        # NOT the binary hex representation!
        message_bytes = commit_hash.encode('utf-8')
        
        # Sign using RSA-PSS with SHA-256
        signature = private_key.sign(
            message_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),  # MGF1 with SHA-256
                salt_length=padding.PSS.MAX_LENGTH   # Maximum salt length
            ),
            hashes.SHA256()  # Hash algorithm
        )
        
        print(f"✓ Signed commit hash using RSA-PSS-SHA256")
        print(f"  Signature length: {len(signature)} bytes")
        return signature
        
    except Exception as e:
        print(f"✗ Error signing commit hash: {e}")
        exit(1)

def encrypt_signature(signature, public_key):
    """
    Encrypt signature with instructor's public key using RSA/OAEP-SHA256
    
    Args:
        signature: Digital signature bytes
        public_key: Instructor's RSA public key
        
    Returns:
        bytes: Encrypted signature
    """
    try:
        # Encrypt using RSA/OAEP with SHA-256
        encrypted = public_key.encrypt(
            signature,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),  # MGF1 with SHA-256
                algorithm=hashes.SHA256(),                     # Hash algorithm
                label=None                                     # No label
            )
        )
        
        print(f"✓ Encrypted signature using RSA/OAEP-SHA256")
        print(f"  Encrypted length: {len(encrypted)} bytes")
        return encrypted
        
    except Exception as e:
        print(f"✗ Error encrypting signature: {e}")
        exit(1)

def encode_base64(data):
    """
    Encode data to base64 string (single line, no line breaks)
    
    Args:
        data: Bytes to encode
        
    Returns:
        str: Base64-encoded string
    """
    encoded = base64.b64encode(data).decode('utf-8')
    print(f"✓ Base64 encoded result")
    print(f"  Length: {len(encoded)} characters")
    return encoded

def main():
    """
    Main function to generate encrypted commit signature
    """
    print("=" * 70)
    print("PKI-2FA Commit Signature Generator")
    print("=" * 70)
    print()
    
    # Step 1: Get latest commit hash
    print("Step 1: Getting latest commit hash...")
    commit_hash = get_latest_commit_hash()
    print()
    
    # Step 2: Load student private key
    print("Step 2: Loading student private key...")
    student_private_key = load_private_key('student_private.pem')
    print()
    
    # Step 3: Sign commit hash with student private key (RSA-PSS)
    print("Step 3: Signing commit hash with RSA-PSS-SHA256...")
    signature = sign_commit_hash(commit_hash, student_private_key)
    print()
    
    # Step 4: Load instructor public key
    print("Step 4: Loading instructor public key...")
    instructor_public_key = load_public_key('instructor_public.pem')
    print()
    
    # Step 5: Encrypt signature with instructor public key (RSA/OAEP)
    print("Step 5: Encrypting signature with RSA/OAEP-SHA256...")
    encrypted_signature = encrypt_signature(signature, instructor_public_key)
    print()
    
    # Step 6: Base64 encode the result
    print("Step 6: Base64 encoding encrypted signature...")
    encrypted_signature_b64 = encode_base64(encrypted_signature)
    print()
    
    # Display results
    print("=" * 70)
    print("RESULTS - Copy these for submission:")
    print("=" * 70)
    print()
    print("Latest Commit Hash:")
    print(commit_hash)
    print()
    print("Encrypted Commit Signature (Base64):")
    print(encrypted_signature_b64)
    print()
    print("=" * 70)
    print("⚠️  IMPORTANT: Copy the entire base64 string as ONE LINE")
    print("=" * 70)

if __name__ == "__main__":
    main()
