# AlumniSearchApp

AlumniSearchApp is a Python-based web application that integrates LinkedIn OAuth and provides APIs to search and retrieve alumni data from a local CSV file. This application is designed to validate users with LinkedIn and fetch alumni information, specifically for the University of North Texas (UNT).

## Features
1. **LinkedIn OAuth Integration**:
   - Users can authenticate via LinkedIn.
   - Validates if the LinkedIn email belongs to UNT (`@unt.edu`).

2. **Alumni Data APIs**:
   - Fetch alumni data from a local CSV file.
   - Search alumni by major or position.
   - Filter alumni who graduated in 2003 or later.

3. **Health Check Endpoint**:
   - Confirms that the application is running.

---

## Prerequisites
- Python 3.7 or above
- Required Python libraries:
  - `flask`
  - `flask-cors`
  - `requests`

To install the dependencies, run:
```bash
pip install -r requirements.txt


Steps to Set Up and Run the Application:
git clone https://github.com/support-alumni/Dashboard.git
cd Dashboard
Prepare the Alumni CSV File: Place a file named csv.txt in the directory:
C:\Users\mahta\Desktop\AlumniSearchApp\csv.txt
Run:
python app.py
access:
http://localhost:5000
API Endpoints
LinkedIn OAuth Integration
Login Endpoint:

URL: /login
Method: GET
Description: Redirects the user to LinkedIn's OAuth login page.
Callback Endpoint:

URL: /linkedin/callback
Method: GET
Description: Exchanges the LinkedIn authorization code for an access token.
Validate Email:

URL: /validate_email
Method: GET
Description: Validates if the LinkedIn email address is a UNT email (@unt.edu).
Alumni Data API
Fetch All Alumni:

URL: /api/alumni
Method: GET
Description: Retrieves alumni who graduated in 2003 or later from UNT.
Response:
[
  {
    "name": "John Doe",
    "major": "Computer Science",
    "position": "Software Engineer",
    "email": "john.doe@unt.edu",
    "graduation_year": 2010
  }
]
Search Alumni:

URL: /api/alumni/search
Method: GET
Query Parameters:
major: Filter by major (case-insensitive).
position: Filter by position (case-insensitive).
Example is:
/api/alumni/search?major=Computer%20Science&position=Engineer
output: [
  {
    "name": "John Doe",
    "major": "Computer Science",
    "position": "Software Engineer",
    "email": "john.doe@unt.edu",
    "graduation_year": 2010
  }
]
Ping Endpoint:

URL: /api/ping
Method: GET
Description: Verifies that the API is running.
Response:
{
  "message": "API is running!"
}

  
