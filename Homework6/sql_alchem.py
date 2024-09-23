from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from faker import Faker
import random

fake = Faker()
Base = declarative_base()

class Author(Base):
    __tablename__ = 'authors'
    
    author_id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String, nullable=False) 
    lastname = Column(String, nullable=False)
    birthdate = Column(Date, nullable=False)
    birthplace = Column(String, nullable=False)
    
    books = relationship('Book', back_populates='author')

class Book(Base):
    __tablename__ = 'books'
    
    book_id = Column(Integer, primary_key=True, autoincrement=True)
    book_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    pages = Column(Integer, nullable=False)
    public_date = Column(Date, nullable=False)
    
    author_id = Column(Integer, ForeignKey('authors.author_id'), nullable=False)
    author = relationship('Author', back_populates='books')

# Create the SQLite database
engine = create_engine('sqlite:///book_authors.db', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def generate_authors():
    authors = []
    for i in range(500):
        author = Author(
            firstname=fake.first_name(),
            lastname=fake.last_name(),
            birthdate=fake.date_of_birth(minimum_age=18, maximum_age=100),
            birthplace=fake.city()
        )
        authors.append(author)
    return authors

def generate_books():
    books = []
    categories = ['Comedy', 'Romance', 'Science', 'Fiction', 'Fantasy', 'History', 'Horror', 'Biography']
    for i in range(1000):
        book = Book(
            book_name=fake.sentence(nb_words=2),
            category=random.choice(categories),
            pages=random.randint(100, 1500),
            public_date=fake.date_of_birth(minimum_age=18, maximum_age=100),
            author_id=random.randint(1, 500)  # Assigning a random author ID
        )
        books.append(book)   
    return books

# Generate and add authors to the session
authors = generate_authors()
session.add_all(authors)
session.commit()

# Generate and add books to the session
books = generate_books()
session.add_all(books)
session.commit()

# Query the book with the most pages
most_pages_book = session.query(Book).order_by(Book.pages.desc()).first()
print(f"Book with the most pages: {most_pages_book.book_name}, Pages: {most_pages_book.pages}")

# Calculate average number of pages
average_pages = session.query(func.avg(Book.pages)).scalar()
print(f"Average number of pages: {round(average_pages)}")

# Query the youngest author
youngest_author = session.query(Author).order_by(Author.birthdate.desc()).first()
print(f"Youngest author: {youngest_author.firstname} {youngest_author.lastname}, Birthdate: {youngest_author.birthdate}")

# Query authors without books
authors_without_books = session.query(Author).outerjoin(Book).filter(Book.book_id == None).all()
print(f"Authors without books: {[author.firstname + ' ' + author.lastname for author in authors_without_books]}")

# Close the session
session.close()
