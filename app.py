from flask import Flask, redirect, url_for, request, session, jsonify, render_template
import requests
import os
import urllib.parse

# Initialize the Flask application
linkedin_app = Flask(__name__)
linkedin_app.secret_key = 'Mmp1868397Iranhomebaba!'  # Use an environment variable for production

# LinkedIn OAuth settings
CLIENT_ID = '86sj54i09odtrh'
CLIENT_SECRET = 'WPL_AP1.HOjCrpkLrg9FRGli.f8dw+g=='
REDIRECT_URI = 'https://mywebsite.com/linkedin/callback'

@linkedin_app.route('/')
def home():
    return render_template('index.html')

@linkedin_app.route('/login')
def login():
    AUTH_URL = 'https://www.linkedin.com/oauth/v2/authorization'
    state = 'random_unique_state'  # Generate a unique state for each request
    return redirect(f'{AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=r_liteprofile%20r_emailaddress&state={state}')

@linkedin_app.route('/linkedin/callback')
def linkedin_callback():
    code = request.args.get('code')
    if not code:
        return "Error: No authorization code returned", 400

    # Exchange code for an access token
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

    token_json = token_response.json()
    access_token = token_json.get('access_token')
    session['linkedin_access_token'] = access_token

    return redirect(url_for('profile'))

@linkedin_app.route('/profile')
def profile():
    PROFILE_URL = 'https://api.linkedin.com/v2/me'
    access_token = session.get('linkedin_access_token')

    if not access_token:
        return redirect(url_for('home'))

    headers = {'Authorization': f'Bearer {access_token}'}
    profile_response = requests.get(PROFILE_URL, headers=headers)

    if profile_response.status_code != 200:
        return f"Error fetching profile: {profile_response.json()}", profile_response.status_code

    profile_data = profile_response.json()
    return render_template('profile.html', profile_data=profile_data)

@linkedin_app.route('/search')
def search():
    return render_template('search.html')

@linkedin_app.route('/search_alumni')
def search_alumni():
    # Retrieve query parameters
    degree = request.args.get('degree', '')
    grad_year = request.args.get('grad_year', '')
    location = request.args.get('location', '')

    # Construct the search URL with UNT added
    search_keywords = f"{degree} {grad_year} {location} University of North Texas".strip()
    search_url = 'https://www.linkedin.com/search/results/people/?'
    search_params = {
        'keywords': search_keywords,
        'origin': 'FACETED_SEARCH'
    }
    linkedin_search_url = search_url + urllib.parse.urlencode(search_params)

    # Render the search page with the search URL
    return render_template('search.html', linkedin_search_url=linkedin_search_url)

if __name__ == '__main__':
    linkedin_app.run(debug=True)