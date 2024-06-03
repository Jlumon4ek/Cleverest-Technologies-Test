from fastapi import APIRouter, HTTPException, Query, status
from typing import List
from models.schemas import BookSchema, BookCreateSchema
from services.book_service import BookService

router = APIRouter()


@router.get("/", response_model=List[BookSchema])
async def get_books(limit: int = Query(5, ge=1), offset: int = Query(0, ge=0)):
    return await BookService.get_books(limit, offset)


@router.get("/{book_id}", response_model=BookSchema)
async def get_book(book_id: int):
    return await BookService.get_book(book_id)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    await BookService.delete_book(book_id)


@router.post("/", response_model=BookSchema)
async def add_book(book: BookCreateSchema):
    return await BookService.add_book(book)
