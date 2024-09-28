from flask import Flask, redirect, request, session, render_template, url_for
import requests
import pickle
import numpy as np
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # You should use a strong secret key in production

# Cognito configuration
CLIENT_ID = "55frhng9fbut7d39u58cbr24ij"
CLIENT_SECRET = ""
COGNITO_DOMAIN = "lungcancerml.auth.us-east-1.amazoncognito.com"  # example: your-app.auth.us-west-2.amazoncognito.com
REDIRECT_URI = "http://localhost:5000/callback"  # Make sure this matches your Cognito app client settings

# Load your pre-trained model
model = pickle.load(open('logistic_regression_model.pkl', 'rb'))

@app.route('/', methods=['GET'])
def home():
    # If the user is not logged in, redirect to the Cognito login page
    if 'id_token' not in session:
        cognito_login_url = "https://lungcancerml.auth.us-east-1.amazoncognito.com/login?client_id=55frhng9fbut7d39u58cbr24ij&response_type=code&scope=email+openid+phone&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fcallback"
        # return redirect(REDIRECT_URI)
        return redirect('/home')
    else:
        # If logged in, render the index page
        # return render_template('index.html')
        return redirect('/home')

@app.route('/home', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/callback', methods=['GET'])
def callback():
    # Get the authorization code from the callback request
    code = request.args.get('code')
    if code is None:
        return "Login failed", 400

    # Exchange the authorization code for tokens
    token_url = f"https://{COGNITO_DOMAIN}/oauth2/token"
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    
    # Optional: Include client secret if using a secret client (more secure)
    auth_header = (CLIENT_ID, CLIENT_SECRET)
    token_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    token_response = requests.post(token_url, data=token_data, headers=token_headers, auth=auth_header)

    if token_response.status_code == 200:
        tokens = token_response.json()
        session['id_token'] = tokens['id_token']
        session['access_token'] = tokens['access_token']
        session['refresh_token'] = tokens['refresh_token']
        return redirect(url_for('home'))
    else:
        return "Token exchange failed", 400

# Predict route (no changes needed in this part)
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == "POST":
        # Ensure the user is logged in
        if 'id_token' not in session:
            return redirect(url_for('home'))

        age = int(request.form['age'])
        smoking = int(request.form['smoking'])
        yellow_fingers = int(request.form['yellow_fingers'])
        anxiety = int(request.form['anxiety'])
        peer_pressure = int(request.form['peer_pressure'])
        chronic_disease = int(request.form['chronic_disease'])
        fatigue = int(request.form['fatigue'])
        allergy = int(request.form['allergy'])
        wheezing = int(request.form['wheezing'])
        alcohol_consuming = int(request.form['alcohol_consuming'])
        coughing = int(request.form['coughing'])
        shortness_of_breath = int(request.form['shortness_of_breath'])
        swallowing_difficulty = int(request.form['swallowing_difficulty'])
        chest_pain = int(request.form['chest_pain'])
        gender = bool(request.form['gender'])
        if gender == 'M':
            gender_f = False
            gender_m = True
        else:
            gender_f = True
            gender_m = False

        values = np.array([[age, smoking, yellow_fingers, anxiety, peer_pressure, chronic_disease, fatigue, allergy, wheezing, alcohol_consuming, coughing, shortness_of_breath, swallowing_difficulty, chest_pain, gender_f, gender_m]])
        prediction = model.predict(values)

        return render_template('result.html', prediction=prediction)

# Main driver function
if __name__ == '__main__':
    app.run(debug=True)
