# 🚀 Installation Guide

Complete installation guide for OpenImage with multiple installation methods.

---

## 📋 Prerequisites

### System Requirements

=== "Minimum"
    - **CPU**: 2 cores
    - **RAM**: 2GB
    - **Storage**: 5GB free
    - **OS**: Linux, macOS, Windows 10+

=== "Recommended"
    - **CPU**: 4+ cores
    - **RAM**: 4GB+
    - **Storage**: 20GB+ SSD
    - **OS**: Ubuntu 20.04+ or macOS

### Software Requirements

=== "Docker Installation"
    - [Docker](https://docs.docker.com/get-docker/) 20.10+
    - [Docker Compose](https://docs.docker.com/compose/install/) 2.0+
    - (Windows) [WSL 2](https://docs.microsoft.com/en-us/windows/wsl/install)

=== "Manual Installation"
    - [Python](https://www.python.org/downloads/) 3.11+
    - [PostgreSQL](https://www.postgresql.org/download/) 14+ (optional)
    - [Git](https://git-scm.com/downloads)
    - pip (included with Python)

---

## 🐳 Method 1: Docker Installation (Recommended)

### Quick Start (30 seconds)

⚠️ If you already have personnal api key to one of the available api (gemini, huggingface, deepai, runaware, stability, replicate), you can edit the start.sh to add them before followwing step.

```bash
# Clone repository
git clone https://github.com/yourusername/openimage.git
cd openimage/oi_v2

# Run automated setup
chmod +x start.sh
./start.sh
```

The script will:
1. ✅ Create necessary directories
2. ✅ Generate `.env` file template
3. ✅ Build Docker containers
4. ✅ Initialize PostgreSQL database
5. ✅ Run Django migrations
6. ✅ Offer superuser creation

**Access your installation:**
- Main App: http://localhost:9510
- pgAdmin: http://localhost:9511
- Documentation: http://localhost:9512

### Manual Docker Setup

#### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/openimage.git
cd openimage/oi_v2
```

#### Step 2: Configure Environment

Create `.env` file:

```bash
cp .env.example .env
nano .env  # or use your favorite editor
```

**Essential configuration:**

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Docker)
DATABASE_URL=postgres://openimage_user:your_very_strong_password1234@db:5432/openimage_db

# Google Gemini (FREE - Get key at https://aistudio.google.com/app/apikey)
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Other providers
HUGGINGFACE_API_KEY=
DEEPAI_API_KEY=
RUNWARE_API_KEY=
REPLICATE_API_KEY=
STABILITY_AI_API_KEY=

# Default Provider
DEFAULT_IMAGE_PROVIDER=pollinations

# Default model
DEFAULT_IMAGE_GENERATION_MODEL=core
```

#### Step 3: Build and Start Services

```bash
# Build containers
docker-compose build

# Start all services
docker-compose up -d

# Check status
docker-compose ps
```

**Expected output:**
```
NAME        SERVICE    STATUS    PORTS
oi_www      site       running   0.0.0.0:9510->8001/tcp
oi_db       db         running   5432/tcp
oi_pgadmin  pgadmin    running   0.0.0.0:9511->80/tcp
oi_doc      mkdocs     running   0.0.0.0:9512->8000/tcp
```

#### Step 4: Initialize Database

```bash
# Wait for PostgreSQL to be ready (10 seconds)
sleep 10

# Create database schema
docker-compose exec site python manage.py migrate

# Create superuser (optional)
docker-compose exec site python manage.py createsuperuser

# Collect static files
docker-compose exec site python manage.py collectstatic --noinput
```

#### Step 5: Verify Installation

```bash
# Check Django logs
docker-compose logs -f site

# Test API connection
curl http://localhost:9510/
```

### Import Sample Database (Optional)

If you want to start with example images:

```bash
# Import provided backup
docker-compose exec -T db psql -U openimage_user openimage_db < z_backups_db/backup-db-07102025.sql

# Verify import
docker-compose exec db psql -U openimage_user -d openimage_db -c "SELECT COUNT(*) FROM you_image_generator_generatedimage;"
```

---

## 🔧 Method 2: Automated Script Installation

### Linux / macOS

```bash
# Make script executable
chmod +x setup.sh

# Run installation
./setup.sh
```

### Windows

```cmd
# Double-click setup.bat
# Or run in Command Prompt:
setup.bat
```

The script will:
1. Check Python installation
2. Create virtual environment
3. Install dependencies
4. Create `.env` template
5. Initialize database (SQLite by default)
6. Collect static files
7. Offer superuser creation

**After installation:**

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Start server
python manage.py runserver
```

Access at: http://localhost:8000

---

## 💻 Method 3: Manual Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/openimage.git
cd openimage/oi_v2
```

### Step 2: Create Virtual Environment

=== "Linux/macOS"
    ```bash
    python3.11 -m venv venv
    source venv/bin/activate
    ```

=== "Windows"
    ```cmd
    python -m venv venv
    venv\Scripts\activate
    ```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

**Common packages installed:**
- Django 5.2.6
- psycopg2-binary (PostgreSQL adapter)
- requests (API calls)
- python-decouple (environment variables)
- Pillow (image processing)
- pytest, black, flake8 (development tools)

### Step 4: Configure Environment

Create `.env` file in `oi_v2/`:

```bash
# Django Core
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database - SQLite (development)
# Leave DATABASE_URL empty to use SQLite
DATABASE_URL=

# Or PostgreSQL (production)
# DATABASE_URL=postgres://user:password@localhost:5432/dbname

# === FREE API KEYS ===
# Google Gemini (1500/day) - https://aistudio.google.com/app/apikey
GEMINI_API_KEY=

# Hugging Face - https://huggingface.co/settings/tokens
HUGGINGFACE_API_KEY=

# DeepAI - https://deepai.org/dashboard/profile
DEEPAI_API_KEY=

# === PAID API KEYS (Optional) ===
RUNWARE_API_KEY=
REPLICATE_API_KEY=
STABILITY_AI_API_KEY=

# Settings
DEFAULT_IMAGE_PROVIDER=pollinations

# Default model
DEFAULT_IMAGE_GENERATION_MODEL=core
```

### Step 5: Initialize Database

```bash
# Create database tables
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### Step 6: Start Development Server

```bash
python manage.py runserver
```

Access at: http://localhost:8000

---

## 🔑 API Keys Configuration

### Getting API Keys

#### 1. Google Gemini (FREE - Recommended) ⭐

**Why:** 1500 free images/day, excellent quality

**Steps:**
1. Visit https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy key and add to `.env`:
   ```
   GEMINI_API_KEY=AIzaSyC...your-key-here
   ```

**Limits:** 1500 requests/day (free tier)

#### 2. Hugging Face (FREE - Optional)

**Why:** Access to FLUX.1 and multiple models

**Steps:**
1. Create account at https://huggingface.co/join
2. Go to https://huggingface.co/settings/tokens
3. Click "New token" → Select "Read" role
4. Copy and add to `.env`:
   ```
   HUGGINGFACE_API_KEY=hf_...your-token
   ```

**Limits:** Generous free tier, may have cold starts

#### 3. DeepAI (FREE - Backup)

**Why:** Simple API, decent quality

**Steps:**
1. Sign up at https://deepai.org/
2. Go to https://deepai.org/dashboard/profile
3. Copy your API key
4. Add to `.env`:
   ```
   DEEPAI_API_KEY=quickstart-...your-key
   ```

**Limits:** Free tier with reasonable limits

#### 43. Paid Providers (Optional)

=== "Runware ($0.002/image)"
    ```
    1. Sign up: https://runware.ai
    2. Get key: https://my.runware.ai/keys
    3. Add: RUNWARE_API_KEY=your-key
    
    Best for: High-volume production
    ```

=== "Replicate ($0.003-0.005/image)"
    ```
    1. Sign up: https://replicate.com
    2. Get token: https://replicate.com/account/api-tokens
    3. Add: REPLICATE_API_KEY=r8_your-token
    
    Best for: Top quality results
    ```

=== " Simple API, decent quality ($0.01-0.04/image)"
    ```
    1. Sign up: https://platform.stability.ai
    2. Get key: https://platform.stability.ai/account/keys
    3. Add: STABILITY_AI_API_KEY=sk-your-key
    
    Best for: Enterprise applications
    ```


=== "DeepAI ($0.01-.../image)"
    ```
    1. Sign up at https://deepai.org/
    2. Go to https://deepai.org/dashboard/profile
    3. Copy your API key
    4. Add to `.env`:

    Best for: 
    ```

---

## 🗄️ Database Configuration

### SQLite (Development)

**Default configuration** - No setup needed!

```python
# settings.py - Automatically used if DATABASE_URL is empty
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Pros:** 
- ✅ Zero configuration
- ✅ Perfect for development
- ✅ Single file database

**Cons:**
- ❌ Not recommended for production
- ❌ Limited concurrent access

### PostgreSQL (Production)

#### Option A: Docker PostgreSQL (Included)

Already configured in `docker-compose.yml`:

```yaml
db:
  image: postgres:14
  environment:
    POSTGRES_DB: openimage_db
    POSTGRES_USER: openimage_user
    POSTGRES_PASSWORD: your_very_strong_password1234
```

**No additional setup needed with Docker!**

#### Option B: Local PostgreSQL

**Install PostgreSQL:**

=== "Ubuntu/Debian"
    ```bash
    sudo apt update
    sudo apt install postgresql postgresql-contrib
    sudo systemctl start postgresql
    ```

=== "macOS"
    ```bash
    brew install postgresql@14
    brew services start postgresql@14
    ```

=== "Windows"
    Download from: https://www.postgresql.org/download/windows/

**Create database:**

```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE openimage_db;
CREATE USER openimage_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE openimage_db TO openimage_user;
\q
```

**Update `.env`:**

```bash
DATABASE_URL=postgres://openimage_user:your_password@localhost:5432/openimage_db
```

**Run migrations:**

```bash
python manage.py migrate
```

---

## 🧪 Testing Your Installation

### Quick Test

```bash
# Test Django is working
python manage.py check

# Test database connection
python manage.py showmigrations

# Test static files
python manage.py collectstatic --dry-run
```

### Test API Providers

```bash
# Run comprehensive API test
cd z_Test_scripts
python test_all_apis.py
```

**Expected output:**
```
🧪 Testing: Pollinations
✅ SUCCESS! Saved to: test_outputs/pollinations_test.png

🧪 Testing: Gemini
✅ SUCCESS! Saved to: test_outputs/gemini_test.png

🧪 Testing: Hugging Face
✅ SUCCESS! Saved to: test_outputs/huggingface_flux-schnell_test.png

📊 RESULTS: 3/8 providers working
✅ At least one provider is working!
```

### Test Single Provider

```bash
# In Django shell
python manage.py shell

# Test Gemini
from you_image_generator.ai_clients import get_api_client
from django.conf import settings

client = get_api_client('gemini', settings.GEMINI_API_KEY)
result = client.generate_image("a red apple")
print(f"✅ Success! Image size: {len(result[0].image_data)} bytes")
```

### Test Web Interface

1. **Start server:**
   ```bash
   python manage.py runserver
   ```

2. **Open browser:** http://localhost:8000

3. **Generate test image:**
   - Select "Pollinations" (no API key needed)
   - Prompt: "a red apple on white background"
   - Click "Generate Image"
   - Should complete in 2-5 seconds

---

## 📦 pgAdmin Setup (Docker Only)

### Access pgAdmin

1. Open http://localhost:9511
2. Login with credentials from `docker-compose.yml`:
   - Email: `admin@openimage.com`
   - Password: `pgadminpassword1234!`

### Register OpenImage Database

1. **Right-click "Servers"** → "Register" → "Server"

2. **General tab:**
   - Name: `OpenImage DB`

3. **Connection tab:**
   - Host name/address: `db` (Docker service name)
   - Port: `5432`
   - Maintenance database: `openimage_db`
   - Username: `openimage_user`
   - Password: `your_very_strong_password1234`

4. **Save** and you're connected!

### Useful pgAdmin Operations

=== "View Tables"
    Navigate to:
    ```
    Servers → OpenImage DB → Databases → openimage_db → Schemas → public → Tables
    ```

=== "Query Images"
    ```sql
    SELECT id, prompt, provider, width, height, created_at
    FROM you_image_generator_generatedimage
    ORDER BY created_at DESC
    LIMIT 10;
    ```

=== "Backup Database"
    Right-click database → "Backup..."
    - Format: Custom
    - Filename: `openimage_backup_2025-10-07.backup`

=== "Restore Database"
    Right-click database → "Restore..."
    - Select your backup file
    - Click "Restore"

---

## 🔄 Importing Sample Data

### Import Database Backup

```bash
# Docker method
docker-compose exec -T db psql -U openimage_user openimage_db < z_backups_db/backup-db-07102025.sql

# Manual installation method
psql -U openimage_user -d openimage_db -f z_backups_db/backup-db-07102025.sql
```

### Verify Import

```bash
# Check image count
docker-compose exec db psql -U openimage_user -d openimage_db -c "SELECT COUNT(*) FROM you_image_generator_generatedimage;"

# Or in Django shell
python manage.py shell
>>> from you_image_generator.models import GeneratedImage
>>> print(f"Total images: {GeneratedImage.objects.count()}")
```

---

## 🐛 Troubleshooting

### Common Installation Issues

#### Port Already in Use

**Problem:** `Error: Port 9510 is already allocated`

**Solution:**
```bash
# Find process using port
lsof -i :9510  # Linux/macOS
netstat -ano | findstr :9510  # Windows

# Kill process or change port in docker-compose.yml
ports:
  - "9520:8001"  # Use different port
```

#### Docker Not Starting

**Problem:** `Cannot connect to Docker daemon`

**Solution:**
```bash
# Check Docker status
sudo systemctl status docker  # Linux
docker info  # All platforms

# Start Docker
sudo systemctl start docker  # Linux
# Or start Docker Desktop on Windows/Mac
```

#### Database Connection Failed

**Problem:** `FATAL: password authentication failed`

**Solution:**
```bash
# Check .env credentials match docker-compose.yml
# Recreate database
docker-compose down -v
docker-compose up -d

# Wait 10 seconds
sleep 10
docker-compose exec site python manage.py migrate
```

#### Module Not Found

**Problem:** `ModuleNotFoundError: No module named 'decouple'`

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### Permission Denied

**Problem:** `Permission denied: '/app/db.sqlite3'`

**Solution:**
```bash
# Docker: Fix permissions
docker-compose exec site chown -R 1000:1000 /app

# Manual: Check file permissions
chmod 644 db.sqlite3
chmod 755 .
```

#### API Key Errors

**Problem:** `API key not configured for Gemini`

**Solution:**
```bash
# Verify .env file exists and has key
cat .env | grep GEMINI_API_KEY

# Ensure no spaces around = sign
GEMINI_API_KEY=AIzaSyC...  ✅ Correct
GEMINI_API_KEY = AIzaSyC... ❌ Wrong

# Restart Django
docker-compose restart site  # Docker
# Or kill and restart runserver manually
```

#### Static Files Not Loading

**Problem:** CSS/JS not loading

**Solution:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check DEBUG setting
# In .env: DEBUG=True (for development)

# Docker: check volume mount
docker-compose logs site | grep static
```

---

## 🔄 Updating OpenImage

### Docker Update

```bash
# Pull latest code
git pull origin main

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Run new migrations
docker-compose exec site python manage.py migrate

# Collect new static files
docker-compose exec site python manage.py collectstatic --noinput
```

### Manual Update

```bash
# Activate virtual environment
source venv/bin/activate

# Pull latest code
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart server
# Kill existing runserver and start again
python manage.py runserver
```

---

## 🚀 Post-Installation Steps

### 1. Configure API Keys

Get at least one API key (Gemini recommended):
- https://aistudio.google.com/app/apikey

### 2. Test Generation

Generate your first image with Pollinations (no key needed)

### 3. Configure Settings

Adjust `settings.py` for your needs:
```python
# Email configuration (for user accounts later)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587

# Time zone
TIME_ZONE = 'Europe/Paris'  # Your timezone

# Allowed hosts (production)
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

### 4. Setup Backup

```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y-%m-%d)
docker-compose exec db pg_dump -U openimage_user openimage_db > backups/backup_$DATE.sql
EOF

chmod +x backup.sh

# Run daily at 2 AM
crontab -e
# Add: 0 2 * * * /path/to/openimage/backup.sh
```

### 5. Monitor Logs

```bash
# Docker
docker-compose logs -f site

# Manual
tail -f debug.log
```

### 6. Setup SSL (Production)

Use Let's Encrypt with Nginx:
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com
```

---

## 📚 Next Steps

### Learn the Basics

1. [First Generation Tutorial](tutorial.md)
2. [Understanding Providers](apis.md)
3. [Style Presets Guide](features.md#style-presets)

### Advanced Topics

1. [AI Upscaling](features.md#ai-upscaling)
2. [Search & Tags](search.md)
3. [Batch Operations](features.md#batch-operations)

### Development

1. [Developer Guide](dev.md)
2. [Adding Providers](custom-providers.md)
3. [API Reference](api-reference.md)

---

## 🆘 Getting Help

### Documentation

- 📖 [Full Documentation](index.md)
- 🎓 [Tutorials](tutorial.md)
- 🔧 [Troubleshooting](troubleshooting.md)

### Community

- 💬 [GitHub Discussions](https://github.com/yourusername/openimage/discussions)
- 🐛 [Report Issues](https://github.com/yourusername/openimage/issues)
- 📧 [Email Support](mailto:support@openimage.dev)

### Common Questions

??? question "Which installation method should I choose?"
    - **Docker**: Best for most users, includes all services
    - **Script**: Quick setup for Python developers
    - **Manual**: Maximum control, best for customization

??? question "Do I need all API keys?"
    No! Start with just Pollinations (no key needed) or Gemini (free tier).

??? question "Can I use SQLite in production?"
    Not recommended. Use PostgreSQL for production environments.

??? question "How do I change the port?"
    Edit `docker-compose.yml` or use `python manage.py runserver 0.0.0.0:8080`

??? question "Can I run this on a Raspberry Pi?"
    Yes! Use manual installation. Docker may be slow on RPi 3 or older.

---

## ✅ Installation Checklist

- [ ] System requirements met
- [ ] Docker installed (if using Docker method)
- [ ] Repository cloned
- [ ] Environment variables configured
- [ ] Database initialized
- [ ] Migrations applied
- [ ] At least one API key configured
- [ ] Test generation successful
- [ ] Static files collected
- [ ] Documentation accessible

---

<div align="center">

**🎉 Congratulations! OpenImage is now installed!**

[← Back to Home](index.md) | [Next: First Generation →](tutorial.md)

</div>