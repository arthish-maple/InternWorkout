import pickle

from flask import Flask
from flask import request
from flask import jsonify , render_template
import numpy as np
import joblib


model_file = 'final_forest_model.pkl'

with open(model_file, 'rb') as file:
    model = pickle.load(file)

# Load the scaler from the file
scaler = joblib.load('scaler.pkl')



def convert_to_numeric(value):
    if value == 'yes':
        return 1
    elif value == 'no':
        return 0
    else:
        return value



app = Flask('churn')



@app.route('/predict', methods=['GET','POST'])




def predict():
    try:
        # Receive JSON data from the client
        incoming_data = request.get_json()

        # Check if the JSON data is not empty
        if not incoming_data:
            return jsonify({'error': 'No JSON data provided'}), 400

       
        #features = incoming_data.get('features')

        # Extract features from the incoming data
        features = [
            incoming_data.get('tenure'),
            convert_to_numeric(incoming_data.get('paperlessbilling')),
            incoming_data.get('monthlycharges'),
            convert_to_numeric(incoming_data.get('seniorcitizen')),
            convert_to_numeric(incoming_data.get('partner')),
            convert_to_numeric(incoming_data.get('dependents')),
            convert_to_numeric(incoming_data.get('multiplelines')),
            convert_to_numeric(incoming_data.get('onlinesecurity')),
            convert_to_numeric(incoming_data.get('onlinebackup')),
            convert_to_numeric(incoming_data.get('deviceprotection')),
            convert_to_numeric(incoming_data.get('techsupport')),
            convert_to_numeric(incoming_data.get('streamingmovies')),
            convert_to_numeric(incoming_data.get('Contract_One year')),
            convert_to_numeric(incoming_data.get('Contract_Two year')),
            convert_to_numeric(incoming_data.get('paymentmethod_electronic'))
        ]



        if not features:
            return jsonify({'error': 'No features provided in JSON data'}), 400

        # Convert features to a format suitable for the model
        # For instance, convert list to numpy array
        features_array = np.array(features).reshape(1, -1)  

        features_to_scale = features_array[:, [0, 2]]

        # Scale the features
        scaled_features = scaler.transform(features_to_scale)

        # Replace scaled features in the original feature array
        features_array[:, [0, 2]] = scaled_features

        # Make prediction
        prediction = model.predict(features_array)
        
        if prediction[0] == 0:
            message = "The customer will not churn"
        elif prediction[0] == 1:
            message = "The customer will churn"


        # Return the prediction result
        return jsonify({'Prediction': int(prediction[0]) ,
                         "message" : message}), 200

    except Exception as e:
        # Handle any exceptions that occur
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)