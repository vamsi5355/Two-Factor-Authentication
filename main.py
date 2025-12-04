from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import os
import base64
from crypto_utils import load_private_key, decrypt_seed
from totp_utils import generate_totp_code, verify_totp_code

app = FastAPI()

# Global variable to store decrypted seed
decrypted_seed = None

def try_save_seed(hex_seed):
    """Try to save seed to /data/seed.txt, but don't fail if not writable"""
    try:
        os.makedirs("/data", exist_ok=True)
        with open("/data/seed.txt", "w") as f:
            f.write(hex_seed)
    except (OSError, PermissionError):
        # In local dev, /data might not be writable. That's OK.
        pass

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.post("/decrypt-seed")
async def decrypt_seed_endpoint():
    """POST /decrypt-seed - Decrypt the seed from encrypted_seed.txt"""
    global decrypted_seed
    
    try:
        if not os.path.exists("encrypted_seed.txt"):
            raise FileNotFoundError("encrypted_seed.txt not found")
        
        with open("encrypted_seed.txt", "r") as f:
            encrypted_seed_b64 = f.read().strip()
        
        private_key = load_private_key("student_private.pem")
        hex_seed = decrypt_seed(encrypted_seed_b64, private_key)
        
        decrypted_seed = hex_seed
        try_save_seed(hex_seed)
        
        return {"status": "ok", "message": "Seed decrypted and saved"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})

@app.get("/generate-2fa")
async def generate_2fa():
    """GET /generate-2fa - Generate current TOTP code"""
    global decrypted_seed
    
    try:
        if decrypted_seed is None:
            if os.path.exists("/data/seed.txt"):
                with open("/data/seed.txt", "r") as f:
                    decrypted_seed = f.read().strip()
            else:
                raise Exception("Seed not decrypted yet")
        
        code, remaining = generate_totp_code(decrypted_seed)
        return {"code": code, "valid_for": remaining}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})

@app.post("/verify-2fa")
async def verify_2fa(payload: dict):
    """POST /verify-2fa - Verify TOTP code"""
    global decrypted_seed
    
    try:
        code = payload.get("code")
        if not code:
            raise HTTPException(status_code=400, detail={"error": "Missing code"})
        
        if decrypted_seed is None:
            if os.path.exists("/data/seed.txt"):
                with open("/data/seed.txt", "r") as f:
                    decrypted_seed = f.read().strip()
            else:
                raise Exception("Seed not decrypted yet")
        
        is_valid = verify_totp_code(decrypted_seed, code, valid_window=1)
        return {"valid": is_valid}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
