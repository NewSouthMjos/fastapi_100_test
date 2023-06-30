FROM python:3.11-slim-bullseye

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY ["uvicorn_settings.py", "entrypoint.sh", "alembic.ini", "/app/"]
COPY ./alembic ./alembic
COPY ./commons ./commons
COPY ./api ./api
COPY ./crud ./crud
COPY main.py .
RUN chmod +x entrypoint.sh
CMD ["sh", "entrypoint.sh"]