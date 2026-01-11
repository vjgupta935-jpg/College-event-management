#!/usr/bin/env python3
"""
🧪 System Test Script - Verify all components work correctly
"""

import requests
import time

def test_system():
    print("🧪 Testing College Event Management System...")

    base_url = "http://localhost:5000"

    tests = [
        ("/", "Homepage"),
        ("/events", "Events page"),
        ("/login", "Login page"),
        ("/register", "Register page"),
    ]

    for endpoint, description in tests:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {description}: OK")
            else:
                print(f"❌ {description}: HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {description}: Connection failed - {e}")

    print("🎉 Testing complete!")

if __name__ == "__main__":
    print("⏳ Starting system test in 3 seconds...")
    time.sleep(3)
    test_system()
