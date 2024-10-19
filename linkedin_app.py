from flask import Flask, redirect, url_for, request, session
import requests
import os

# Initialize the Flask application
linkedin_app = Flask(__name__)

# Set your secret key directly in the code (consider using environment variables for security)
linkedin_app.secret_key = 'Mah12345!'  # Your secret key

# Use your actual LinkedIn client ID and secret directly in the code
CLIENT_ID = '8646rxftgq9t17'  # Your actual client ID
CLIENT_SECRET = 'WPL_AP1.ybsDyCxIbeKMyATs.5KJ3DA=='  # Your actual client secret
REDIRECT_URI = 'http://localhost:5000/linkedin/callback'  # Ensure this matches your app settings

@linkedin_app.route('/')
def home():
    return '<a href="/login">Sign in with LinkedIn</a>'

@linkedin_app.route('/login')
def login():
    AUTH_URL = 'https://www.linkedin.com/oauth/v2/authorization'
    state = 'random_unique_state'  # Generate a unique state for each request
    # Redirecting to LinkedIn for authorization
    return redirect(f'{AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=r_liteprofile%20r_emailaddress&state={state}')

@linkedin_app.route('/linkedin/callback')
def linkedin_callback():
    code = request.args.get('code')
    print(f'Authorization Code: {code}')  # Debugging line to check if code is received

    if not code:
        return "Error: No authorization code returned", 400

    TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
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

    # Handle the token response
    if token_response.status_code != 200:
        return f"Error fetching token: {token_response.json()}", token_response.status_code

    token_json = token_response.json()
    access_token = token_json.get('access_token')
    session['linkedin_access_token'] = access_token

    # Redirect to profile route after obtaining access token
    return redirect(url_for('profile'))

@linkedin_app.route('/profile')
def profile():
    PROFILE_URL = 'https://api.linkedin.com/v2/me'
    access_token = session.get('linkedin_access_token')

    if not access_token:
        return "No access token found. Please log in again."

    headers = {'Authorization': f'Bearer {access_token}'}
    profile_response = requests.get(PROFILE_URL, headers=headers)

    if profile_response.status_code != 200:
        return f"Error fetching profile: {profile_response.json()}", profile_response.status_code

    profile_data = profile_response.json()
    return f'<h1>LinkedIn Profile Data</h1><pre>{profile_data}</pre>'

if __name__ == '__main__':
    linkedin_app.run(debug=True)
