from peewee import *
import datetime

db_path = "Novel.db"
db = SqliteDatabase(db_path)

class BaseModel(Model):
    class Meta:
        database = db

class Author(BaseModel):
    name = CharField(unique=True)

class Genre(BaseModel):
    name = CharField(unique=True)

class Status(BaseModel):
    name = CharField(unique=True)

class Book(BaseModel):
    title = CharField(unique=True)
    authors = ForeignKeyField(Author, backref='authors')
    genres = ForeignKeyField(Author, backref='genres')
    summary = TextField()
    status = ForeignKeyField(Status, backref='statuses')

class Chapter(BaseModel):
    book = ForeignKeyField(Book, backref='chapters')
    content = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
    is_published = BooleanField(default=True)

def init():
    db.connect()
    db.create_tables([Author, Genre, Status, Book, Chapter])
    return db

def create_author(name):
    author = Author.create(name=name)
    return author

def create_book(title, authors=[], genres=[], summary="", status=""):
    for author in authors:

    book = Book.create(title=title, authors=[], genres=[], summary="", status="")