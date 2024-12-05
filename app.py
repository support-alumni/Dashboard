import csv
from flask import Flask, redirect, url_for, request, session, jsonify
import requests
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for the app
app.secret_key = 'WPL_AP1.HOjCrpkLrg9FRGli.f8dw+g=='  # Your secret key

# LinkedIn API credentials
CLIENT_ID = '86sj54i09odtrh'
CLIENT_SECRET = 'WPL_AP1.HOjCrpkLrg9FRGli.f8dw+g=='
REDIRECT_URI = 'http://localhost:5000/linkedin/callback'

# LinkedIn API endpoints
AUTH_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
PROFILE_URL = 'https://api.linkedin.com/v2/me'
EMAIL_URL = 'https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))'

# Path to the fake alumni CSV file
ALUMNI_CSV_FILE = r'C:\Users\mahta\Desktop\AlumniSearchApp\csv.txt'  # Fixed indentation


def read_alumni_csv():
    """Read alumni data from the CSV file."""
    alumni_data = []
    try:
        with open(ALUMNI_CSV_FILE, mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['graduation_year'] = int(row['graduation_year'])  # Convert graduation_year to int
                alumni_data.append(row)
        print("Raw alumni data:", alumni_data)  # Debugging: Print the data read
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return alumni_data


@app.route('/')
def home():
    """Home route for testing API functionality."""
    return jsonify({"message": "Welcome! Use /login for LinkedIn or /api/alumni for alumni data."})


# ----------------- LinkedIn OAuth Routes -----------------
@app.route('/login', methods=['GET'])
def login():
    """Redirect to LinkedIn's OAuth login page."""
    state = 'random_unique_state'  # In production, generate a secure random state
    auth_url = (
        f'{AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}'
        f'&scope=r_emailaddress%20r_liteprofile&state={state}'
    )
    return redirect(auth_url)


@app.route('/linkedin/callback', methods=['GET'])
def linkedin_callback():
    """Handle LinkedIn's OAuth callback and exchange the authorization code for an access token."""
    code = request.args.get('code')
    if not code:
        return jsonify({"error": "No authorization code returned"}), 400

    # Exchange the authorization code for an access token
    token_response = requests.post(
        TOKEN_URL,
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    if token_response.status_code != 200:
        return jsonify({"error": "Error fetching token", "details": token_response.json()}), token_response.status_code

    token_json = token_response.json()
    access_token = token_json.get('access_token')
    session['linkedin_access_token'] = access_token
    return redirect(url_for('validate_email'))


@app.route('/validate_email', methods=['GET'])
def validate_email():
    """Validate the LinkedIn email domain to check if it's a UNT email."""
    access_token = session.get('linkedin_access_token')
    if not access_token:
        return jsonify({"error": "No access token found"}), 403

    headers = {'Authorization': f'Bearer {access_token}'}
    email_response = requests.get(EMAIL_URL, headers=headers)
    if email_response.status_code != 200:
        return jsonify({"error": "Error fetching email", "details": email_response.json()}), email_response.status_code

    email_data = email_response.json()
    email = email_data.get('elements', [])[0].get('handle~', {}).get('emailAddress')

    if not email or not email.endswith('@unt.edu'):
        return jsonify({"error": f"Access denied: {email} is not a UNT email address."}), 403

    return jsonify({"message": "Email validated successfully", "email": email}), 200


# ----------------- Alumni API Routes -----------------
@app.route('/api/alumni', methods=['GET'])
def get_alumni():
    """Fetch alumni data from the CSV file, filter for UNT graduates from 2003 onwards."""
    alumni_data = read_alumni_csv()

    # Debug: Print filtered alumni
    filtered_alumni = [
        {
            "name": alum["name"],
            "major": alum["major"],
            "position": alum["position"],
            "email": alum["email"],
            "graduation_year": alum["graduation_year"]
        }
        for alum in alumni_data
        if alum["graduation_year"] >= 2003 and alum["university"].lower() == "unt"
    ]
    print("Filtered alumni data:", filtered_alumni)  # Debug: Print filtered data
    return jsonify(filtered_alumni), 200


@app.route('/api/alumni/search', methods=['GET'])
def search_alumni():
    """Search alumni data based on major or position."""
    major = request.args.get('major', '').lower()
    position = request.args.get('position', '').lower()
    alumni_data = read_alumni_csv()

    # Debug: Print searched alumni
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
           (position in alum["position"].lower() or not position) and
           alum["graduation_year"] >= 2003 and alum["university"].lower() == "unt"
    ]
    print("Searched alumni data:", searched_alumni)  # Debug: Print searched data
    return jsonify(searched_alumni), 200


@app.route('/api/ping', methods=['GET'])
def ping():
    """Health check endpoint to confirm the API is running."""
    return jsonify({"message": "API is running!"}), 200


if __name__ == '__main__':
    app.run(debug=True)
