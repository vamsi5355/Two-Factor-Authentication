import requests
import json

BASE_URL = "http://localhost:8080"

print("╔════════════════════════════════════════════════════════════╗")
print("║          PKI-2FA Microservice - API Test Suite             ║")
print("╚════════════════════════════════════════════════════════════╝")

tests_passed = 0
tests_total = 0

# TEST 1: Health Check
print("\n" + "="*60)
print("  TEST 1: Health Check")
print("="*60)
tests_total += 1
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"✅ Status Code: {response.status_code}")
    print(f"✅ Response: {response.json()}")
    if response.status_code == 200:
        tests_passed += 1
except Exception as e:
    print(f"❌ Error: {e}")

# TEST 2: Decrypt Seed
print("\n" + "="*60)
print("  TEST 2: Decrypt Seed")
print("="*60)
tests_total += 1
try:
    response = requests.post(f"{BASE_URL}/decrypt-seed", timeout=5)
    print(f"✅ Status Code: {response.status_code}")
    print(f"✅ Response: {response.json()}")
    if response.status_code == 200:
        tests_passed += 1
        print("✅ Seed decrypted successfully!")
except Exception as e:
    print(f"❌ Error: {e}")

# TEST 3: Generate 2FA Code
print("\n" + "="*60)
print("  TEST 3: Generate 2FA Code")
print("="*60)
tests_total += 1
try:
    response = requests.get(f"{BASE_URL}/generate-2fa", timeout=5)
    print(f"✅ Status Code: {response.status_code}")
    data = response.json()
    print(f"✅ Response: {data}")
    if response.status_code == 200 and "code" in data:
        code = data["code"]
        remaining = data["valid_for"]
        print(f"✅ Generated Code: {code} (valid for {remaining}s)")
        tests_passed += 1
        
        # TEST 4: Verify Valid Code
        print("\n" + "="*60)
        print("  TEST 4: Verify Valid Code")
        print("="*60)
        tests_total += 1
        try:
            verify_response = requests.post(
                f"{BASE_URL}/verify-2fa",
                json={"code": code},
                timeout=5
            )
            print(f"✅ Status Code: {verify_response.status_code}")
            verify_data = verify_response.json()
            print(f"✅ Response: {verify_data}")
            if verify_data.get("valid") == True:
                print("✅ Valid code accepted!")
                tests_passed += 1
            else:
                print("❌ Valid code rejected!")
        except Exception as e:
            print(f"❌ Error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

# TEST 5: Verify Invalid Code
print("\n" + "="*60)
print("  TEST 5: Verify Invalid Code")
print("="*60)
tests_total += 1
try:
    response = requests.post(
        f"{BASE_URL}/verify-2fa",
        json={"code": "000000"},
        timeout=5
    )
    print(f"✅ Status Code: {response.status_code}")
    data = response.json()
    print(f"✅ Response: {data}")
    if data.get("valid") == False:
        print("✅ Invalid code correctly rejected!")
        tests_passed += 1
except Exception as e:
    print(f"❌ Error: {e}")

# TEST 6: Missing Code
print("\n" + "="*60)
print("  TEST 6: Verify with Missing Code")
print("="*60)
tests_total += 1
try:
    response = requests.post(
        f"{BASE_URL}/verify-2fa",
        json={},
        timeout=5
    )
    print(f"✅ Status Code: {response.status_code}")
    print(f"✅ Response: {response.json()}")
    if response.status_code == 400:
        print("✅ Correctly rejected empty code with HTTP 400!")
        tests_passed += 1
except Exception as e:
    print(f"❌ Error: {e}")

# TEST SUMMARY
print("\n" + "="*60)
print("  TEST SUMMARY")
print("="*60)
print(f"Total: {tests_passed}/{tests_total} tests passed")
if tests_passed == tests_total:
    print("✅ ALL TESTS PASSED!")
else:
    print(f"⚠️  {tests_total - tests_passed} test(s) failed")
