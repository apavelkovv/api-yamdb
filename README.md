# YaMDb

Проект **YaMDb** собирает отзывы пользователей на произведения (фильмы, книги, музыку). Сами произведения в YaMDb не хранятся — здесь нельзя посмотреть фильм или послушать музыку. Произведения делятся на категории и жанры, пользователи оставляют текстовые отзывы и ставят оценки, из которых формируется усреднённый рейтинг произведения. Пользователи также могут комментировать отзывы друг друга.

## Авторы

- [Артем Павелков](https://github.com/apavelkovv) — регистрация и аутентификация, права доступа, работа с токеном
- [Карим Гатауллин](https://github.com/a1zyG) — модели, view и эндпоинты для произведений, категорий, жанров;
- [Дарья Глухова](https://github.com/daria-gluhova) — отзывы, комментарии, рейтинг произведений
- [Максим Ткаченко](https://github.com/DrFaustus1) — модели, view и эндпоинты для отзывов, комментариев; импорт данных из CSV

## Стек технологий

- Python 3.12
- Django 5.1
- Django REST Framework
- Simple JWT
- django-filter
- SQLite

## Как развернуть проект локально

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone git@github.com:username/api_yamdb.git
cd api_yamdb
```

Создать и активировать виртуальное окружение:

```bash
python3 -m venv venv
source venv/bin/activate   # для Linux/macOS
source venv/Scripts/activate   # для Windows
```

Установить зависимости из файла requirements.txt:

```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции:

```bash
python3 manage.py migrate
```

Импортировать тестовые данные из CSV (опционально):

```bash
python3 manage.py import_csv
```

Запустить проект:

```bash
python3 manage.py runserver
```

## Примеры запросов

Регистрация нового пользователя:

```
POST /api/v1/auth/signup/
{
  "email": "user@example.com",
  "username": "user"
}
```

Получение JWT-токена:

```
POST /api/v1/auth/token/
{
  "username": "user",
  "confirmation_code": "confirmation_code_from_email"
}
```

Получение списка всех категорий:

```
GET /api/v1/categories/
```

Полная документация API доступна после запуска проекта по адресу `/redoc/`.