from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import base64

def load_private_key(pem_file):
    """Load RSA private key from PEM file"""
    with open(pem_file, 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )
    return private_key

def decrypt_seed(encrypted_seed_b64, private_key):
    """
    Decrypt base64-encoded encrypted seed using RSA/OAEP
    
    Args:
        encrypted_seed_b64: Base64-encoded ciphertext
        private_key: RSA private key object
    
    Returns:
        Decrypted hex seed (64-character string)
    
    Raises:
        ValueError: If decryption fails or seed is invalid
    """
    try:
        # Step 1: Base64 decode the encrypted seed
        encrypted_seed = base64.b64decode(encrypted_seed_b64)
        
        # Step 2: RSA/OAEP decrypt with SHA-256
        decrypted_bytes = private_key.decrypt(
            encrypted_seed,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Step 3: Decode bytes to UTF-8 string
        decrypted_seed = decrypted_bytes.decode('utf-8')
        
        # Step 4: Validate - must be 64-character hex string
        if len(decrypted_seed) != 64:
            raise ValueError(f"Invalid seed length: {len(decrypted_seed)} (expected 64)")
        
        # Check all characters are hex digits
        try:
            int(decrypted_seed, 16)
        except ValueError:
            raise ValueError("Decrypted seed contains non-hex characters")
        
        # Step 5: Return hex seed
        return decrypted_seed
        
    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}")


# Test the decryption (run locally)

if __name__ == "__main__":
    private_key = load_private_key("student_private.pem")

    with open("encrypted_seed.txt", "r") as f:
        encrypted_seed_b64 = f.read().strip()

    try:
        seed = decrypt_seed(encrypted_seed_b64, private_key)
        print(f"Seed: {seed}")
    except Exception as e:
        print(f"❌ Decryption failed: {e}")

