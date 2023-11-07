from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/save_data', methods=['POST'])
def save_data():
    print(request.data)  # This will print the raw data received
    print(request.json)  # This will show the parsed JSON, if any

    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    patient_id = data.get('patient_id')
    date = data.get('date')
    repetitions = data.get('repetitions')

    if patient_id is None or date is None or repetitions is None:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    # Proceed with database insertion here...

    return jsonify({"status": "success", "message": "Data saved successfully"}), 200

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
