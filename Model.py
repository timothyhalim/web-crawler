import os
from peewee import *
import datetime

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
    title = CharField(unique=True)
    summary = TextField()
    status = ForeignKeyField(Status, backref='statuses')

class Chapter(BaseModel):
    book = ForeignKeyField(Book, backref='chapters')
    title = CharField()
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