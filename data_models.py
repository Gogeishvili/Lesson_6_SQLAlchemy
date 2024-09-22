from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    birth_place = Column(String, nullable=False)

    books = relationship("Book", back_populates="author")

    def __init__(self, first_name, last_name, birth_date, birth_place):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.birth_place = birth_place


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    category_name = Column(String, nullable=False)
    number_of_pages = Column(Integer, nullable=False)
    date_of_issue = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)

    author = relationship("Author", back_populates="books")

    def __init__(self, name, category_name, number_of_pages, date_of_issue, author_id):
        self.name = name
        self.category_name = category_name
        self.number_of_pages = number_of_pages
        self.date_of_issue = date_of_issue
        self.author_id = author_id
