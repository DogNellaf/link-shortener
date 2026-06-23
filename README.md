# URL Shortener

> 🇬🇧 English | [🇷🇺 Русский](README.ru.md)

A web service for shortening URLs and generating QR codes, built with Django. Create short links, save them to favourites, track history, and generate styled QR codes — all with or without an account.

## Features

- Short link generation (anonymous and authenticated)
- Custom link titles
- Favourites and history for links and QR codes
- QR code generator with colour and logo customisation
- Deep-link support for iOS apps (YouTube, Telegram, Instagram, Google Docs/Drive/Sheets)
- User registration, login, and password recovery via email
- Profile management: name, email, avatar
- Responsive UI built with Bootstrap 5
- Django admin panel for content management

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, Django 5.1 |
| Database | SQLite (development) / PostgreSQL (production) |
| Frontend | Bootstrap 5, Vanilla JS |
| QR codes | segno, django-qr-code |
| Image processing | Pillow |
| Static files | WhiteNoise |
| Deployment | Docker, Gunicorn |

## Requirements

- Python 3.11+
- pip

## Installation

```bash
# Clone the repository
git clone https://github.com/DogNellaf/link-shortener
cd link-shortener

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate       # Linux / macOS
.venv\Scripts\Activate.ps1      # Windows (PowerShell)

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# (Optional) Create an admin account
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

The service will be available at `http://127.0.0.1:8000/`.

### Docker

```bash
docker-compose up --build
```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Django secret key | insecure dev key |
| `DEBUG` | Enable debug mode (`True`/`False`) | `True` |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | `*` |
| `IS_FOR_RENDER` | Use PostgreSQL and WhiteNoise static storage | `false` |
| `DB_NAME` | PostgreSQL database name | `linkshortener` |
| `DB_USER` | PostgreSQL user | `db_user` |
| `DB_PASSWORD` | PostgreSQL password | _(empty)_ |
| `DB_HOST` | PostgreSQL host | `localhost` |
| `DB_PORT` | PostgreSQL port | `5432` |
| `EMAIL_HOST_USER` | SMTP login for password recovery emails | _(empty)_ |
| `EMAIL_HOST_PASSWORD` | SMTP password | _(empty)_ |

## Running Tests

```bash
python manage.py test core custom_auth account
```

## Project Structure

```
link-shortener/
├── linkshortener/         # Django project settings and root URL conf
├── core/                  # URL shortening: models, views, utils, tests
│   ├── models.py          # ShortedUrl and Qr models
│   ├── views.py           # View functions
│   ├── utils.py           # Short-code generation
│   └── tests.py           # Test suite
├── custom_auth/           # Authentication: registration, login, password reset
│   ├── models.py          # CustomUser and PasswordResetCode models
│   ├── views.py           # Auth views
│   └── tests.py           # Test suite
├── account/               # User profile management
│   ├── views.py           # Account views
│   └── tests.py           # Test suite
├── templates/             # HTML templates
├── static/                # CSS, JS, images, fonts
├── media/                 # User-uploaded files (avatars, QR logos)
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## License

[CC BY-NC 4.0](LICENSE) — attribution required for any use; commercial use requires prior written permission from the copyright holder.
