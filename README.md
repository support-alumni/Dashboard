# Dashboard
# LinkedIn OAuth Flask Application

This is a Flask web app that enables LinkedIn OAuth 2.0 login, allowing users to log in with LinkedIn, view profile information, and perform a customized alumni search for University of North Texas (UNT) on LinkedIn.

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
Install dependencies:

bash:
pip install Flask requests
Set environment variables: Create a .env file with the following:

FLASK_SECRET_KEY: Secret key for Flask session management.
LINKEDIN_CLIENT_ID: LinkedIn app client ID.
LINKEDIN_CLIENT_SECRET: LinkedIn app client secret.
Run the application:

bash
Copy code
python app.py
Configuration: Update REDIRECT_URI and FINAL_REDIRECT_URI in the code to match your LinkedIn callback and redirect URLs.

Routes
/: Home page, renders the main page.
/login: Begins LinkedIn OAuth flow by redirecting to LinkedIn authorization.
/linkedin/callback: Callback endpoint for LinkedIn, retrieves the access token.
/profile: Fetches and displays LinkedIn user profile information.
/search: Alumni search form for UNT.
/search_alumni: Generates a LinkedIn search URL for UNT alumni based on degree, graduation year, and location.
Deployment
Use secure values for FLASK_SECRET_KEY and LINKEDIN_CLIENT_SECRET.
Set debug=False in production for security.
