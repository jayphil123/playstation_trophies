from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)

# Enable CORS
CORS(app)

# Define constants
CLIENT_ID = "09515159-7237-4370-9b40-3806e67c0891"
AUTH_URL = "https://ca.account.sony.com/api/authz/v3/oauth/authorize"
TOKEN_URL = "https://ca.account.sony.com/api/authz/v3/oauth/token"

# Environment variable for NPSSO token (use dotenv for better security)
NPSSO = os.getenv('NPSSO')

def get_auth_code(npsso):
    params = {
        "access_type": "offline",
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": "psn:mobile.v2.core psn:clientapp",
        "redirect_uri": "com.scee.psxandroid.scecompcall://redirect",
    }
    headers = {"Cookie": f"npsso={npsso}"}
    response = requests.get(AUTH_URL, params=params, headers=headers, allow_redirects=False)
    if 'Location' in response.headers:
        query = response.headers['Location'].split('?', 1)[1]
        code = query.split('=')[1].split('&')[0]
        return code
    raise Exception("Failed to get auth code. Check NPSSO token.")

def get_access_token(auth_code):
    data = {
        "code": auth_code,
        "redirect_uri": "com.scee.psxandroid.scecompcall://redirect",
        "grant_type": "authorization_code",
        "token_format": "jwt",
    }
    headers = {
        "Authorization": "Basic MDk1MTUxNTktNzIzNy00MzcwLTliNDAtMzgwNmU2N2MwODkxOnVjUGprYTV0bnRCMktxc1A=",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(TOKEN_URL, data=data, headers=headers)
    if response.status_code == 200:
        return response.json().get('access_token')
    raise Exception("Failed to obtain access token.")

@app.route('/get-trophy-data', methods=['GET'])
def get_trophy_data():
    try:
        auth_code = get_auth_code(NPSSO)
        access_token = get_access_token(auth_code)

        # Example API call to get trophy titles
        api_url = "https://m.np.playstation.com/api/trophy/v1/users/me/trophyTitles"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to fetch trophy data"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
