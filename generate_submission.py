import base64
import subprocess
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

print("=" * 80)
print("GENERATING SUBMISSION PROOF")
print("=" * 80)

# Get commit hash
commit_hash = subprocess.check_output(['git', 'log', '-1', '--format=%H']).decode().strip()
print(f"\n✅ Commit Hash (40-char hex):\n{commit_hash}\n")

# Load keys
print("Loading keys...")
with open("student_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())

with open("instructor_public.pem", "rb") as f:
    instructor_public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

with open("student_public.pem", "r") as f:
    student_public_key = f.read()

with open("encrypted_seed.txt", "r") as f:
    encrypted_seed = f.read().strip()

# Sign commit with student private key (RSA-PSS/SHA-256)
print("Signing commit hash...")
message_bytes = commit_hash.encode('utf-8')
signature_bytes = private_key.sign(
    message_bytes,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# Encrypt signature with instructor public key (RSA/OAEP)
print("Encrypting signature...")
encrypted_signature = instructor_public_key.encrypt(
    signature_bytes,
    padding.OAEP(
        mgf=padding.MGF1(hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Base64 encode
encrypted_signature_b64 = base64.b64encode(encrypted_signature).decode('utf-8')

print("\n" + "=" * 80)
print("📋 SUBMISSION DATA - COPY TO FORM:")
print("=" * 80)

print(f"\n1️⃣  GITHUB REPOSITORY URL:")
print("https://github.com/vamsi5355/Two-Factor-Authentication")

print(f"\n2️⃣  COMMIT HASH (40-char hex):")
print(commit_hash)

print(f"\n3️⃣  ENCRYPTED SIGNATURE (single line, NO breaks):")
print(encrypted_signature_b64)

print(f"\n4️⃣  STUDENT PUBLIC KEY (for API form):")
student_public_for_api = student_public_key.replace('\n', '\\n')
print(student_public_for_api)

print(f"\n5️⃣  ENCRYPTED SEED (single line, NO breaks):")
print(encrypted_seed)

print("\n" + "=" * 80)
print("✅ Ready for submission!")
print("=" * 80)
