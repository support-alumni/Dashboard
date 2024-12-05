
from flask import Blueprint, jsonify, request
import requests
from flask_cors import CORS

#I used blueprint to have difffrent section
# Initialize Blueprint for alumni-related APIs
alumni_api = Blueprint('alumni_api', __name__)
CORS(alumni_api)  # Enable CORS for this blueprint

# External API details
ALUMNI_API_URL = "https://api.alumni.com/alumni"  # It needs to be replaced with actual API
API_KEY = "your_api_key_here"  # Replace with the actual API key or token

@alumni_api.route('/api/alumni', methods=['GET'])
def get_alumni():
    """
    Fetch alumni data from an external API, filter for UNT graduates from 2003 onwards,
    and return the data.
    """
    # Query the external API
    response = requests.get(
        ALUMNI_API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"}
    )

    # Handle API errors
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch alumni data from external API"}), response.status_code

    # Parse the API response
    alumni_data = response.json()

    # Filter alumni data for UNT graduates from 2003 onwards
    filtered_alumni = [
        {
            "name": alum.get("name"),
            "major": alum.get("major"),
            "position": alum.get("position"),
            "email": alum.get("email"),
            "graduation_year": alum.get("graduation_year")
        }
        for alum in alumni_data
        if alum.get("graduation_year", 0) >= 2003 and alum.get("university") == "UNT"
    ]

    return jsonify(filtered_alumni), 200


@alumni_api.route('/api/alumni/search', methods=['GET'])
def search_alumni():
    """
    Search alumni data based on major or position.
    """
    major = request.args.get('major', '').lower()
    position = request.args.get('position', '').lower()

    # Query the external API
    response = requests.get(
        ALUMNI_API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"}
    )

    # Handle API errors
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch alumni data from external API"}), response.status_code

    # Parse the API response
    alumni_data = response.json()

    # Filter alumni data based on search criteria
    searched_alumni = [
        {
            "name": alum.get("name"),
            "major": alum.get("major"),
            "position": alum.get("position"),
            "email": alum.get("email"),
            "graduation_year": alum.get("graduation_year")
        }
        for alum in alumni_data
        if (major in alum.get("major", "").lower() or not major) and
           (position in alum.get("position", "").lower() or not position)
           and alum.get("graduation_year", 0) >= 2003 and alum.get("university") == "UNT"
    ]

    return jsonify(searched_alumni), 200


@alumni_api.route('/api/ping', methods=['GET'])
def ping():
    """
    Health check endpoint to confirm the alumni API is running.
    """
    return jsonify({"message": "Alumni API is running!"}), 200
