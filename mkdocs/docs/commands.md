# 📝 Commands Reference

Essential commands for OpenImage management.

## 🐳 Docker Commands

### Start/Stop
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Restart specific service
docker-compose restart site

# View logs
docker-compose logs -f site
docker-compose logs -f db

# Stop and remove volumes (⚠️ deletes data)
docker-compose down -v

# Check if a superuser exists
docker-compose exec site python manage.py shell -c "from django.contrib.auth.models import User; print('Superusers:', User.objects.filter(is_superuser=True).values_list('username', flat=True))"

# Delete a superuser
docker-compose exec site python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='**** Here the username to delete ****').delete(); print('Deleted')"

```

### Build & Update
```bash
# Rebuild containers
docker-compose build

# Rebuild and start
docker-compose up -d --build

# Pull latest images
docker-compose pull
```

### Container Management
```bash
# List running containers
docker-compose ps

# Execute command in container
docker-compose exec site python manage.py shell

# Access container shell
docker-compose exec site bash
docker-compose exec db psql -U openimage_user openimage_db
```

## 🗄️ Database Commands

### Migrations
```bash
# Create migration files
docker-compose exec site python manage.py makemigrations

# Apply migrations
docker-compose exec site python manage.py migrate

# Show migration status
docker-compose exec site python manage.py showmigrations

# Migrate specific app
docker-compose exec site python manage.py migrate you_image_generator

# Rollback migration
docker-compose exec site python manage.py migrate you_image_generator 0001

# Reset all migrations (⚠️ deletes data)
docker-compose exec site python manage.py migrate you_image_generator zero
docker-compose exec site python manage.py migrate
```

### Database Management
```bash
# Django shell
docker-compose exec site python manage.py shell

# Database shell
docker-compose exec site python manage.py dbshell

# Create superuser
docker-compose exec site python manage.py createsuperuser

# Backup database
docker-compose exec db pg_dump -U openimage_user openimage_db > backup.sql

# Restore database
docker-compose exec -T db psql -U openimage_user openimage_db < backup.sql

# Export data
docker-compose exec site python manage.py dumpdata you_image_generator > data.json

# Import data
docker-compose exec site python manage.py loaddata data.json
```

### Database Queries
```bash
# Count images
docker-compose exec site python manage.py shell -c "from you_image_generator.models import GeneratedImage; print(GeneratedImage.objects.count())"

# List recent images
docker-compose exec site python manage.py shell -c "from you_image_generator.models import GeneratedImage; for img in GeneratedImage.objects.all()[:5]: print(f'{img.id}: {img.prompt[:50]}')"

# Delete all images (⚠️ careful!)
docker-compose exec site python manage.py shell -c "from you_image_generator.models import GeneratedImage; GeneratedImage.objects.all().delete()"
```

## 📁 Static Files Commands

### Collect Static Files
```bash
# Collect all static files
docker-compose exec site python manage.py collectstatic --noinput

# Collect and clear existing
docker-compose exec site python manage.py collectstatic --noinput --clear

# Collect with verbose output
docker-compose exec site python manage.py collectstatic -v 2
```

## 🧪 Testing Commands

### Run Tests
```bash
# Run feature tests
docker-compose exec site python test_features.py

# Run Django tests
docker-compose exec site python manage.py test

# All tests
docker-compose exec site python manage.py test you_image_generator

# Tests spécifiques
docker-compose exec site python manage.py test you_image_generator.tests.test_models
docker-compose exec site python manage.py test you_image_generator.tests.test_views
docker-compose exec site python manage.py test you_image_generator.tests.test_styles
docker-compose exec site python manage.py test you_image_generator.tests.test_ai_clients


# Avec verbosité
docker-compose exec site python manage.py test you_image_generator --verbosity=2

# Avec coverage
docker-compose exec site pip install coverage
docker-compose exec site coverage run manage.py test you_image_generator
docker-compose exec site coverage report
docker-compose exec site coverage html

```

### Check Project
```bash
# Check for issues
docker-compose exec site python manage.py check

# Check migrations
docker-compose exec site python manage.py makemigrations --check --dry-run

# Check static files
docker-compose exec site python manage.py findstatic style.css
```

## 🔧 Development Commands

### Code Quality
```bash
# Format code with black
docker-compose exec site black .

# Sort imports
docker-compose exec site isort .

# Lint with flake8
docker-compose exec site flake8 .

# Type check with mypy
docker-compose exec site mypy you_image_generator
```

### Django Management
```bash
# Create new app
docker-compose exec site python manage.py startapp myapp

# Create superuser
docker-compose exec site python manage.py createsuperuser

# Change password
docker-compose exec site python manage.py changepassword username

# Clear cache
docker-compose exec site python manage.py clear_cache
```

## 🔑 Environment & Config

### View Configuration
```bash
# Show settings
docker-compose exec site python manage.py diffsettings

# Show installed apps
docker-compose exec site python manage.py shell -c "from django.conf import settings; print(settings.INSTALLED_APPS)"

