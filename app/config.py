from os import environ

DATABASE_CONFIG = {
    "host": environ.get("POSTGRES_HOST", "localhost"),
    "password": environ.get("POSTGRES_PASSWORD", "ratestask"),
    "port": 5432,
    "database": "postgres",
    "user": environ.get("POSTGRES_USER", "postgres"),
}