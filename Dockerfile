# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Dependencies installieren
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Prefect (falls nicht in requirements.txt, aber wir setzen es lieber rein)
RUN pip install prefect

# Dein Projekt kopieren
COPY . .

# Standard-Kommando (kann in docker-compose überschrieben werden)
CMD ["python", "pipeline.py"]
