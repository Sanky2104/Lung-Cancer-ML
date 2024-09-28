# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pickle
import numpy as np
import boto3
from flask_bcrypt import Bcrypt
from flask_session import Session
from urllib.parse import urlencode

app = Flask(__name__)

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
bcrypt = Bcrypt(app)

model = pickle.load(open('logistic_regression_model.pkl', 'rb'))

COGNITO_DOMAIN = "lungcancerml.auth.us-east-1.amazoncognito.com"  # Your Cognito domain, e.g., myapp.auth.us-east-1.amazoncognito.com
COGNITO_CLIENT_ID = "3j1sid5k2u9qbre4k7f9nafemo"
COGNITO_REDIRECT_URI = "http://localhost:5000/callback"  # Your redirect URI
# COGNITO_CLIENT_SECRET = "your_client_secret"  # If applicable
COGNITO_AUTH_URL = f"https://{COGNITO_DOMAIN}/oauth2/authorize"
COGNITO_TOKEN_URL = f"https://{COGNITO_DOMAIN}/oauth2/token"
COGNITO_LOGOUT_URL = f"https://{COGNITO_DOMAIN}/logout"

@app.route('/', methods=['GET'])
def login():
    if 'access_token' in session:
        return render_template('index.html')
    
    # If not logged in, redirect to Cognito Hosted UI for authentication
    cognito_login_url = COGNITO_AUTH_URL + "?" + urlencode({
        'client_id': COGNITO_CLIENT_ID,
        'response_type': 'code',
        'scope': 'openid profile email',
        'redirect_uri': COGNITO_REDIRECT_URI
    })
    return redirect(cognito_login_url)

@app.route('/home', methods=['GET'])
def Home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method=="POST":
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
        if gender=='M':
            gender_f = False
            gender_m = True
        else:
            gender_f = True
            gender_m = False
        values = np.array([[age, smoking, yellow_fingers, anxiety, peer_pressure, chronic_disease, fatigue, allergy, wheezing, alcohol_consuming, coughing, shortness_of_breath, swallowing_difficulty, chest_pain, gender_f, gender_m]])
        prediction = model.predict(values)
        return render_template('result.html', prediction = prediction)

if __name__ == '__main__':
    app.run(debug=True)


