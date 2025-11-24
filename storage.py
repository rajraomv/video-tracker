import json
import os
import database

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'library.json')

def load_library():
    # Check for MongoDB connection first
    if os.environ.get('MONGO_URI'):
        books = database.mongo_get_all_books()
        return {'books': books}

    print(f"DEBUG: Loading library from {DATA_FILE}")
    if not os.path.exists(DATA_FILE):
        return {'books': []}
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {'books': []}

def save_library(data):
    # Check for MongoDB connection first
    if os.environ.get('MONGO_URI'):
        return database.mongo_save_library(data)

    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def get_book(book_id):
    # Check for MongoDB connection first
    if os.environ.get('MONGO_URI'):
        return database.mongo_get_book(book_id)

    library = load_library()
    for book in library['books']:
        if book['id'] == book_id:
            return book
    return None

def delete_book(book_id):
    # Check for MongoDB connection first
    if os.environ.get('MONGO_URI'):
        return database.mongo_delete_book(book_id)

    library = load_library()
    original_count = len(library['books'])
    library['books'] = [b for b in library['books'] if b['id'] != book_id]
    
    if len(library['books']) < original_count:
        save_library(library)
        return True
    return False
