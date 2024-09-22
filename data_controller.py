from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from data_models import Author, Book,Base
import random



class DataController:
    def __init__(self):
        self.__engine = create_engine('sqlite:///author_books.sqlite3', echo=False)
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine)
        self.__session = session()

    @property
    def session(self):
        return self.__session;

    def close(self):
        self.__session.close()

    def get_random_author_id(self):
        author_ids = self.__session.query(Author.id).all()
        if author_ids:
            return random.choice(author_ids)[0]
        return None


class DataWriter(DataController):
    def insert_author(self, author):
        self.session.add(author)
        self.session.commit()

    def insert_book(self, book):
        self.session.add(book)
        self.session.commit()

    def clear_data(self):
        self.session.query(Book).delete()
        self.session.query(Author).delete()
        self.session.commit()


class DataAnalyzer(DataController):
    def print_book_with_most_pages(self):
        book = self.session.query(Book).order_by(Book.number_of_pages.desc()).first()
        print(f"Book with the most pages: {book.name} by {book.author.first_name} {book.author.last_name} ({book.number_of_pages} pages)")

    def print_average_number_of_pages(self):
        avg_pages = self.session.query(Book).with_entities(func.avg(Book.number_of_pages)).scalar()
        print(f"Average number of pages: {avg_pages:.2f}")

    def print_youngest_author(self):
        author = self.session.query(Author).order_by(Author.birth_date.desc()).first()
        print(f"Youngest author: {author.first_name} {author.last_name}")

    def print_authors_without_books(self):
        authors = self.session.query(Author).outerjoin(Book).filter(Book.author_id.is_(None)).all()
        print("Authors without books:")
        for author in authors:
            print(f"{author.first_name} {author.last_name}")

    def print_authors_with_more_than_3_books(self):
        authors = self.session.query(Author).join(Book).group_by(Author.id).having(func.count(Book.id) > 3).all()
        print("Authors with more than 3 books:")
        for author in authors:
            print(f"{author.first_name} {author.last_name}")
