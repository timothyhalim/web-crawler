from Model import db, Author, Genre, Status, Book, Chapter


def init():
    db.connect()
    db.create_tables([Book, Chapter])
    return db

def create_author(name):
    author = Author.create(name=name)
    return author

def create_book(title, author):
    book = Book.create(title='charlie')
    return book