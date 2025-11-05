#!/usr/bin/env python3
"""
Script pour tester la connexion à l'API Stability AI
"""
import requests
import os

API_KEY = os.getenv('STABILITY_AI_API_KEY')

if not API_KEY:
    print("❌ STABILITY_AI_API_KEY non trouvée dans .env")
    exit(1)

print(f"🔑 Testing API key: {API_KEY[:10]}...")

# Test 1: Vérifier les engines disponibles
print("\n📋 Testing available engines...")
engines_url = "https://api.stability.ai/v1/engines/list"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

try:
    response = requests.get(engines_url, headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        engines = response.json()
        print("✅ Available engines:")
        for engine in engines:
            print(f"  • {engine['id']} - {engine['name']}")
    else:
        print(f"❌ Error: {response.text}")
        
except Exception as e:
    print(f"❌ Connection error: {e}")

# Test 2: Test simple de génération
print("\n🎨 Testing simple generation...")
test_url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

payload = {
    "text_prompts": [
        {"text": "a simple red circle on white background", "weight": 1.0}
    ],
    "cfg_scale": 7,
    "height": 512,
    "width": 512,
    "samples": 1,
    "steps": 20,
}

try:
    response = requests.post(test_url, headers=headers, json=payload, timeout=30)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Generation test successful!")
        data = response.json()
        if 'artifacts' in data and len(data['artifacts']) > 0:
            print(f"✅ Generated {len(data['artifacts'])} image(s)")
        else:
            print("⚠️  No artifacts returned")
    else:
        print(f"❌ Generation failed: {response.text}")
        
except Exception as e:
    print(f"❌ Generation error: {e}")

print("\n🏁 Test completed!")