FROM python:3.10-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
RUN ["pip", "install", "-r", "requirements.txt"]

COPY bot /app

# Компилируем переводы
RUN pybabel compile -d locales -D bot

# Ждём, пока база будет готова
CMD bash -c "
    echo 'Waiting for the database to be healthy...';
    until mysqladmin ping -h \"$DB_ADDRESS\" -u\"$DB_USER\" -p\"$DB_PASS\" --silent; do
      sleep 2;
    done;
    echo 'Database is ready!';
    alembic upgrade head;
    exec python main.py
"