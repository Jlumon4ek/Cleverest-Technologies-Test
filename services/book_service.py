from fastapi import HTTPException
from models.models import Book, Author, Genre, BookGenre
from models.schemas import BookCreateSchema, BookSchema


class BookService:

    @staticmethod
    async def get_books(limit: int, offset: int):
        books = await Book.all().prefetch_related("author").offset(offset).limit(limit)
        books_with_details = []
        for book in books:
            genres = await book.get_genres()
            book_details = {
                "id": book.id,
                "title": book.title,
                "published_date": book.published_date,
                "author": {"id": book.author.id, "name": book.author.name},
                "genres": [{"id": genre.id, "name": genre.name} for genre in genres]
            }
            books_with_details.append(book_details)
        return books_with_details

    @staticmethod
    async def get_book(book_id: int):
        book = await Book.get_or_none(id=book_id).prefetch_related("author")
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        genres = await book.get_genres()
        book_details = {
            "id": book.id,
            "title": book.title,
            "published_date": book.published_date,
            "author": {"id": book.author.id, "name": book.author.name},
            "genres": [{"id": genre.id, "name": genre.name} for genre in genres]
        }
        return book_details

    @staticmethod
    async def delete_book(book_id: int):
        book = await Book.get_or_none(id=book_id)
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        await book.delete()

    @staticmethod
    async def add_book(book: BookCreateSchema):
        author = await Author.get_or_none(id=book.author_id)
        if author is None:
            raise HTTPException(status_code=404, detail="Author not found")

        book_obj = await Book.create(
            title=book.title,
            published_date=book.published_date,
            author_id=book.author_id
        )

        for genre_id in book.genre_ids:
            genre = await Genre.get_or_none(id=genre_id)
            if genre is None:
                raise HTTPException(status_code=404, detail=f"Genre with id {
                                    genre_id} not found")
            await BookGenre.create(book_id=book_obj.id, genre_id=genre_id)

        await book_obj.fetch_related("author", "genres")

        genres = await book_obj.get_genres()
        book_details = {
            "id": book_obj.id,
            "title": book_obj.title,
            "published_date": book_obj.published_date,
            "author": {"id": book_obj.author.id, "name": book_obj.author.name},
            "genres": [{"id": genre.id, "name": genre.name} for genre in genres]
        }

        return book_details
