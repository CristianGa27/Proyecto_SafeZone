# -*- coding: utf-8 -*-
import os

from dotenv import load_dotenv

# Carga las variables desde el archivo .env
load_dotenv()

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "TU_CLAVE_SECRETA_SUPER_SEGURA_AQUI_12345")

MAIL_CONFIG = {
    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT': 587,
    'MAIL_USE_TLS': True,
    'MAIL_USERNAME': 'criscagarpa@gmail.com',
    'MAIL_PASSWORD': os.getenv("MAIL_PASSWORD", ""),
    'MAIL_DEFAULT_SENDER': 'SafeZone <criscagarpa@gmail.com>',
}

DB_CONFIG = {
    'host': os.getenv("DB_HOST", "localhost"),
    'user': os.getenv("DB_USER", "root"),
    'password': os.getenv("DB_PASSWORD", ""),
    'database': os.getenv("DB_NAME", "Prueba"),
    'port': 3306,
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'use_unicode': True,
}

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'static/uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
