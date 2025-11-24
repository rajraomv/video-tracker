import json
import os

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'library.json')

def load_library():
    print(f"DEBUG: Loading library from {DATA_FILE}")
    if not os.path.exists(DATA_FILE):
        return {'books': []}
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {'books': []}

def save_library(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def get_book(book_id):
    library = load_library()
    for book in library['books']:
        if book['id'] == book_id:
            return book
    return None
