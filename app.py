from flask import Flask, request, jsonify, send_file
import pandas as pd
import os

app = Flask(__name__)

# Define the CSV file path
csv_file = 'data.csv'

# Check if the CSV file exists, if not create one with headers
if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=["Unique ID", "Name", "Longitude", "Latitude", "Floor"])
    df.to_csv(csv_file, index=False)

@app.route('/submit-data', methods=['POST'])
def submit_data():
    try:
        # Get the incoming JSON data from the Android app
        data = request.json
        
        # Extract the details
        unique_id = data.get("id")
        name = data.get("name")
        longitude = data.get("longitude")
        latitude = data.get("latitude")
        floor = data.get("floor")
        
        # Append the data to the CSV file
        new_data = pd.DataFrame([[unique_id, name, longitude, latitude, floor]], 
                                columns=["Unique ID", "Name", "Longitude", "Latitude", "Floor"])
        new_data.to_csv(csv_file, mode='a', header=False, index=False)
        
        # Return a success response
        return jsonify({"message": "Data received successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route to serve the CSV file
@app.route('/get-csv', methods=['GET'])
def get_csv():
    # Check if the file exists before serving
    if os.path.exists(csv_file):
        return send_file(csv_file, as_attachment=True, attachment_filename='data.csv')
    else:
        return jsonify({"error": "CSV file not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
