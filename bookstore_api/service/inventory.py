import json
from config import DATA_PATH

def load_books():
    with open(DATA_PATH + "books.json", "r") as f:
        return json.load(f)

def save_books(books):
    with open(DATA_PATH + "books.json", "w") as f:
        json.dump(books, f, indent=4)

def get_book(book_id):
    books = load_books()
    return books.get(book_id)

def update_stock(book_id, quantity):
    books = load_books()
    if book_id in books:
        books[book_id]["stock"] -= quantity
        save_books(books)
        return books[book_id]
    return None
def add_book(book_id, book_data):
    books = load_books()
    books[book_id] = book_data
    save_books(books)
    return books[book_id]
def delete_book(book_id):
    books = load_books()
    if book_id in books:
        del books[book_id]
        save_books(books)
        return True
    return False
