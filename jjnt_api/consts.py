from os import environ

DB_USER = environ.get("DB_USER", "db_user")
DB_PASSWORD = environ.get("DB_PASSWORD", "db_password")
DB_HOST = environ.get("DB_HOST", "db_host")
DB_PORT = int(environ.get("DB_PORT", "5432"))
DB_NAME = environ.get("DB_NAME", "bn_name")

# Others
LATEST_KNOWN = "posledni_znamy"
