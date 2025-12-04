import time
import base64
from typing import Tuple

import pyotp

from crypto_utils import load_private_key, decrypt_seed


def generate_totp_code(hex_seed: str) -> Tuple[str, int]:
    """
    Generate current TOTP code from hex seed.

    Args:
        hex_seed: 64-character hex string.

    Returns:
        Tuple of (6-digit code, remaining seconds valid).

    Raises:
        ValueError: If seed is invalid or generation fails.
    """
    try:
        # Step 1: Validate hex seed
        if len(hex_seed) != 64:
            raise ValueError(f"Invalid seed length: {len(hex_seed)} (expected 64)")

        try:
            int(hex_seed, 16)
        except ValueError:
            raise ValueError("Seed contains non-hex characters")

        # Step 2: Convert hex seed to bytes
        seed_bytes = bytes.fromhex(hex_seed)

        # Step 3: Convert bytes to base32 encoding (PyOTP expects base32 secret)
        base32_seed = base64.b32encode(seed_bytes).decode("utf-8")

        # Step 4: Create TOTP object with base32 seed
        totp = pyotp.TOTP(base32_seed)

        # Step 5: Generate current TOTP code
        code = totp.now()

        # Step 6: Calculate remaining seconds in current period
        remaining_seconds = 30 - (int(time.time()) % 30)

        return code, remaining_seconds

    except Exception as e:
        raise ValueError(f"TOTP generation failed: {e}")


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify TOTP code with time window tolerance.

    Args:
        hex_seed: 64-character hex string.
        code: 6-digit code to verify.
        valid_window: Number of periods before/after to accept (default 1 = ±30 seconds).

    Returns:
        True if code is valid, False otherwise.

    Raises:
        ValueError: If seed or code is invalid or verification fails.
    """
    try:
        # Validate inputs
        if len(hex_seed) != 64:
            raise ValueError("Invalid seed length")

        if not isinstance(code, str) or len(code) != 6 or not code.isdigit():
            raise ValueError("Code must be 6 digits")

        # Step 1: Convert hex seed to base32 (same as generation)
        seed_bytes = bytes.fromhex(hex_seed)
        base32_seed = base64.b32encode(seed_bytes).decode("utf-8")

        # Step 2: Create TOTP object
        totp = pyotp.TOTP(base32_seed)

        # Step 3: Verify code with time window tolerance
        is_valid = totp.verify(code, valid_window=valid_window)

        return is_valid

    except Exception as e:
        raise ValueError(f"TOTP verification failed: {e}")


if __name__ == "__main__":
    # Step 0: Decrypt the seed using your private key and encrypted_seed.txt
    private_key = load_private_key("student_private.pem")

    with open("encrypted_seed.txt", "r") as f:
        encrypted_seed_b64 = f.read().strip()

    try:
        hex_seed = decrypt_seed(encrypted_seed_b64, private_key)
        print("Decrypted seed:", hex_seed)
        print("Seed length:", len(hex_seed))

        # Test code generation
        code, remaining = generate_totp_code(hex_seed)
        print(f"✅ TOTP Code: {code}")
        print(f"   Valid for: {remaining} seconds")

        # Test verification with current code
        is_valid = verify_totp_code(hex_seed, code)
        print(f"✅ Verification (current code): {is_valid}")

        # Test verification with an invalid code
        is_invalid = verify_totp_code(hex_seed, "000000")
        print(f"✅ Verification (invalid code): {is_invalid}")

    except Exception as e:
        print(f"❌ Error: {e}")
