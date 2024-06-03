from fastapi import APIRouter, HTTPException
from models.schemas import AuthorWithBooksSchema, AuthorSchema, AuthorCreateSchema
from services.author_service import AuthorService

router = APIRouter()


@router.get("/{author_id}", response_model=AuthorWithBooksSchema, tags=["authors"])
async def get_author(author_id: int):
    author_details = await AuthorService.get_author(author_id)
    if author_details is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author_details


@router.post("/", response_model=AuthorSchema, tags=["authors"])
async def add_author(author: AuthorCreateSchema):
    return await AuthorService.add_author(author)


@router.delete("/{author_id}", tags=["authors"])
async def delete_author(author_id: int):
    await AuthorService.delete_author(author_id)
    return {"message": "Author and all associated books have been deleted"}
