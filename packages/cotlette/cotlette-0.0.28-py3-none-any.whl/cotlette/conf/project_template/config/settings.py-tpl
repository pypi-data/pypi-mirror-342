import pathlib

# Базовая директория проекта
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': 'cotlette.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Путь к файлу базы данных
    }
}

ALLOWED_HOSTS = ['*']

DEBUG = True

INSTALLED_APPS = [
    'cotlette.apps.admin',
    'cotlette.apps.users'
]

TEMPLATES = [
    {
        "BACKEND": "cotlette.template.backends.jinja2.Jinja2",
        "DIRS": ["templates"],
        "APP_DIRS": True
    },
]