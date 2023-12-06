from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import sqlite3
import subprocess
import sys
import os

app = Flask(__name__)

DATABASE_FILE = 'patients_data.db'

# Establishes a connection to the SQLite database.
def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # This allows for dictionary-like access to the database rows.
    return conn

@app.before_first_request
def initialize_database():
    init_db()

# Initializes the database with the necessary tables if they do not already exist.
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

# A test endpoint to check if the server is running.
@app.route('/test_connection', methods=['GET'])
def test_connection():
    return jsonify({"message": "Server is running and connection is successful"}), 200

# Endpoint to retrieve exercise data for a specific patient by ID.
@app.route('/get_exercise_data/<int:patient_id>', methods=['GET'])
def get_exercise_data(patient_id):
    db = get_db_connection()
    cursor = db.cursor()
    # Query to select all exercise data for a given patient ID, ordered by date.
    cursor.execute(
        'SELECT * FROM exercise_data WHERE patient_id = ? ORDER BY date DESC',
        (patient_id,)
    )
    exercises = cursor.fetchall()
    db.close()

    # Convert database rows to a list of dictionaries.
    exercises_data = []
    if exercises:
        for exercise in exercises:
            exercises_data.append({
                "patient_id": exercise['patient_id'],
                "date": exercise['date'],
                "repetitions": exercise['repetitions']
            })

    return jsonify(exercises_data), 200


@app.route('/start_exercise', methods=['POST'])
def start_exercise():
    data = request.get_json()
    print("Received data from Unity:", data)
    patient_id = data.get('patient_id')
    date = data.get('date')
    exercise_time = data.get('time')

    if exercise_time is None:
        print("No exercise time provided")
        return jsonify({"status": "error", "message": "No exercise time provided"}), 400

    print("Exercise time received:", exercise_time)

    script_path = os.path.join(os.path.dirname(__file__), 'Test.py')

    result = subprocess.run(
        [sys.executable, script_path, '--time', str(exercise_time)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    if result.stderr and not "terminating async callback" in result.stderr:
        print("Error in script execution:", result.stderr)
        return jsonify({"status": "error", "message": "Error in script execution"}), 500

    try:
        # Assuming the repetition count is always the last line
        reps_count = int(result.stdout.strip().split('\n')[-1])
    except ValueError:
        print("Invalid output from script")
        return jsonify({"status": "error", "message": "Invalid output from script"}), 500

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO exercise_data (patient_id, date, repetitions) VALUES (?, ?, ?)',
        (patient_id, date, reps_count)
    )
    db.commit()
    db.close()

    return jsonify({"status": "success", "message": "Exercise started", "repetitions": reps_count}), 200




# Endpoint to save exercise data sent via a POST request.
@app.route('/save_data/', methods=['POST'])
def save_data():
    data = request.get_json()
    # If data is not provided or is incomplete, return an error.
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    # Extract information from the JSON data.
    patient_id = data.get('patient_id')
    date = data.get('date', datetime.now().strftime("%Y-%m-%d %H:%M"))  # Assign current datetime if 'date' is missing.
    repetitions = data.get('repetitions')

    # Insert the extracted data into the exercise_data table.
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO exercise_data (patient_id, date, repetitions) VALUES (?, ?, ?)',
        (patient_id, date, repetitions)
    )
    db.commit()
    db.close()

    return jsonify({"status": "success", "message": "Data saved successfully"}), 200

# Endpoint to delete all exercise data.
@app.route('/delete_all_dates', methods=['POST'])
def delete_all_dates():
    conn = sqlite3.connect('patients_data.db')
    cursor = conn.cursor()
    # Execute delete operation on both tables.
    cursor.execute("DELETE FROM patients")
    cursor.execute("DELETE FROM exercise_data")
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "All data deleted"}), 200

# Endpoint to delete the latest exercise data entry.
@app.route('/delete_latest_date', methods=['POST'])
def delete_latest_date():
    conn = sqlite3.connect('patients_data.db')
    cursor = conn.cursor()
    # Delete the most recent entry from exercise_data table.
    cursor.execute("DELETE FROM exercise_data WHERE date = (SELECT MAX(date) FROM exercise_data)")
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Latest data entry deleted"}), 200

# Run the Flask application.
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
