# docker commands

## Chercher des fichiers dans un container

docker exec -it <nom_conteneur_pgadmin> find / -name "*.backup" -o -name "*.sql"

docker exec -it <nom_conteneur_pgadmin> find / -name "open-image-v0-data.sql"

## Afficher le contenu d'un dossier dans un container

docker exec -it <nom_conteneur_pgadmin> ls -la /var/lib/pgadmin/storage/admin_openimage.com/

docker exec -it oi_pgadmin ls -la /var/lib/pgadmin/storage/admin_openimage.com/

## Copier un fichier dans un conteneur localement :

docker cp <nom_conteneur_pgadmin>:/chemin/vers/backup.sql ./backup.sql

docker cp oi_pgadmin:/var/lib/pgadmin/storage/admin_openimage.com/open-image-data-custom.backup ./open-image-data-custom.backup.sql

docker cp oi_pgadmin:/var/lib/pgadmin/storage/admin_openimage.com/open-image-v0-data.sql ./open-image-v0-data.sql

## Lister les containers en cours
docker ps

## Vérifier les ports exposés
docker ps | grep postgres

# docker-compose Commands

## Restart only site

docker-compose restart site

## Reconstruire le container

docker-compose down
docker-compose up -d --build

## Access container logs (CTRL+C for quiting)

docker-compose logs -f site

## Access container logs 

docker-compose logs --tail=100 service

## Entrez dans le container et exécuter manage.py

docker-compose exec site python manage.py shell

### Dans le shell Python :

from django.conf import settings
print(settings.GEMINI_API_KEY)

## Créér le fichier de migration

docker-compose exec site python manage.py makemigrations --empty you_image_generator --name add_metadata_fields

## Appliquer la migration

docker-compose exec site python manage.py migrate you_image_generator

## Vérifier si python-decouple est installé
docker-compose exec site pip show python-decouple

## Ou lister tous les packages
docker-compose exec site pip list | grep decouple

# curl Command to test api

```
curl -X POST "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell" \
  -H "Authorization: Bearer VOTRE_CLE_HF" \
  -H "Content-Type: application/json" \
  -d '{"inputs": "a red apple"}' \
  --output test.png

curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=YOUR_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}'

curl \
  -F "text=Hello world!" \
  -H "api-key: YOUR_DEEPAI_API_KEY" \
  https://api.deepai.org/api/text-generator

```

# Postgres

## Tester la connexion depuis votre machine
docker-compose exec db psql -U openimage_user -d openimage_db

## Exporter toute la base de données
docker-compose exec db pg_dump -U openimage_user openimage_db > backup-db-07102025.sql

## Méthode 1 : Restore PostgreSQL
docker-compose up -d db
docker-compose exec -T db psql -U openimage_user openimage_db < backup-db-07102025.sql

## Ou juste l'app image generator
docker-compose exec site python manage.py dumpdata you_image_generator > images_backup.json

# Méthode 2 : Load JSON
docker-compose exec site python manage.py loaddata images_backup.json

# Utile

## verif quota 

https://aistudio.google.com/app/apikey


# Backup database
docker-compose exec db pg_dump -U openimage_user openimage_db > backup.sql

# Backup images
docker-compose exec site python manage.py dumpdata you_image_generator > images_backup.json