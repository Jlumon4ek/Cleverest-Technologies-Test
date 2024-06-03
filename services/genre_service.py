from fastapi import HTTPException
from models.models import Book, Genre, BookGenre
from models.schemas import GenreCreateSchema, GenreWithBooksSchema
from tortoise.transactions import in_transaction


class GenreService:

    @staticmethod
    async def delete_genre(genre_id: int):
        async with in_transaction() as conn:
            genre = await Genre.get_or_none(id=genre_id).using_db(conn)
            if genre is None:
                raise HTTPException(status_code=404, detail="Genre not found")

            # Найти все книги, связанные с этим жанром
            book_genres = await BookGenre.filter(genre_id=genre_id).using_db(conn)
            book_ids = [book_genre.book_id for book_genre in book_genres]

            # Удалить все записи в таблице связей BookGenre
            await BookGenre.filter(genre_id=genre_id).using_db(conn).delete()

            # Удалить все книги, связанные с этим жанром
            for book_id in book_ids:
                book = await Book.get_or_none(id=book_id).using_db(conn)
                if book:
                    await book.delete(using_db=conn)

            # Удалить сам жанр
            await genre.delete(using_db=conn)

    @staticmethod
    async def add_genre(genre: GenreCreateSchema):
        genre_obj = await Genre.create(name=genre.name)
        return genre_obj

    @staticmethod
    async def get_genre(genre_id: int):
        genre = await Genre.get_or_none(id=genre_id)
        if genre is None:
            return None

        book_genres = await BookGenre.filter(genre_id=genre_id).prefetch_related("book__author")
        books = []
        for book_genre in book_genres:
            book = book_genre.book
            genres = await book.get_genres()
            book_details = {
                "id": book.id,
                "title": book.title,
                "published_date": book.published_date,
                "author": {"id": book.author.id, "name": book.author.name},
                "genres": [{"id": genre.id, "name": genre.name} for genre in genres]
            }
            books.append(book_details)

        genre_details = {
            "id": genre.id,
            "name": genre.name,
            "books": books
        }
        return genre_details
