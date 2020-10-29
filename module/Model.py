import os
from peewee import *
import datetime
from .DataProcess import DataProcess

db_path = os.path.join( __file__, "..", "Novel.db" )
db = SqliteDatabase(db_path)

class BaseModel(Model):
    class Meta:
        database = db

class Author(BaseModel):
    name = CharField(unique=True, constraints=[SQL('COLLATE NOCASE')])

class Genre(BaseModel):
    name = CharField(unique=True, constraints=[SQL('COLLATE NOCASE')])

class Status(BaseModel):
    name = CharField(unique=True, constraints=[SQL('COLLATE NOCASE')])

class Book(BaseModel):
    title = CharField()
    fullurl = CharField(unique=True)
    url = CharField()
    summary = TextField()
    release = CharField(unique=True)
    status = ForeignKeyField(Status)

    def chapters(self):
        chapters = [chapter for chapter in Chapter.select().where(Chapter.book == self.id)]
        chapters.sort(key= lambda k : DataProcess.natural_keys(k.url))
        return chapters

    def authors(self):
        authors = (BookAuthor.select().where(BookAuthor.book == self.id))
        return authors

    def genres(self):
        genres = (BookGenre.select().where(BookGenre.book == self.id))
        return genres

class Chapter(BaseModel):
    book = ForeignKeyField(Book)
    title = CharField()
    fullurl = CharField(unique=True)
    url = CharField()
    content = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
    is_published = BooleanField(default=True)

class BookAuthor(BaseModel):
    book = ForeignKeyField(Book)
    author = ForeignKeyField(Author)

    class Meta:
        primary_key = CompositeKey('book', 'author')

class BookGenre(BaseModel):
    book = ForeignKeyField(Book)
    genre = ForeignKeyField(Genre)

    class Meta:
        primary_key = CompositeKey('book', 'genre')