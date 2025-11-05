#!/bin/bash

# Script pour exécuter les commandes Django dans le conteneur Docker
# Usage: ./django-admin.sh <command>
# Exemples:
#   ./django-admin.sh makemigrations
#   ./django-admin.sh migrate  
#   ./django-admin.sh createsuperuser
#   ./django-admin.sh runserver

# Nom du service Django dans docker-compose.yml (à ajuster si différent)
DJANGO_SERVICE="django"

if [ $# -eq 0 ]; then
    echo "Usage: $0 <django-command> [args...]"
    echo "Exemples:"
    echo "  $0 makemigrations"
    echo "  $0 migrate"
    echo "  $0 createsuperuser" 
    echo "  $0 shell"
    echo "  $0 runserver"
    echo "  $0 collectstatic"
    exit 1
fi

# Vérifier si docker compose est en cours d'exécution
if ! docker compose ps | grep -q "$DJANGO_SERVICE"; then
    echo "Le service Django n'est pas en cours d'exécution."
    echo "Lancez d'abord: docker compose up -d"
    exit 1
fi

# Exécuter la commande Django dans le conteneur
docker compose exec "$DJANGO_SERVICE" python manage.py "$@"