import traceback
import datetime

from .Model import db, Author, Genre, Status, Book, Chapter, BookAuthor, BookGenre

def init():
    db.connect()
    db.create_tables([Author, Genre, Status, Book, Chapter, BookAuthor, BookGenre])
    return db

def create_authors(names):
    if isinstance(names, str):
        names = [names]
    return [Author.get_or_create(name=name)[0] for name in names]

def create_genres(names):
    if isinstance(names, str):
        names = [names]
    return [Genre.get_or_create(name=name)[0] for name in names]

def create_status(name):
    return Status.get_or_create(name=name)[0]

def create_book(title, fullurl, url, authors=[], genres=[], summary="", status="", release=datetime.datetime.now().strftime('%Y')):
    if isinstance(status, str):
        status = create_status(status)
    book = Book.get_or_create(title=title, fullurl=fullurl, url=url, summary=summary, release=release, status=status)
    authors = list(set(create_authors(authors)))
    genres = list(set(create_genres(genres)))

    for author in authors:
        BookAuthor.get_or_create(book=book[0], author=author)
    for genre in genres:
        BookGenre.get_or_create(book=book[0], genre=genre)

    return book[0]

def create_chapter(book, title, fullurl, url, content="", is_published=False):
    chapter = Chapter.create(book=book, title=title, fullurl=fullurl, url=url, content=content, is_published=is_published)
    return chapter
