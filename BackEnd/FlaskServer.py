from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE_FILE = 'patients_data.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

def init_db():
    with app.app_context():
        db = get_db_connection()
        cursor = db.cursor()
        # Create table for patients
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        ''')
        # Create table for exercise data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exercise_data (
                patient_id INTEGER,
                date TEXT,
                repetitions INTEGER,
                FOREIGN KEY(patient_id) REFERENCES patients(id)
            )
        ''')
        db.commit()

@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    patient_id = data.get('patient_id')
    date = data.get('date')
    repetitions = data.get('repetitions')

    if patient_id is None or date is None or repetitions is None:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    # Insert data into the database
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO exercise_data (patient_id, date, repetitions) VALUES (?, ?, ?)',
        (patient_id, date, repetitions)
    )
    db.commit()
    db.close()

    return jsonify({"status": "success", "message": "Data saved successfully"}), 200

# Initialize the database
init_db()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

@app.route('/delete_all_dates', methods=['POST'])
def delete_all_dates():
    conn = sqlite3.connect('patients_data.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patient_data")  # This will delete all records
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "All dates deleted"}), 200

@app.route('/delete_latest_date', methods=['POST'])
def delete_latest_date():
    conn = sqlite3.connect('patients_data.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patient_data WHERE date = (SELECT MAX(date) FROM patient_data)")
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Latest date deleted"}), 200
