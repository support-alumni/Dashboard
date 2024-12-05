from flask import Flask, redirect, url_for, request, session, jsonify
import requests

# Initialize the Flask application
linkedin_app = Flask(__name__)
linkedin_app.secret_key = 'WPL_AP1.HOjCrpkLrg9FRGli.f8dw+g=='  # Your secret key

# LinkedIn API credentials
CLIENT_ID = '86sj54i09odtrh'
CLIENT_SECRET = 'WPL_AP1.HOjCrpkLrg9FRGli.f8dw+g=='
REDIRECT_URI = 'http://localhost:5000/linkedin/callback'

# LinkedIn API endpoints
AUTH_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
PROFILE_URL = 'https://api.linkedin.com/v2/me'
EMAIL_URL = 'https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))'


@linkedin_app.route('/')
def home():
    """
    Home route for testing API functionality.
    """
    return jsonify({"message": "Welcome to the LinkedIn OAuth app. Use /login to authenticate."})


@linkedin_app.route('/login', methods=['GET'])
def login():
    """
    Redirect to LinkedIn's OAuth login page.
    """
    state = 'random_unique_state'  # In production, generate a secure random state
    auth_url = (
        f'{AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}'
        f'&scope=r_emailaddress%20r_liteprofile&state={state}'
    )
    return redirect(auth_url)


@linkedin_app.route('/linkedin/callback', methods=['GET'])
def linkedin_callback():
    """
    Handle LinkedIn's OAuth callback and exchange the authorization code for an access token.
    """
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

    # Parse the access token
    token_json = token_response.json()
    access_token = token_json.get('access_token')
    session['linkedin_access_token'] = access_token  # Store access token in session
    return redirect(url_for('validate_email'))


@linkedin_app.route('/validate_email', methods=['GET'])
def validate_email():
    """
    Validate the LinkedIn email domain to check if it's a UNT email.
    """
    access_token = session.get('linkedin_access_token')
    if not access_token:
        return jsonify({"error": "No access token found"}), 403

    headers = {'Authorization': f'Bearer {access_token}'}

    # Fetch the user's email address
    email_response = requests.get(EMAIL_URL, headers=headers)
    if email_response.status_code != 200:
        return jsonify({"error": "Error fetching email", "details": email_response.json()}), email_response.status_code

    email_data = email_response.json()
    email = email_data.get('elements', [])[0].get('handle~', {}).get('emailAddress')

    # Validate the email domain
    if not email or not email.endswith('@unt.edu'):
        return jsonify({"error": f"Access denied: {email} is not a UNT email address."}), 403

    # Return validated email
    return jsonify({"message": "Email validated successfully", "email": email}), 200


@linkedin_app.route('/profile', methods=['GET'])
def profile():
    """
    Fetch the user's LinkedIn profile information.
    """
    access_token = session.get('linkedin_access_token')
    if not access_token:
        return jsonify({"error": "No access token found"}), 403

    headers = {'Authorization': f'Bearer {access_token}'}

    # Fetch the user's profile
    profile_response = requests.get(PROFILE_URL, headers=headers)
    if profile_response.status_code != 200:
        return jsonify({"error": "Error fetching profile", "details": profile_response.json()}), profile_response.status_code

    profile_data = profile_response.json()
    return jsonify(profile_data), 200


if __name__ == '__main__':
    linkedin_app.run(debug=True)
