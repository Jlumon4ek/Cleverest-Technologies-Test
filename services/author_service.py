from fastapi import HTTPException
from models.models import Author, Book, Genre, BookGenre
from models.schemas import AuthorWithBooksSchema, AuthorSchema, AuthorCreateSchema
from tortoise.transactions import in_transaction


class AuthorService:

    @staticmethod
    async def get_author(author_id: int):
        author = await Author.get_or_none(id=author_id).prefetch_related("books")
        if author is None:
            return None

        books = []
        for book in author.books:
            genres = await book.get_genres()
            book_details = {
                "id": book.id,
                "title": book.title,
                "published_date": book.published_date,
                "author": {"id": author.id, "name": author.name},
                "genres": [{"id": genre.id, "name": genre.name} for genre in genres]
            }
            books.append(book_details)

        author_details = {
            "id": author.id,
            "name": author.name,
            "biography": author.biography,
            "books": books
        }
        return author_details

    @staticmethod
    async def add_author(author: AuthorCreateSchema):
        author_obj = await Author.create(
            name=author.name,
            biography=author.biography
        )
        return author_obj

    @staticmethod
    async def delete_author(author_id: int):
        async with in_transaction() as conn:
            author = await Author.get_or_none(id=author_id).using_db(conn)
            if author is None:
                raise HTTPException(status_code=404, detail="Author not found")

            books = await Book.filter(author_id=author_id).using_db(conn)
            for book in books:
                await BookGenre.filter(book_id=book.id).using_db(conn).delete()
                await book.delete(using_db=conn)

            await author.delete(using_db=conn)
