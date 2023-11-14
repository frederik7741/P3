from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
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
@app.route('/test_connection', methods=['GET'])
def test_connection():
    return jsonify({"message": "Server is running and connection is successful"}), 200

@app.route('/get_exercise_data/<int:patient_id>', methods=['GET'])
def get_exercise_data(patient_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        'SELECT * FROM exercise_data WHERE patient_id = ? ORDER BY date DESC',
        (patient_id,)
    )
    exercises = cursor.fetchall()
    db.close()

    # Convert the rows into a list of dicts
    exercises_data = []
    if exercises:
        for exercise in exercises:
            exercises_data.append({
                "date": exercise['date'],
                "repetitions": exercise['repetitions']
            })

    return jsonify(exercises_data), 200


@app.route('/save_data/', methods=['POST'])
def save_data():
    print(f"Received POST request at {request.path}")  # Log the request path
    print(f"Request data: {request.data}")  # Log the raw request data
    data = request.get_json()
    if not data:
        print("No data provided")  # Add this line for debugging
        return jsonify({"status": "error", "message": "No data provided"}), 400

    patient_id = data.get('patient_id')
    date = data.get('date', None)  # Assign a default value of None if 'date' is missing
    repetitions = data.get('repetitions')

    if patient_id is None or repetitions is None:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    # If 'date' is None, assign a default date value here
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d %H:%M")

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
    cursor.execute("DELETE FROM patients")  # Update table name to "patients"
    cursor.execute("DELETE FROM exercise_data")  # Update table name to "exercise_data"
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "All dates deleted"}), 200

@app.route('/delete_latest_date', methods=['POST'])
def delete_latest_date():
    conn = sqlite3.connect('patients_data.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM exercise_data WHERE date = (SELECT MAX(date) FROM exercise_data)")  # Update table name to "exercise_data"
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Latest date deleted"}), 200
