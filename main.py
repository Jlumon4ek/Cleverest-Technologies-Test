from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from routers import books, authors, genres, readers


from tortoise.transactions import in_transaction
from fastapi import HTTPException
from models.models import *
from models.schemas import *


app = FastAPI()

register_tortoise(
    app,
    db_url=f"postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    modules={"models": ["models.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(authors.router, prefix="/authors", tags=["authors"])
app.include_router(genres.router, prefix="/genres", tags=["genres"])
app.include_router(readers.router, prefix="/readers", tags=["readers"])