# Show API keys (⚠️ sensitive)
docker-compose exec site python manage.py shell -c "from django.conf import settings; print(f'Gemini: {bool(settings.GEMINI_API_KEY)}')"
```

### Update Environment
```bash
# Edit .env file
nano .env

# Restart after .env change
docker-compose restart site

# Rebuild with new env
docker-compose up -d --force-recreate site
```

## 📊 Monitoring Commands

### Logs & Debug
```bash
# Tail logs
docker-compose logs -f --tail=100 site

# Search logs
docker-compose logs site | grep ERROR

# Show resource usage
docker stats

# Show disk usage
docker system df

# Clean up unused resources
docker system prune -a
```

### Performance
```bash
# Django debug toolbar (in development)
# Visit: http://localhost:8000 (check right side panel)

# SQL queries count
docker-compose exec site python manage.py shell -c "from django.db import connection; print(len(connection.queries))"

# Check slow queries
docker-compose exec db psql -U openimage_user openimage_db -c "SELECT query, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"
```

## 🚀 Deployment Commands

### Prepare for Production
```bash
# Collect static files
docker-compose exec site python manage.py collectstatic --noinput

# Compress static files
docker-compose exec site python manage.py compress

# Run security check
docker-compose exec site python manage.py check --deploy

# Test email configuration
docker-compose exec site python manage.py sendtestemail admin@example.com
```

### Production Deploy
```bash
# Pull latest code
git pull origin main

# Rebuild containers
docker-compose -f docker-compose.prod.yml build

# Start with production config
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec site python manage.py migrate

# Collect static
docker-compose -f docker-compose.prod.yml exec site python manage.py collectstatic --noinput
```

## 🔄 Backup & Restore

### Complete Backup
```bash
#!/bin/bash
# backup.sh - Complete system backup

BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

# Backup database
docker-compose exec -T db pg_dump -U openimage_user openimage_db > $BACKUP_DIR/database.sql

# Backup data
docker-compose exec -T site python manage.py dumpdata > $BACKUP_DIR/data.json

# Backup .env
cp .env $BACKUP_DIR/

# Backup uploaded files (if any)
docker cp openimage_site:/app/media $BACKUP_DIR/

echo "Backup completed: $BACKUP_DIR"
```

### Restore from Backup
```bash
#!/bin/bash
# restore.sh - Restore from backup

BACKUP_DIR=$1

# Stop services
docker-compose down

# Restore database
docker-compose up -d db
sleep 5
docker-compose exec -T db psql -U openimage_user openimage_db < $BACKUP_DIR/database.sql

# Start all services
docker-compose up -d

echo "Restore completed from: $BACKUP_DIR"
```

## 🧹 Cleanup Commands

### Clean Database
```bash
# Delete old images (older than 30 days)
docker-compose exec site python manage.py shell -c "
from you_image_generator.models import GeneratedImage
from django.utils import timezone
from datetime import timedelta
cutoff = timezone.now() - timedelta(days=30)
count = GeneratedImage.objects.filter(created_at__lt=cutoff).delete()[0]
print(f'Deleted {count} old images')
"

# Vacuum database
docker-compose exec db psql -U openimage_user openimage_db -c "VACUUM ANALYZE;"
```

### Clean Docker
```bash
# Remove stopped containers
docker-compose rm

# Clean images
docker system prune -a --volumes

# Clean build cache
docker builder prune -a
```

## 🆘 Emergency Commands

### Service Recovery
```bash
# Hard restart
docker-compose down
docker-compose up -d

# Reset site container
docker-compose stop site
docker-compose rm -f site
docker-compose up -d site

# Reset database (⚠️ deletes all data)
docker-compose down -v
docker-compose up -d
docker-compose exec site python manage.py migrate
```

### Debug Issues
```bash
# Check container health
docker-compose ps

# Inspect container
docker inspect openimage_site

# Check container logs
docker logs openimage_site --tail 100

# Run Django in debug mode
docker-compose exec site python manage.py runserver 0.0.0.0:8000 --verbosity 3
```

## 📚 Useful Aliases

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
# OpenImage aliases
alias oilogs='docker-compose logs -f site'
alias oisshell='docker-compose exec site python manage.py shell'
alias oimigrate='docker-compose exec site python manage.py makemigrations && docker-compose exec site python manage.py migrate'
alias oistatic='docker-compose exec site python manage.py collectstatic --noinput'
alias oirestart='docker-compose restart site'
alias oitest='docker-compose exec site python test_features.py'
alias oibackup='./backup.sh'
```

Then use:
```bash
oilogs      # View logs
oisshell    # Django shell
oimigrate   # Run migrations
oistatic    # Collect static
oirestart   # Restart
oitest      # Run tests
```

---

**💡 Tip**: Bookmark this page for quick reference!

**⚠️  Warning**: Commands marked with ⚠️ can delete data. Always backup first!