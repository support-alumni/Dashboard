import csv
from flask import Blueprint, jsonify, request
from flask_cors import CORS

# Initialize Blueprint for alumni-related APIs
alumni_api = Blueprint('alumni_api', __name__)
CORS(alumni_api)  # Enable CORS for this blueprint

# Path to the fake alumni CSV file
ALUMNI_CSV_FILE = 'alumni.csv'


def read_alumni_csv():
    """Read alumni data from the CSV file."""
    alumni_data = []
    try:
        with open(ALUMNI_CSV_FILE, mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert graduation_year to int for filtering
                row['graduation_year'] = int(row['graduation_year'])
                alumni_data.append(row)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return alumni_data


@alumni_api.route('/api/alumni', methods=['GET'])
def get_alumni():
    """
    Fetch alumni data from the CSV file, filter for UNT graduates from 2003 onwards,
    and return the data.
    """
    alumni_data = read_alumni_csv()

    # Filter alumni data for UNT graduates from 2003 onwards
    filtered_alumni = [
        {
            "name": alum["name"],
            "major": alum["major"],
            "position": alum["position"],
            "email": alum["email"],
            "graduation_year": alum["graduation_year"]
        }
        for alum in alumni_data
        if alum["graduation_year"] >= 2003 and alum["university"] == "UNT"
    ]

    return jsonify(filtered_alumni), 200


@alumni_api.route('/api/alumni/search', methods=['GET'])
def search_alumni():
    """
    Search alumni data based on major or position.
    """
    major = request.args.get('major', '').lower()
    position = request.args.get('position', '').lower()

    alumni_data = read_alumni_csv()

    # Filter alumni data based on search criteria
    searched_alumni = [
        {
            "name": alum["name"],
            "major": alum["major"],
            "position": alum["position"],
            "email": alum["email"],
            "graduation_year": alum["graduation_year"]
        }
        for alum in alumni_data
        if (major in alum["major"].lower() or not major) and
           (position in alum["position"].lower() or not position)
           and alum["graduation_year"] >= 2003 and alum["university"] == "UNT"
    ]

    return jsonify(searched_alumni), 200


@alumni_api.route('/api/ping', methods=['GET'])
def ping():
    """
    Health check endpoint to confirm the alumni API is running.
    """
    return jsonify({"message": "Alumni API is running!"}), 200
