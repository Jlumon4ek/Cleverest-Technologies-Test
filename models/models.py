from tortoise.models import Model
from tortoise import fields


class Author(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    biography = fields.TextField()

    class Meta:
        table = "Author"


class Book(Model):
    id = fields.IntField(primary_key=True)
    title = fields.CharField(max_length=255)
    author = fields.ForeignKeyField('models.Author', related_name='books')
    published_date = fields.DateField(null=True)
    genres = fields.ManyToManyField(
        'models.Genre', through='book_genre', related_name='books')

    async def get_genres(self):
        book_genres = await BookGenre.filter(book_id=self.id).prefetch_related('genre')
        return [bg.genre for bg in book_genres]

    class Meta:
        table = "Book"


class Genre(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)

    class Meta:
        table = "Genre"


class BookGenre(Model):
    id = fields.IntField(primary_key=True)
    book = fields.ForeignKeyField('models.Book', related_name='book_genres')
    genre = fields.ForeignKeyField('models.Genre', related_name='book_genres')

    class Meta:
        table = "BookGenre"


class Reader(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255)
    phone = fields.CharField(max_length=255)
    address = fields.TextField()

    class Meta:
        table = "Reader"


class LibraryCard(Model):
    id = fields.IntField(primary_key=True)
    reader = fields.OneToOneField('models.Reader', related_name='library_card')

    class Meta:
        table = "LibraryCard"
