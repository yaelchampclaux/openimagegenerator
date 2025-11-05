#!/bin/bash

echo "🧪 Testing Pollinations.ai API (FREE)..."

# Test direct de l'API Pollinations
echo "📡 Testing direct API call..."
curl -o test_image.png "https://image.pollinations.ai/prompt/a%20simple%20red%20car?width=512&height=512&nologo=true"

if [ -f "test_image.png" ] && [ -s "test_image.png" ]; then
    echo "✅ Pollinations API works! Image saved as test_image.png"
    file test_image.png
else
    echo "❌ Pollinations API failed or returned empty file"
fi

echo ""
echo "🔍 You can now test your Django app with Pollinations provider"
echo "   Just select 'Pollinations.ai (FREE)' in the dropdown"