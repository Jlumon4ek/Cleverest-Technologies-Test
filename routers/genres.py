from fastapi import APIRouter, HTTPException
from models.schemas import GenreSchema, GenreCreateSchema, GenreWithBooksSchema
from services.genre_service import GenreService

router = APIRouter()


@router.delete("/{genre_id}", tags=["genres"])
async def delete_genre(genre_id: int):
    await GenreService.delete_genre(genre_id)
    return {"message": "Genre and all associated books have been deleted"}


@router.post("/", response_model=GenreSchema, tags=["genres"])
async def add_genre(genre: GenreCreateSchema):
    return await GenreService.add_genre(genre)


@router.get("/{genre_id}", response_model=GenreWithBooksSchema, tags=["genres"])
async def get_genre(genre_id: int):
    genre_details = await GenreService.get_genre(genre_id)
    if genre_details is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre_details
