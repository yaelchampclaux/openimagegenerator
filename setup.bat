@echo off
REM Script d'installation automatique pour OpenImage (Windows)
REM Usage: Double-cliquez sur setup.bat

echo ========================================
echo   OpenImage - AI Image Generator Setup
echo ========================================
echo.

REM Vérifier Python
echo [INFO] Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python n'est pas installe ou n'est pas dans le PATH
    echo Telechargez Python sur: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [INFO] Python %PYTHON_VERSION% detecte
echo.

REM Créer l'environnement virtuel
if not exist "venv" (
    echo [INFO] Creation de l'environnement virtuel...
    python -m venv venv
) else (
    echo [WARN] L'environnement virtuel existe deja
)
echo.

REM Activer l'environnement virtuel
echo [INFO] Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Mettre à jour pip
echo [INFO] Mise a jour de pip...
python -m pip install --upgrade pip --quiet

REM Installer les dépendances
echo [INFO] Installation des dependances...
echo Cette etape peut prendre plusieurs minutes...
pip install -r requirements.txt --quiet
echo.

REM Créer le fichier .env si inexistant
if not exist ".env" (
    echo [INFO] Creation du fichier .env...
    (
        echo # Django Settings
        echo SECRET_KEY=django-insecure-change-this-in-production
        echo DEBUG=True
        echo ALLOWED_HOSTS=localhost,127.0.0.1
        echo.
        echo # ===================================
        echo # AI Image Generation API Keys
        echo # ===================================
        echo.
        echo # Google Gemini - GRATUIT ^(1500/jour^)
        echo # Get key: https://aistudio.google.com/app/apikey
        echo GEMINI_API_KEY=
        echo.
        echo # Hugging Face - GRATUIT ^(optionnel^)
        echo # Get key: https://huggingface.co/settings/tokens
        echo HUGGINGFACE_API_KEY=
        echo.
        echo # DeepAI - GRATUIT ^(optionnel^)
        echo # Get key: https://deepai.org/dashboard/profile
        echo DEEPAI_API_KEY=
        echo.
        echo # Runware - PAYANT ^($0.002/image^)
        echo # Get key: https://my.runware.ai/keys
        echo RUNWARE_API_KEY=
        echo.
        echo # Replicate - PAYANT ^(pay-per-use^)
        echo # Get key: https://replicate.com/account/api-tokens
        echo REPLICATE_API_KEY=
        echo.
        echo # Stability AI - PAYANT
        echo # Get key: https://platform.stability.ai/account/keys
        echo STABILITY_AI_API_KEY=
        echo.
        echo # Default provider
        echo DEFAULT_IMAGE_PROVIDER=pollinations
    ) > .env
    echo [INFO] Fichier .env cree
) else (
    echo [WARN] Le fichier .env existe deja
)
echo.

REM Créer les dossiers nécessaires
echo [INFO] Creation des dossiers...
if not exist "static" mkdir static
if not exist "staticfiles" mkdir staticfiles
if not exist "test_outputs" mkdir test_outputs
echo.

REM Migrations de la base de données
echo [INFO] Application des migrations...
python manage.py migrate
echo.

REM Collecter les fichiers statiques
echo [INFO] Collecte des fichiers statiques...
python manage.py collectstatic --noinput
echo.

REM Demander création superuser
echo.
set /p CREATE_SUPER="Voulez-vous creer un superutilisateur Django ? (o/n): "
if /i "%CREATE_SUPER%"=="o" (
    python manage.py createsuperuser
)
echo.

REM Afficher le résumé
echo ========================================
echo [INFO] Installation terminee !
echo ========================================
echo.
echo Prochaines etapes :
echo.
echo 1. Ajoutez vos cles API dans le fichier .env
echo    Minimum recommande : GEMINI_API_KEY
echo    Obtenez-la sur : https://aistudio.google.com/app/apikey
echo.
echo 2. Testez les APIs configurees :
echo    python test_all_apis.py
echo.
echo 3. Lancez le serveur de developpement :
echo    python manage.py runserver
echo.
echo 4. Ouvrez votre navigateur sur :
echo    http://localhost:8000
echo.
echo ========================================
echo.
echo [INFO] Providers disponibles sans configuration :
echo    - Pollinations.ai ^(Gratuit, aucune cle requise^)
echo    - Placeholder ^(Pour tests uniquement^)
echo.
echo [WARN] Pour de meilleurs resultats, configurez Gemini ^(gratuit^)
echo.
echo Documentation complete dans README.md
echo Problemes ? Consultez SETUP_GUIDE.md
echo.
pause