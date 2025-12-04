import requests

print("Calling /decrypt-seed endpoint...")
response = requests.post("http://localhost:8080/decrypt-seed")

if response.status_code == 200:
    print(f"✅ Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("\n✅ seed.txt has been created in memory!")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.json())
