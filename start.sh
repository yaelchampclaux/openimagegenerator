#!/bin/bash

echo "🚀 Setting up your Django Image Generator App..."

# Step 1: Create missing directories
echo "📁 Creating missing directories..."
mkdir -p static
mkdir -p you_image_generator/templatetags
mkdir -p you_image_generator/migrations

# Step 2: Create missing __init__.py files
touch you_image_generator/templatetags/__init__.py

# Step 3: Create the .env file with your API key
echo "🔐 Creating .env file..."
cat > .env << 'EOF'
# Django Settings
SECRET_KEY=django-insecure-z9&v=n+=r7$f2v_+t@_itk3d45@#@+1vg&7v@)ofy(4jvpbche
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (must match docker-compose.yml)
DATABASE_URL=postgres://user:password@localhost:5432/dbname
DB_NAME=openimage_db
DB_USER=openimage_user
DB_PASSWORD=your_very_strong_password1234
DB_HOST=db
DB_PORT=5432

# ===================================
# AI Image Generation API Keys
# ===================================

# --- FREE APIs (No payment required) ---

# Google Gemini (Nano Banana) - FREE tier with generous limits
# Get your key at: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_gemini_key_here

# Hugging Face - FREE tier, optional for more usage
# Get your key at: https://huggingface.co/settings/tokens
HUGGINGFACE_API_KEY=your_gemini_key_here

# DeepAI - FREE tier, optional for more features
# Get your key at: https://deepai.org/dashboard/profile
DEEPAI_API_KEY=your_deepai_key_here

# --- PAID APIs (Budget-friendly) ---

# Runware - Very affordable ($0.002 per image)
# Get your key at: https://my.runware.ai/keys
RUNWARE_API_KEY=your_runware_key_here

# Replicate - Pay per use, FLUX.1 access
# Get your key at: https://replicate.com/account/api-tokens
REPLICATE_API_KEY=your_replicate_token_here

# Stability AI - High quality but expensive
# Get your key at: https://platform.stability.ai/account/keys
STABILITY_AI_API_KEY=your_stability_ai_key_here


# ===================================
# Default Settings
# ===================================

# Default provider: placeholder, pollinations, deepai, huggingface, gemini, runware, replicate, stability
DEFAULT_IMAGE_PROVIDER=pollinations

# Default model
DEFAULT_IMAGE_GENERATION_MODEL=core
EOF

echo "⚠️  IMPORTANT: Edit .env file and add your real Stability AI API key!"
echo "   Get it from: https://platform.stability.ai/account/keys"

# Step 4: Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Step 5: Build and start the containers
echo "🏗️  Building containers..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Step 6: Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Step 7: Run Django migrations
echo "🔄 Running database migrations..."
docker-compose exec site python manage.py makemigrations
docker-compose exec site python manage.py migrate

# Step 8: Create superuser (optional)
echo "👤 Creating superuser (optional)..."
echo "You can skip this by pressing Ctrl+C"
docker-compose exec site python manage.py createsuperuser

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Your app is now running on:"
echo "   • Main app: http://localhost:9510"
echo "   • Admin panel: http://localhost:9510/admin"
echo "   • pgAdmin: http://localhost:9511"
echo "   • Documentation: http://localhost:9512"
echo ""
echo "📝 Next steps:"
echo "   1. Edit .env file and add your Stability AI API key"
echo "   2. Restart the app: docker-compose restart site"
echo "   3. Visit http://localhost:9510 to test image generation"
echo ""
echo "🔍 To view logs: docker-compose logs -f site"
echo "🐛 To debug: docker-compose exec site python manage.py shell"