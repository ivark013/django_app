import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "your-secret-key-here"

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "dashboard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "security_system.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "security_system.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email settings (replace with your actual email settings)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your_email@gmail.com"
EMAIL_HOST_PASSWORD = "your_email_password"

# Telegram settings (replace with your actual Telegram bot token)
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"

# WhatsApp settings (you'll need to implement this using a third-party service)
WHATSAPP_API_KEY = "your_whatsapp_api_key"

# AI model paths
AI_MODELS = {
    # "violence": {
    #    "model": os.path.join(
    #        BASE_DIR, "models", r"E:\مشاريع التخرج\security_system\models\vio_best2.pt"
    #    ),
    #    "yaml": os.path.join(
    #        BASE_DIR,
    #       "models",
    #      r"E:\مشاريع التخرج\security_system\models\violence_data.yaml",
    # ),
    # },
    # "thief": {
    #    "model": os.path.join(
    #       BASE_DIR, "models", r"E:\مشاريع التخرج\security_system\models\thief.pt"
    #  ),
    # "yaml": os.path.join(
    #    BASE_DIR,
    #   "models",
    #  r"E:\مشاريع التخرج\security_system\models\thief_data.yaml",
    # ),
    # },
    "thief_mask": {
        "model": os.path.join(
            BASE_DIR,
            "models",
            r"E:\مشاريع التخرج\security_system\models\theif-mask detection 2.pt",
        ),
        "yaml": os.path.join(
            BASE_DIR,
            "models",
            r"E:\مشاريع التخرج\security_system\models\theif-mask detection 2.yaml",
        ),
    },
    "weapon": {
        "model": os.path.join(
            BASE_DIR,
            "models",
            r"E:\مشاريع التخرج\security_system\models\gun-knife detection 2.pt",
        ),
        "yaml": os.path.join(
            BASE_DIR,
            "models",
            r"E:\مشاريع التخرج\security_system\models\weapon_data.yaml",
        ),
    },
}

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/accounts/login/"
