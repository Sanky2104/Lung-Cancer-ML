from flask import Flask, render_template
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open('logistic_regression_model.pkl', 'rb'))

@app.route('/', methods=['GET'])
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


