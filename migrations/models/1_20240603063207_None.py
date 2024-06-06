from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "Author" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "biography" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "Book" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "published_date" DATE,
    "author_id" INT NOT NULL REFERENCES "Author" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Genre" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "BookGenre" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "book_id" INT NOT NULL REFERENCES "Book" ("id") ON DELETE CASCADE,
    "genre_id" INT NOT NULL REFERENCES "Genre" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Reader" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "phone" VARCHAR(255) NOT NULL,
    "address" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "LibraryCard" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "reader_id" INT NOT NULL UNIQUE REFERENCES "Reader" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "book_genre" (
    "Book_id" INT NOT NULL REFERENCES "Book" ("id") ON DELETE CASCADE,
    "genre_id" INT NOT NULL REFERENCES "Genre" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_book_genre_Book_id_25c0ab" ON "book_genre" ("Book_id", "genre_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
