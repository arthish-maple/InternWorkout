# Import necessary libraries
import numpy as np

import pickle


# Define a function to load the pre-trained model
def load_model():
   
    model = pickle.load(open('final_model.sav','rb'))
    return model



# Define a function to make predictions
def predict(model, input_data):
    # Preprocess the input data
    processed_data = input_data.reshape(1,-1)
    
    # Make predictions using the model
    predictions = model.predict(processed_data)
    
    return predictions


if __name__ == "__main__":
    
    # Load the model
    model = load_model()
    input_data = (13,7,127.5,1,1,19,8,8,7,12.90857142857143,8,8,7,12.90857142857143,-1.7)
    # Example of unseen data (replace with your actual data)
    unseen_data = np.array(input_data)
    
    # Predict on unseen data
    predictions = predict(model, unseen_data)
    
    # Display predictions
    if predictions[0] == 0:
        print("The Student is a Graduate")
    elif predictions[0] == 1:
        print("The Student is a Dropout")
    else:
        print("The Student is Enrolled")    

