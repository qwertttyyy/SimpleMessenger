# SimpleMessenger

## Тестовое задание на позицию Python Developer 

## Техническое задание
Ваша задача - написать RESTful API простого мессенджера.
Реализуемый функционал:
- Механизм авторизации
- Поиск пользователей
- Возможность отправлять личные сообщения
- Настройки пользователя (username, аватар, номер телефона, т.п.)

Для реализации используйте FastAPI и MongoDB.


## Используемый стек
- Python
- FastAPI
- MongoDB
- Motor
- WebSockets


## Начало работы
Для локального запуска SimpleMessenger выполните следующие шаги:

1. Клонирование репозитория и установка зависимостей:
    ```bash
    git clone git@github.com:qwertttyyy/SimpleMessenger.git
    cd SimpleMessenger
    pip install -r requirements.txt
    ```
2. Создайте файл .env 
    ```dotenv
   APP_TITLE=SimpleMessanger
   DATABASE_URL=mongodb://localhost:27017   # url адрес MongoDB сервера
   DATABASE_NAME=db                         # Имя базы данных
   SECRET=SECRET                            # Секретный ключ для шифрования
   JWT_LIFETIME_SECONDS=3600                # <Кол-во секнуду жизни JWT токена>
   ```

2. Для работы проекта должен быть запущен MongoDB сервер. <br>
Укажите url сервера в файле .env, если он отличный от дефолтного

3. Запуск сервера FastAPI:
    ```bash
    uvicorn main:app --reload
    ```

#### Приложение будет доступно по адресу http://127.0.0.1:8000
#### Swagger документация http://127.0.0.1:8000/docs

