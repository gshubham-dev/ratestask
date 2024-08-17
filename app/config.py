from os import environ

# Configuration dictionary for database connection
DATABASE_CONFIG = {
    "host": environ.get("POSTGRES_HOST", "localhost"),
    "password": environ.get("POSTGRES_PASSWORD", "ratestask"),
    "port": 5432,  # Default PostgreSQL port
    "database": "postgres",  # Default database name
    "user": environ.get("POSTGRES_USER", "postgres"),
}
