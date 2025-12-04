#!/usr/bin/env python3
import os, sys
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crypto_utils import load_private_key, decrypt_seed
from totp_utils import generate_totp_code

def log_totp_code():
    try:
        if not os.path.exists("encrypted_seed.txt"):
            print(f"[{datetime.now(timezone.utc)}] ERROR: encrypted_seed.txt not found")
            return
        with open("encrypted_seed.txt", "r") as f:
            encrypted_seed_b64 = f.read().strip()
        hex_seed = None
        if os.path.exists("/data/seed.txt"):
            with open("/data/seed.txt", "r") as f:
                hex_seed = f.read().strip()
        else:
            private_key = load_private_key("student_private.pem")
            hex_seed = decrypt_seed(encrypted_seed_b64, private_key)
        code, remaining = generate_totp_code(hex_seed)
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - 2FA Code: {code}"
        os.makedirs("/cron", exist_ok=True)
        with open("/cron/last_code.txt", "a") as f:
            f.write(log_entry + "\n")
        print(log_entry)
    except Exception as e:
        print(f"[{datetime.now(timezone.utc)}] ERROR: {e}")

if __name__ == "__main__":
    log_totp_code()
