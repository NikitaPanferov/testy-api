FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

COPY . /app

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

RUN openssl genrsa -out ./certs/jwt-private.pem 2048
RUN openssl rsa -in ./certs/jwt-private.pem -outform PEM -pubout -out ./certs/jwt-public.pem

EXPOSE 443

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443"]