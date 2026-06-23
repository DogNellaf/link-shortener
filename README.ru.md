# Сервис сокращения ссылок

> [🇬🇧 English](README.md) | 🇷🇺 Русский

Веб-сервис для сокращения ссылок и генерации QR-кодов, построенный на Django. Создавайте короткие ссылки, сохраняйте их в избранное, отслеживайте историю и генерируйте стилизованные QR-коды — с аккаунтом и без него.

## Возможности

- Генерация коротких ссылок (для авторизованных и анонимных пользователей)
- Пользовательские названия ссылок
- Избранное и история ссылок и QR-кодов
- Генератор QR-кодов с настройкой цвета и логотипа
- Поддержка deep-link для iOS-приложений (YouTube, Telegram, Instagram, Google Docs/Drive/Sheets)
- Регистрация, вход и восстановление пароля по email
- Управление профилем: имя, email, аватар
- Адаптивный интерфейс на Bootstrap 5
- Панель администратора Django

## Стек разработки

| Слой | Технология |
|---|---|
| Backend | Python 3.11, Django 5.1 |
| База данных | SQLite (разработка) / PostgreSQL (продакшн) |
| Frontend | Bootstrap 5, Vanilla JS |
| QR-коды | segno, django-qr-code |
| Обработка изображений | Pillow |
| Статика | WhiteNoise |
| Деплой | Docker, Gunicorn |

## Требования

- Python 3.11+
- pip

## Установка

```bash
# Клонируйте репозиторий
git clone https://github.com/DogNellaf/link-shortener
cd link-shortener

# Создайте и активируйте виртуальное окружение
python -m venv .venv
source .venv/bin/activate       # Linux / macOS
.venv\Scripts\Activate.ps1      # Windows (PowerShell)

# Установите зависимости
pip install -r requirements.txt

# Примените миграции
python manage.py migrate

# (Опционально) Создайте суперпользователя
python manage.py createsuperuser

# Запустите сервер разработки
python manage.py runserver
```

Сервис будет доступен по адресу `http://127.0.0.1:8000/`.

### Docker

```bash
docker-compose up --build
```

## Переменные окружения

| Переменная | Описание | По умолчанию |
|---|---|---|
| `SECRET_KEY` | Секретный ключ Django | небезопасный dev-ключ |
| `DEBUG` | Режим отладки (`True`/`False`) | `True` |
| `ALLOWED_HOSTS` | Список допустимых хостов через запятую | `*` |
| `IS_FOR_RENDER` | Использовать PostgreSQL и WhiteNoise | `false` |
| `DB_NAME` | Имя базы данных PostgreSQL | `linkshortener` |
| `DB_USER` | Пользователь PostgreSQL | `db_user` |
| `DB_PASSWORD` | Пароль PostgreSQL | _(пусто)_ |
| `DB_HOST` | Хост PostgreSQL | `localhost` |
| `DB_PORT` | Порт PostgreSQL | `5432` |
| `EMAIL_HOST_USER` | SMTP-логин для писем восстановления пароля | _(пусто)_ |
| `EMAIL_HOST_PASSWORD` | SMTP-пароль | _(пусто)_ |

## Запуск тестов

```bash
python manage.py test core custom_auth account
```

## Структура проекта

```
link-shortener/
├── linkshortener/         # Настройки Django и корневые URL
├── core/                  # Сокращение ссылок: модели, представления, утилиты, тесты
│   ├── models.py          # Модели ShortedUrl и Qr
│   ├── views.py           # Представления
│   ├── utils.py           # Генерация коротких кодов
│   └── tests.py           # Тесты
├── custom_auth/           # Авторизация: регистрация, вход, сброс пароля
│   ├── models.py          # Модели CustomUser и PasswordResetCode
│   ├── views.py           # Представления авторизации
│   └── tests.py           # Тесты
├── account/               # Управление профилем пользователя
│   ├── views.py           # Представления аккаунта
│   └── tests.py           # Тесты
├── templates/             # HTML-шаблоны
├── static/                # CSS, JS, изображения, шрифты
├── media/                 # Файлы пользователей (аватары, логотипы QR)
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Лицензия

[CC BY-NC 4.0](LICENSE) — при любом использовании обязательно указание авторства; коммерческое использование требует предварительного письменного разрешения правообладателя.
