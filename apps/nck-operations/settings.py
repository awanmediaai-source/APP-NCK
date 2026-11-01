from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent
SECRET_KEY = (BASE_DIR / '.secret').read_text().strip()
DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver']
INSTALLED_APPS = ['django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.staticfiles', 'core']
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF = 'urls'
TEMPLATES = [{'BACKEND':'django.template.backends.django.DjangoTemplates', 'DIRS':[BASE_DIR/'templates'], 'APP_DIRS':True, 'OPTIONS':{'context_processors':['django.template.context_processors.request']}}]
DATABASES = {'default':{'ENGINE':'django.db.backends.postgresql', 'NAME':os.getenv('NCK_DB','nck_operations'), 'USER':os.getenv('NCK_DB_USER',os.getenv('USER')), 'HOST':'127.0.0.1', 'PORT':'55432'}}
TIME_ZONE = 'Asia/Jakarta'
USE_TZ = True
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR/'static']
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_SAMESITE = 'Strict'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
