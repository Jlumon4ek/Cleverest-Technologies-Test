# schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class GenreSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class GenreCreateSchema(BaseModel):
    name: str


class AuthorSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class AuthorCreateSchema(BaseModel):
    name: str
    biography: Optional[str] = None


class BookSchema(BaseModel):
    id: int
    title: str
    published_date: Optional[date]
    author: AuthorSchema
    genres: List[GenreSchema]

    class Config:
        orm_mode = True


class BookCreateSchema(BaseModel):
    title: str
    published_date: Optional[date]
    author_id: int
    genre_ids: List[int]


class AuthorWithBooksSchema(BaseModel):
    id: int
    name: str
    biography: str
    books: List[BookSchema]

    class Config:
        orm_mode = True


class GenreWithBooksSchema(BaseModel):
    id: int
    name: str
    books: List[BookSchema]

    class Config:
        orm_mode = True

# schemas.py


class ReaderSchema(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    address: str

    class Config:
        orm_mode = True


class ReaderCreateSchema(BaseModel):
    name: str
    email: str
    phone: str
    address: str
