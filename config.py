from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")


TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": f"{DB_HOST}",
                "port": f"{DB_PORT}",
                "user": f"{DB_USER}",
                "password": f"{DB_PASS}",
                "database": f"{DB_NAME}",
            }
        }
    },
    "apps": {
        "models": {
            "models": ["models.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


# TORTOISE_ORM = {
#     "connections": {"default": "sqlite://db.sqlite3"},  # Или ваша база данных
#     "apps": {
#         "models": {
#             # Убедитесь, что путь к вашим моделям правильный
#             "models": ["models.models", "aerich.models"],
#             "default_connection": "default",
#         },
#     },
# }
