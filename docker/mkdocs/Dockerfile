FROM python:3.11-slim-bullseye
WORKDIR /app
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libglib2.0-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install mkdocs-with-pdf==0.9.3 mkdocs-material
EXPOSE 8001
CMD ["mkdocs", "serve", "--dev-addr=0.0.0.0:8000"]
