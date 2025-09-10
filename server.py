from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('dreams.db')
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

# API: Submit a dream
@app.route('/submit-dream', methods=['POST'])
def submit_dream():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    date = data.get('date')

    conn = sqlite3.connect('dreams.db')
    c = conn.cursor()
    c.execute('INSERT INTO dreams (name, description, date) VALUES (?, ?, ?)',
              (name, description, date))
    conn.commit()
    dream_id = c.lastrowid
    conn.close()

    return jsonify({"success": True, "id": dream_id})

# API: Get all dreams
@app.route('/dreams')
def get_dreams():
    conn = sqlite3.connect('dreams.db')
    c = conn.cursor()
    c.execute('SELECT id, name, description, date FROM dreams ORDER BY date DESC')
    dreams = [{"id": row[0], "name": row[1], "description": row[2], "date": row[3]} for row in c.fetchall()]
    conn.close()
    return jsonify(dreams)

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use PORT from environment, default to 5000
    app.run(host='0.0.0.0', port=port)

