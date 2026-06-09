import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

    ENTRA_CLIENT_ID = os.getenv("ENTRA_CLIENT_ID")
    ENTRA_CLIENT_SECRET = os.getenv("ENTRA_CLIENT_SECRET")
    ENTRA_TENANT_ID = os.getenv("ENTRA_TENANT_ID")

    ENTRA_AUTHORITY = f"https://login.microsoftonline.com/{ENTRA_TENANT_ID}"
    ENTRA_SCOPE = ["User.Read"]

    DB_SERVER = os.getenv("DB_SERVER")
    DB_NAME = os.getenv("DB_NAME")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    ADMIN_EMAILS = [
        email.strip().lower()
        for email in os.getenv("ADMIN_EMAILS", "").split(",")
        if email.strip()
    ]

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"