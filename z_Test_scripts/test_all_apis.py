#!/usr/bin/env python3
"""
Script pour tester toutes les APIs de génération d'images
Usage: python test_all_apis.py
"""
import os
import sys
from pathlib import Path

# Configuration Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'openimage.settings')

import django
django.setup()

from you_image_generator.ai_clients import (
    PollinationsClient,
    HuggingFaceClient,
    GeminiClient,
    DeepAIClient,
    RunwareClient,
    ReplicateClient,
    StabilityAiClient,
    PlaceholderClient,
    AVAILABLE_PROVIDERS
)

def test_provider(name, client_class, api_key=None, skip_reason=None):
    """Test un provider spécifique"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {name}")
    print(f"{'='*60}")
    
    if skip_reason:
        print(f"⏭️  SKIPPED: {skip_reason}")
        return False
    
    if not api_key and AVAILABLE_PROVIDERS.get(name.lower().replace(' ', '').replace('(', '').replace(')', ''), {}).get('requires_api_key'):
        print(f"⏭️  SKIPPED: No API key configured")
        return False
    
    try:
        # Initialiser le client
        if api_key:
            client = client_class(api_key)
        else:
            client = client_class()
        
        print(f"✅ Client initialized: {client.model_name}")
        
        # Test de génération
        print(f"🎨 Generating test image with prompt: 'a red apple'")
        
        result = client.generate_image(
            prompt="a red apple",
            options={'width': 512, 'height': 512}
        )
        
        if result and len(result) > 0:
            img = result[0]
            print(f"✅ SUCCESS!")
            print(f"   - Model: {img.model_used}")
            print(f"   - Image size: {len(img.image_data)} bytes")
            if img.image_url:
                print(f"   - URL: {img.image_url}")
            
            # Sauvegarder l'image de test
            output_dir = Path("test_outputs")
            output_dir.mkdir(exist_ok=True)
            
            filename = f"{name.lower().replace(' ', '_').replace('(', '').replace(')', '')}_test.png"
            output_path = output_dir / filename
            
            with open(output_path, 'wb') as f:
                f.write(img.image_data)
            
            print(f"   - Saved to: {output_path}")
            return True
        else:
            print(f"❌ FAILED: No image generated")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def main():
    """Test toutes les APIs disponibles"""
    print("🚀 Starting API Tests")
    print(f"{'='*60}\n")
    
    # Récupérer les clés API
    gemini_key = os.getenv('GEMINI_API_KEY')
    huggingface_key = os.getenv('HUGGINGFACE_API_KEY')
    deepai_key = os.getenv('DEEPAI_API_KEY')
    runware_key = os.getenv('RUNWARE_API_KEY')
    replicate_key = os.getenv('REPLICATE_API_KEY')
    stability_key = os.getenv('STABILITY_AI_API_KEY')
    
    results = {}
    
    # Tests des providers gratuits sans clé
    print("\n" + "🆓 FREE APIs (No Key Required) ".center(60, "="))
    
    results['Placeholder'] = test_provider(
        "Placeholder",
        PlaceholderClient
    )
    
    results['Pollinations'] = test_provider(
        "Pollinations",
        PollinationsClient
    )
    
    # Tests des providers gratuits avec clé optionnelle
    print("\n" + "🆓 FREE APIs (Optional Key) ".center(60, "="))
    
    results['DeepAI'] = test_provider(
        "DeepAI",
        DeepAIClient,
        api_key=deepai_key
    )
    
    results['Hugging Face'] = test_provider(
        "Hugging Face",
        HuggingFaceClient,
        api_key=huggingface_key
    )
    
    # Tests des providers gratuits avec clé requise
    print("\n" + "🆓 FREE APIs (Key Required) ".center(60, "="))
    
    results['Gemini'] = test_provider(
        "Gemini (Nano Banana)",
        GeminiClient,
        api_key=gemini_key
    )
    
    # Tests des providers payants
    print("\n" + "💰 PAID APIs ".center(60, "="))
    
    results['Runware'] = test_provider(
        "Runware",
        RunwareClient,
        api_key=runware_key
    )
    
    results['Replicate'] = test_provider(
        "Replicate (FLUX.1)",
        ReplicateClient,
        api_key=replicate_key,
        skip_reason="Takes 20-30 seconds, enable manually if needed"
    )
    
    results['Stability AI'] = test_provider(
        "Stability AI",
        StabilityAiClient,
        api_key=stability_key
    )
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RESULTS SUMMARY")
    print("=" * 60)
    
    working = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, success in results.items():
        status = "✅ WORKING" if success else "❌ FAILED/SKIPPED"
        print(f"{name:.<40} {status}")
    
    print(f"\n✅ Working: {working}/{total}")
    print(f"❌ Failed/Skipped: {total - working}/{total}")
    
    if working > 0:
        print("\n🎉 At least one provider is working!")
        print(f"💡 Check 'test_outputs/' folder for generated images")
    else:
        print("\n⚠️  No providers working. Check your API keys in .env file")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()