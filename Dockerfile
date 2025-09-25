FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1


WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
build-essential curl netcat-traditional \
&& rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY ./app ./app
COPY alembic.ini alembic.ini
COPY migrations ./migrations
COPY .env .env
COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh


CMD ["./entrypoint.sh"]