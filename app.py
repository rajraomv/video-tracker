from flask import Flask, render_template, request, jsonify
import os
from storage import load_library, get_book, save_library
from manage import add_book_logic, refresh_book_logic, delete_book_logic

app = Flask(__name__)

@app.route('/')
def library_view():
    library = load_library()
    return render_template('library.html', books=library['books'])

@app.route('/admin')
def admin_view():
    library = load_library()
    return render_template('admin.html', books=library['books'])

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

@app.route('/api/admin/add_book', methods=['POST'])
def api_add_book():
    data = request.json
    url = data.get('url')
    # Use a default title or fetch it if not provided (simplified for now)
    # In a real scenario, we might want to fetch the title from YouTube first or ask the user.
    # For this quick implementation, we'll try to fetch the title from the playlist info if not provided,
    # but add_book_logic expects a title. Let's assume the user might want to edit it later or we just use "New Book".
    # Actually, let's just use the playlist title if we can, or ask the user in the UI.
    # The UI doesn't have a title input yet, let's default to "New Playlist" or update UI.
    # Wait, the UI *does* need a title input. I'll update the UI in a sec.
    # For now, let's pass a placeholder.
    title = "New Playlist" 
    
    # BETTER APPROACH: Let's fetch the title inside logic if not provided? 
    # Or just update add_book_logic to be smarter.
    # For now, let's just pass the URL and let logic handle it? 
    # logic takes (url, title).
    
    # Let's update the UI to ask for title, or just use a default.
    result = add_book_logic(url, title) 
    return jsonify(result)

@app.route('/api/admin/refresh_book', methods=['POST'])
def api_refresh_book():
    data = request.json
    book_id = data.get('book_id')
    result = refresh_book_logic(book_id)
    return jsonify(result)

@app.route('/api/admin/delete_book', methods=['POST'])
def api_delete_book():
    data = request.json
    book_id = data.get('book_id')
    result = delete_book_logic(book_id)
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
