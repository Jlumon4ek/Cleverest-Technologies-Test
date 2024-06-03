from fastapi import HTTPException
from models.models import Reader, LibraryCard
from models.schemas import ReaderCreateSchema, ReaderSchema
from tortoise.transactions import in_transaction


class ReaderService:

    @staticmethod
    async def add_reader(reader: ReaderCreateSchema):
        async with in_transaction() as conn:
            reader_obj = await Reader.create(
                name=reader.name,
                email=reader.email,
                phone=reader.phone,
                address=reader.address
            )
            await LibraryCard.create(
                reader=reader_obj
            )
        return reader_obj

    @staticmethod
    async def get_readers():
        return await Reader.all()

    @staticmethod
    async def delete_reader(reader_id: int):
        async with in_transaction() as conn:
            reader = await Reader.get_or_none(id=reader_id).using_db(conn)
            if reader is None:
                raise HTTPException(status_code=404, detail="Reader not found")

            library_card = await LibraryCard.get_or_none(reader_id=reader_id).using_db(conn)
            if library_card:
                await library_card.delete(using_db=conn)

            await reader.delete(using_db=conn)

    @staticmethod
    async def delete_library_card(library_card_id: int):
        async with in_transaction() as conn:
            library_card = await LibraryCard.get_or_none(id=library_card_id).using_db(conn)
            if library_card is None:
                raise HTTPException(
                    status_code=404, detail="LibraryCard not found")

            reader_id = library_card.reader_id
            await library_card.delete(using_db=conn)

            reader = await Reader.get_or_none(id=reader_id).using_db(conn)
            if reader:
                await reader.delete(using_db=conn)
