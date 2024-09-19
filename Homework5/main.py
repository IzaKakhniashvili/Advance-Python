import sqlite3
from faker import Faker
import random

fake = Faker()

conn = sqlite3.connect('book_authors.db')

cursor = conn.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS authors(
        author_id INTEGER PRIMARY KEY AUTOINCREMENT,
        author_name TEXT NOT NULL,
        lastname DATE NOT NULL,
        birthdate DATE NOT NULL,
        birthplace TEXT NOT NULL        
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS books(
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_name TEXT NOT NULL,
        category TEXT NOT NULL,
        pages INTEGER NOT NULL,
        public_date INTEGER NOT NULL,
        author_id INTEGER NOT NULL,
        FOREIGN KEY(author_id) REFERENCES authora(author_id)
    )
""")

def generate_authors():
    authors = []
    for i in range(500):
        author_name = fake.first_name()
        lastname = fake.last_name()
        birthdate = fake.date_of_birth(minimum_age=18, maximum_age=100).isoformat()
        birthplace = fake.city()
        authors.append((author_name, lastname, birthdate, birthplace))
    return authors

def generate_books():
    books = []
    categories = ['Comedy', 'Romance', 'Science', 'Fiction', 'Fantasy', 'History', 'Horror', 'Biography']
    for i in range(1000):
        book_name = fake.sentence(nb_words=2)
        category = random.choice(categories)
        pages = random.randint(100, 1500)
        public_date = fake.date_of_birth(minimum_age=18, maximum_age=100).isoformat()
        author_id = random.randint(0, 500)
        books.append((book_name, category, pages, public_date, author_id))   
    return books

authors  = generate_authors()
books = generate_books()

cursor.executemany("""
        INSERT INTO authors (author_name, lastname, birthdate, birthplace)
        VALUES (?, ?, ?, ?)
    """, authors)     

cursor.executemany("""
        INSERT INTO books (book_name, category, pages, public_date, author_id)
        VALUES (?, ?, ?, ?, ?)
    """, books)     



#ყველაზე მეტი გვერდების მქონე წიგნის ყველა ველი
cursor.execute("""
    SELECT * 
    FROM books
    ORDER BY pages DESC
    LIMIT 1;
""")

#წიგნების გვერდების საშუალო რაოდენობა
cursor.execute("""
    SELECT avg(pages) as average_pages
    FROM books;
""")

#ყველაზე ახალგაზრდა ავტორი
cursor.execute("""
    SELECT * 
    FROM authors
    ORDER BY birthdate DESC
    LIMIT 1;
""")

#ისეთი ავტორები, რომლებსაც ჯერ წიგნი არ აქვთ
cursor.execute("""
SELECT a.*
FROM authors a
LEFT JOIN books b ON a.author_id = b.author_id
WHERE b.author_id IS NULL;
""")

conn.commit()

conn.close()

print("Data has been successfully inserted into the database.")