import json
import requests
import base64

# Read your student public key
with open('student_public.pem', 'r') as f:
    public_key = f.read()

# Your student ID (get this from your Partnr profile)
student_id = "23A91A0504"  # Replace with your actual student ID

# Your GitHub repository URL
github_repo_url = "https://github.com/vamsi5355/Two-Factor-Authentication.git"  # Replace with your actual repo URL

# Prepare the request
payload = {
    "student_id": "23A91A0504",
    "github_repo_url": "https://github.com/vamsi5355/Two-Factor-Authentication.git",
    "public_key": public_key
}

# API endpoint
api_url = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/"

try:
    # Send POST request
    response = requests.post(api_url, json=payload, timeout=30)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Parse response
    data = response.json()
    
    if response.status_code == 200 and "encrypted_seed" in data:
        # Save encrypted seed to file
        with open('encrypted_seed.txt', 'w') as f:
            f.write(data['encrypted_seed'])
        
        print("✅ Encrypted seed saved to encrypted_seed.txt")
        print(f"Encrypted Seed: {data['encrypted_seed'][:50]}...")
    else:
        print("❌ Failed to get encrypted seed")
        print(f"Error: {data.get('error', 'Unknown error')}")
        
except Exception as e:
    print(f"❌ Error: {e}")
