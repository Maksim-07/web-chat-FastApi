# Веб чат на FastApi и SQLAlchemy

## Инструкция для развертывания приложения

### 1. Клонирование репозитория

``` Bash
git clone https://github.com/Maksim-07/web-chat-FastApi.git

cd web-chat-FastApi
```

### 2. Создание окружения

Установка poetry и необходимых пакетов:

``` Bash
pip install poetry

cd .\src\
poetry install
```

### 3. Настройка переменных окружения Python

Создать файл ```.env``` в корневой папке ```src``` и заполнить следующим содержимым:

```
POSTGRES_HOST="web-chat-db"
POSTGRES_PORT=5532
POSTGRES_USER="web-chat-db"
POSTGRES_PASSWORD="web-chat-db"
POSTGRES_DB="web-chat-db"

ALGORITHM="your-algorithm"
SECRET_KEY="your-secret-key-for-jwt-token"
```

### 4. Запуск приложения с помощью Docker Compose

``` Bash
docker-compose up -d
```

