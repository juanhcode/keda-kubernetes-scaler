FROM python:3.11-slim

WORKDIR /app

# Instala la librería redis
RUN pip install redis

# Copia el script desde el contexto del build
COPY worker.py .

CMD ["python", "worker.py"]
