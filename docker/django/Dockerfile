FROM python:3.11-slim-bullseye

WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
COPY ./requirements.txt /app/requirements.txt

# Assurer une version récente de pip/setuptools/wheel
RUN pip install --upgrade pip setuptools wheel

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
