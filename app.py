from flask import Flask, render_template, request, jsonify
import os
from storage import load_library, get_book, save_library

app = Flask(__name__)

@app.route('/')
def library_view():
    library = load_library()
    return render_template('library.html', books=library['books'])

@app.route('/book/<book_id>')
def book_view(book_id):
    book = get_book(book_id)
    if not book:
        return "Book not found", 404
    return render_template('book.html', book=book)

@app.route('/api/progress', methods=['POST'])
def update_progress():
    data = request.json
    book_id = data.get('book_id')
    chapter_id = data.get('chapter_id')
    completed = data.get('completed', False)
    
    # Optional: track specific section progress if needed
    # section_index = data.get('section_index') 

    if not book_id or not chapter_id:
        return jsonify({"status": "error", "message": "Missing book_id or chapter_id"}), 400

    library = load_library()
    book_found = False
    
    for book in library['books']:
        if book['id'] == book_id:
            book_found = True
            chapter_found = False
            for chapter in book['chapters']:
                if chapter['id'] == chapter_id:
                    chapter_found = True
                    chapter['completed'] = completed
                    # We could also track timestamp progress here
                    break
            
            if not chapter_found:
                return jsonify({"status": "error", "message": "Chapter not found"}), 404
            
            # Recalculate total book progress
            total_chapters = len(book['chapters'])
            completed_chapters = sum(1 for c in book['chapters'] if c.get('completed'))
            book['total_progress'] = (completed_chapters / total_chapters) * 100 if total_chapters > 0 else 0
            break
    
    if not book_found:
from flask import Flask, render_template, request, jsonify
import os # Added import for os module
from storage import load_library, get_book, save_library

app = Flask(__name__)

@app.route('/')
def library_view():
    library = load_library()
    return render_template('library.html', books=library['books'])

@app.route('/book/<book_id>')
def book_view(book_id):
    book = get_book(book_id)
    if not book:
        return "Book not found", 404
    return render_template('book.html', book=book)

@app.route('/api/progress', methods=['POST'])
def update_progress():
    data = request.json
    book_id = data.get('book_id')
    chapter_id = data.get('chapter_id')
    completed = data.get('completed', False)
    
    # Optional: track specific section progress if needed
    # section_index = data.get('section_index') 

    if not book_id or not chapter_id:
        return jsonify({"status": "error", "message": "Missing book_id or chapter_id"}), 400

    library = load_library()
    book_found = False
    
    for book in library['books']:
        if book['id'] == book_id:
            book_found = True
            chapter_found = False
            for chapter in book['chapters']:
                if chapter['id'] == chapter_id:
                    chapter_found = True
                    chapter['completed'] = completed
                    # We could also track timestamp progress here
                    break
            
            if not chapter_found:
                return jsonify({"status": "error", "message": "Chapter not found"}), 404
            
            # Recalculate total book progress
            total_chapters = len(book['chapters'])
            completed_chapters = sum(1 for c in book['chapters'] if c.get('completed'))
            book['total_progress'] = (completed_chapters / total_chapters) * 100 if total_chapters > 0 else 0
            break
    
    if not book_found:
        return jsonify({"status": "error", "message": "Book not found"}), 404

    save_library(library)
    return jsonify({"status": "success", "progress": book.get('total_progress', 0)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True) # Running on 5001 to avoid conflict with calc app
