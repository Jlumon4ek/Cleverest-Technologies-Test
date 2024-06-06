from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from routers import books, authors, genres, readers
from models.models import *
from models.schemas import *
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(authors.router, prefix="/authors", tags=["authors"])
app.include_router(genres.router, prefix="/genres", tags=["genres"])
app.include_router(readers.router, prefix="/readers", tags=["readers"])
