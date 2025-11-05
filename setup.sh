#!/bin/bash

# Script d'installation automatique pour OpenImage
# Usage: chmod +x setup.sh && ./setup.sh

set -e  # Exit on error

echo "🎨 OpenImage - Multi-Provider AI Image Generator"
echo "=================================================="
echo ""

# Couleurs pour l'affichage
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier Python
info "Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    error "Python 3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
info "Python $PYTHON_VERSION détecté"

# Créer l'environnement virtuel
if [ ! -d "venv" ]; then
    info "Création de l'environnement virtuel..."
    python3 -m venv venv
else
    warning "L'environnement virtuel existe déjà"
fi

# Activer l'environnement virtuel
info "Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
info "Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

# Créer le fichier .env si inexistant
if [ ! -f ".env" ]; then
    info "Création du fichier .env..."
    cat > .env << 'EOF'
# Django Settings
SECRET_KEY=django-insecure-$(openssl rand -base64 32)
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
# Uncomment below for PostgreSQL
# DATABASE_URL=postgres://user:password@localhost:5432/dbname

# ===================================
# AI Image Generation API Keys
# ===================================

# Google Gemini - GRATUIT (1500/jour)
# Get key: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=

# Hugging Face - GRATUIT (optionnel)
# Get key: https://huggingface.co/settings/tokens
HUGGINGFACE_API_KEY=

# DeepAI - GRATUIT (optionnel)
# Get key: https://deepai.org/dashboard/profile
DEEPAI_API_KEY=

# Runware - PAYANT ($0.002/image)
# Get key: https://my.runware.ai/keys
RUNWARE_API_KEY=

# Replicate - PAYANT (pay-per-use)
# Get key: https://replicate.com/account/api-tokens
REPLICATE_API_KEY=

# Stability AI - PAYANT
# Get key: https://platform.stability.ai/account/keys
STABILITY_AI_API_KEY=

# Default provider
DEFAULT_IMAGE_PROVIDER=pollinations
EOF
    info "Fichier .env créé. Veuillez ajouter vos clés API."
else
    warning "Le fichier .env existe déjà"
fi

# Créer les dossiers nécessaires
info "Création des dossiers..."
mkdir -p static staticfiles test_outputs

# Migrations de la base de données
info "Application des migrations..."
python manage.py migrate

# Collecter les fichiers statiques
info "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Créer un superuser (optionnel)
echo ""
read -p "Voulez-vous créer un superutilisateur Django ? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Afficher le résumé
echo ""
echo "=================================================="
info "✅ Installation terminée !"
echo "=================================================="
echo ""
echo "📋 Prochaines étapes :"
echo ""
echo "1. Ajoutez vos clés API dans le fichier .env"
echo "   Minimum recommandé : GEMINI_API_KEY"
echo "   Obtenez-la sur : https://aistudio.google.com/app/apikey"
echo ""
echo "2. Testez les APIs configurées :"
echo "   python test_all_apis.py"
echo ""
echo "3. Lancez le serveur de développement :"
echo "   python manage.py runserver"
echo ""
echo "4. Ouvrez votre navigateur sur :"
echo "   http://localhost:8000"
echo ""
echo "=================================================="
echo ""
info "🎨 Providers disponibles sans configuration :"
echo "   • Pollinations.ai (Gratuit, aucune clé requise)"
echo "   • Placeholder (Pour tests uniquement)"
echo ""
warning "⚠️  Pour de meilleurs résultats, configurez au moins Gemini (gratuit)"
echo ""
echo "📚 Documentation complète dans README.md"
echo "🆘 Problèmes ? Consultez SETUP_GUIDE.md"
echo ""