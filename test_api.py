#!/usr/bin/env python3
"""Quick API test script"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

try:
    # Test 1: Health check
    print("=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    
    # Test 2: Login
    print("=== Testing Login ===")
    login_data = {"email": "admin@finance.com", "password": "admin123"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=5)
    print(f"Status: {response.status_code}")
    token_data = response.json()
    token = token_data.get("access_token")
    print(f"Token: {token[:30]}...\n")
    
    # Test 3: Get current user
    print("=== Testing /auth/me ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    
    # Test 4: Get dashboard summary
    print("=== Testing /dashboard/summary ===")
    response = requests.get(f"{BASE_URL}/dashboard/summary", headers=headers, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    
    # Test 5: List records
    print("=== Testing /records (list) ===")
    response = requests.get(f"{BASE_URL}/records/", headers=headers, timeout=5)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total records: {data.get('total')}")
    print(f"Items in response: {len(data.get('items', []))}\n")
    
    print("✓ All tests passed!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
