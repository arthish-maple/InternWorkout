import pickle
from flask import Flask, request, render_template, redirect, url_for
import numpy as np
import joblib

model_file = 'Models/final_forest_model.pkl'

with open(model_file, 'rb') as file:
    model = pickle.load(file)

# Load the scaler from the file
scaler = joblib.load('Models/scaler.pkl')

def convert_to_numeric(value):
    if value == 'yes':
        return 1
    elif value == 'no':
        return 0
    else:
        return value

app = Flask(__name__ , template_folder='templates')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract features from the form data
        features = [
            float(request.form.get('tenure', 0)),
            convert_to_numeric(request.form.get('paperlessbilling', 'no')),
            float(request.form.get('monthlycharges', 0)),
            convert_to_numeric(request.form.get('seniorcitizen', 'no')),
            convert_to_numeric(request.form.get('partner', 'no')),
            convert_to_numeric(request.form.get('dependents', 'no')),
            convert_to_numeric(request.form.get('multiplelines', 'no')),
            convert_to_numeric(request.form.get('onlinesecurity', 'no')),
            convert_to_numeric(request.form.get('onlinebackup', 'no')),
            convert_to_numeric(request.form.get('deviceprotection', 'no')),
            convert_to_numeric(request.form.get('techsupport', 'no')),
            convert_to_numeric(request.form.get('streamingmovies', 'no')),
            convert_to_numeric(request.form.get('Contract_One year', 'no')),
            convert_to_numeric(request.form.get('Contract_Two year', 'no')),
            convert_to_numeric(request.form.get('paymentmethod_electronic', 'no'))
        ]

        if not features:
            return redirect(url_for('index'))

        # Convert features to a format suitable for the model
        features_array = np.array(features).reshape(1, -1)
        features_to_scale = features_array[:, [0, 2]]

        # Scale the features
        scaled_features = scaler.transform(features_to_scale)
        features_array[:, [0, 2]] = scaled_features

        # Make prediction
        prediction = model.predict(features_array)

        if prediction[0] == 0:
            message = "The customer will not churn"
        elif prediction[0] == 1:
            message = "The customer will churn"

        # Render the output.html template with prediction results
        return render_template('output.html', prediction=int(prediction[0]), message=message)

    except Exception as e:
        # Handle any exceptions that occur
        return f"An error occurred: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
