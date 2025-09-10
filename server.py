from flask import Flask, request, jsonify, render_template
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Get database URL from environment variable
DATABASE_URL = "postgresql://dreamdb_0k4i_user:Ea7UwZIMa89NVGgHZ5ailN6g9qOM4aJm@dpg-d30sggemcj7s73d8mf0g-a/dreamdb_0k4i" # Render provides this for your PostgreSQL database

# Initialize PostgreSQL database
def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS dreams (
            id SERIAL PRIMARY KEY,
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

    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    c.execute('INSERT INTO dreams (name, description, date) VALUES (%s, %s, %s) RETURNING id',
              (name, description, date))
    dream_id = c.fetchone()[0]
    conn.commit()
    conn.close()

    return jsonify({"success": True, "id": dream_id})

# Get all dreams
@app.route('/dreams')
def get_dreams():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    c = conn.cursor()
    c.execute('SELECT id, name, description, date FROM dreams ORDER BY date DESC')
    dreams = c.fetchall()
    conn.close()
    return jsonify(dreams)

# Update a dream
@app.route('/update-dream/<int:dream_id>', methods=['PUT'])
def update_dream(dream_id):
    data = request.json
    name = data.get('name')
    description = data.get('description')
    date = data.get('date')

    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    c.execute('UPDATE dreams SET name=%s, description=%s, date=%s WHERE id=%s',
              (name, description, date, dream_id))
    conn.commit()
    conn.close()

    return jsonify({"success": True})

# Delete a dream
@app.route('/delete-dream/<int:dream_id>', methods=['DELETE'])
def delete_dream(dream_id):
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    c.execute('DELETE FROM dreams WHERE id=%s', (dream_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# Run locally or on Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT
    app.run(host="0.0.0.0", port=port)
