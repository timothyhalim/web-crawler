from Model import db, Author, Genre, Status, Book, Chapter, BookAuthor, BookGenre
import traceback


def init():
    db.connect()
    db.create_tables([Author, Genre, Status, Book, Chapter, BookAuthor, BookGenre])
    return db

def create_author(name):
    author, new = Author.get_or_create(name=name)
    return author

def create_genre(name):
    genre, new = Genre.get_or_create(name=name)
    return genre

def create_status(name):
    status, new = Status.get_or_create(name=name)
    return status

def create_book(title, authors=[], genres=[], summary="", status=""):
    if isinstance(status, str):
        status = create_status(status)
    book, new = Book.get_or_create(title=title, summary="", status=status)

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

    book_authors = [BookAuthor.get_or_create(book=book, author=author) for author in authors]
    book_genres = [BookGenre.get_or_create(book=book, genre=genre) for genre in genres]

    return book

def create_chapter(book, title, content="", is_published=False):
    chapter = Chapter.create(book=book, title=title, content=content, is_published=is_published)
    return chapter
