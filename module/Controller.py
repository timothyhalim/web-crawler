import traceback
import datetime

from .Model import db, Author, Genre, Status, Book, Chapter, BookAuthor, BookGenre

def init():
    db.connect()
    db.create_tables([Author, Genre, Status, Book, Chapter, BookAuthor, BookGenre])
    return db

def create_author(names):
    if isinstance(names, str):
        names = [names]
    return [Author.get_or_create(name=name)[0] for name in names]

def create_genre(names):
    if isinstance(names, str):
        names = [names]
    return [Genre.get_or_create(name=name)[0] for name in names]

def create_status(names):
    if isinstance(names, str):
        names = [names]
    return [Status.get_or_create(name=name)[0] for name in names]

def create_book(title, authors=[], genres=[], summary="", status="", release=datetime.datetime.now().strftime('%Y')):
    if isinstance(status, str):
        status = create_status(status)
    book = Book.get_or_create(title=title, summary="", release=release, status=status)

    if isinstance(authors, str):
        authors = [create_author(authors)]
    elif isinstance(authors, list):
        authors_cleanup = []
        for author in authors:
            if isinstance(author, str):
                author = create_author(author)
                if not author in authors_cleanup:
                    authors_cleanup += [author]
            elif isinstance(author, Author):
                authors_cleanup += [author]
        authors = authors_cleanup
        
    if isinstance(genres, str):
        genres = [create_genre(genres)]
    elif isinstance(genres, list):
        genres_cleanup = []
        for genre in genres:
            if isinstance(genre, str):
                genre = create_genre(genre)
                if not genre in genres_cleanup:
                    genres_cleanup += [genre]
            elif isinstance(genre, Genre):
                genres_cleanup += [genre]
        genres = genres_cleanup

    for author in authors:
        BookAuthor.get_or_create(book=book[0], author=author)
    for genre in genres:
        BookGenre.get_or_create(book=book[0], genre=genre)

    return book

def create_chapter(book, title, content="", is_published=False):
    chapter = Chapter.create(book=book, title=title, content=content, is_published=is_published)
    return chapter
