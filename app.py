from flask import Flask, render_template, url_for, request, redirect
import pickle
import numpy as np
import MySQLdb.cursors
from flask_mysqldb import MySQL

app = Flask(__name__)

# Load your pre-trained model
model = pickle.load(open('logistic_regression_model.pkl', 'rb'))

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Bobo2104@'
app.config['MYSQL_DB'] = 'projects'

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def Home():
    return render_template('home.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/add_user', methods=['GET','POST'])
def add_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Connect to the database and add user
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        mysql.connection.commit()  # Save the changes
        cursor.close()
        return render_template('index.html')
    return render_template('signup.html')

@app.route('/breathewise', methods=['GET', 'POST'])
def Breathewise():
    email = request.form['email']
    password = request.form['password']
    
    # Query the database to check if the user exists
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()
    if user and user['password'] == password:  # For security, use hashing in production
        # User authenticated successfully
        # return "Login successful! Welcome, {}".format(user['name'])
        return render_template('index.html')
    else:
        # User not found or password incorrect
        return "Invalid email or password. Please try again."

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

    return render_template('result.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)