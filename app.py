from flask import Flask, redirect, session, request, url_for
import os
import random
import string
import requests

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'Mmp1868397Iranhomebaba!'  # Secret key for session management

# LinkedIn OAuth settings
CLIENT_ID = '86sj54i09odtrh'
CLIENT_SECRET = 'WPL_AP1.HOjCrpkLrg9FRGli.f8dw+g=='
REDIRECT_URI = 'https://main.dpob7ezby35e0.amplifyapp.com/linkedin/callback'  # Updated to match your Amplify URL
FINAL_REDIRECT_URI = 'https://main.dpob7ezby35e0.amplifyapp.com/'  # Your desired landing page after login

# Function to generate a random state for CSRF protection
def generate_state():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

# Route to initiate LinkedIn login
@app.route('/login')
def login():
    AUTH_URL = 'https://www.linkedin.com/oauth/v2/authorization'
    state = generate_state()
    session['oauth_state'] = state  # Store the state in session

    # Construct LinkedIn authorization URL
    auth_url = f"{AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=r_liteprofile%20r_emailaddress&state={state}"
    return redirect(auth_url)

# Callback route for LinkedIn to redirect to
@app.route('/linkedin/callback')
def linkedin_callback():
    code = request.args.get('code')
    state = request.args.get('state')

    # Verify state parameter to prevent CSRF
    if state != session.get('oauth_state'):
        return "Error: State mismatch. Possible CSRF attack", 400

    # Exchange authorization code for access token
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

    if token_response.status_code != 200:
        return f"Error fetching token: {token_response.json()}", token_response.status_code

    # Store access token in session
    token_json = token_response.json()
    session['linkedin_access_token'] = token_json.get('access_token')

    # Redirect to a final URL or display a success message
    return redirect(FINAL_REDIRECT_URI)  # Redirect to your desired URL after successful authentication

if __name__ == '__main__':
    app.run(debug=True)
