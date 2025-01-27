# Verwende das offizielle Python 3.12.3-Image
FROM python:3.12.3-slim

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Installiere systemweite Abhängigkeiten für OpenCV
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

# Kopiere die requirements.txt ins Arbeitsverzeichnis
COPY requirements.txt ./

# Installiere die Abhängigkeiten aus der requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere die main.py und andere Dateien ins Arbeitsverzeichnis
COPY main.py ./
COPY backend ./backend
COPY static ./static
COPY templates ./templates
COPY secret.py ./

EXPOSE 5004

# Kommando, um die main.py zu starten
CMD ["python", "main.py"]
