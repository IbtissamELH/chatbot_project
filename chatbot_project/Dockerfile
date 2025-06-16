FROM python:3.11-slim

# 1. Installer dépendances
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Créer dossier de travail
WORKDIR /app

# 3. Copier projet
COPY . /app

# 4. Installer les libs Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 5. Collecter les fichiers statiques (Django)
RUN python manage.py collectstatic --noinput

# 6. Exposer le port par défaut de Django (⚠️ Hugging Face n'accepte que 7860+)
ENV PORT 7860
EXPOSE 7860

# 7. Commande de démarrage
CMD ["python", "manage.py", "runserver", "0.0.0.0:7860"]
