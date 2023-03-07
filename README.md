# API для онлайн платформы торговой сети электроники
###### Тестовое задание

## Запуск проекта:
1. Склонировать репозиторий на локальный компьютер.
2. Установить сервисы Docker и Docker Compose.
3. Переименовать файл `.env.example` в `.env` и заполнить его по шаблону внутри файла.
4. Запустить контейнер с PostgreSQL командой `docker compose up -d`.
5. Создать и накатить миграции в базе данных командами `./manage.py makemigrations` и `./manage.py migrate`.
6. Запустить веб-сервер для разработки командой './manage.py runserver'
7. Backend будет досупен по адресу 'http://127.0.0.1:8000/'

## Доступные маршруты:
### Модель Link:
  * `link/` - CRUD для звеньев (объектов) торговой сети

### Модель User:
  * `user/signup/` - создание пользователя
  * `user/login/` - аутентификация пользователя
  * `user/profile/` - карточка пользователя
  * `user/logout/` - выход из системы
  
###### Примечание: CRUD для пользователя был сделан для удобства его создания через форму DRF.
