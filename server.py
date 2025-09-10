from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)

# Absolute path for database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'dreams.db')

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS dreams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Serve main page
@app.route('/')
def index():
    return render_template('index.html')

# Submit a dream
@app.route('/submit-dream', methods=['POST'])
def submit_dream():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    date = data.get('date')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO dreams (name, description, date) VALUES (?, ?, ?)',
              (name, description, date))
    conn.commit()
    dream_id = c.lastrowid
    conn.close()

    return jsonify({"success": True, "id": dream_id})

# Get all dreams
@app.route('/dreams')
def get_dreams():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, name, description, date FROM dreams ORDER BY date DESC')
    dreams = [{"id": row[0], "name": row[1], "description": row[2], "date": row[3]} for row in c.fetchall()]
    conn.close()
    return jsonify(dreams)

# Update a dream
@app.route('/update-dream/<int:dream_id>', methods=['PUT'])
def update_dream(dream_id):
    data = request.json
    name = data.get('name')
    description = data.get('description')
    date = data.get('date')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE dreams SET name=?, description=?, date=? WHERE id=?',
              (name, description, date, dream_id))
    conn.commit()
    conn.close()

    return jsonify({"success": True})

# Delete a dream
@app.route('/delete-dream/<int:dream_id>', methods=['DELETE'])
def delete_dream(dream_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM dreams WHERE id=?', (dream_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# Run locally or on Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT
    app.run(host="0.0.0.0", port=port)        # bind to all IPs
