from fastapi import APIRouter, HTTPException
from models.schemas import ReaderSchema, ReaderCreateSchema
from services.reader_service import ReaderService
from typing import List

router = APIRouter()


@router.post("/", response_model=ReaderSchema, tags=["readers"])
async def add_reader(reader: ReaderCreateSchema):
    return await ReaderService.add_reader(reader)


@router.get("/", response_model=List[ReaderSchema], tags=["readers"])
async def get_readers():
    return await ReaderService.get_readers()


@router.delete("/{reader_id}", tags=["readers"])
async def delete_reader(reader_id: int):
    await ReaderService.delete_reader(reader_id)
    return {"message": "Reader and the associated LibraryCard have been deleted"}


@router.delete("/library_card/{library_card_id}", tags=["readers"])
async def delete_library_card(library_card_id: int):
    await ReaderService.delete_library_card(library_card_id)
    return {"message": "LibraryCard and the associated reader have been deleted"}
