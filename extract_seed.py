from crypto_utils import load_private_key, decrypt_seed

# Load private key
private_key = load_private_key("student_private.pem")

# Read encrypted seed
with open("encrypted_seed.txt", "r") as f:
    encrypted_seed_b64 = f.read().strip()

# Decrypt
hex_seed = decrypt_seed(encrypted_seed_b64, private_key)

# Save to file
with open("seed.txt", "w") as f:
    f.write(hex_seed)

print(f"✅ Seed.txt created: {hex_seed}")
