Objective:


Housing Data Case Study
With 13 predictor variables we need to predict price from the data set
Step 1: Importing and Merging Data
 importing libraries and  dataset 
* Housing.csv


Step 2: Inspecting the Dataframe
Checking the shape of the data frame and looking for statistical aspects using info() method and describe() method


Step 3: Data Preparation
Dropping the repeated variables
Checking for Missing Values and Inputting Them
Variables creating dummy variables for the remaining categorical variables






Step 4: Test-Train Split
The dataset is split as train and test set using train_test_split method from sklearn library the split is done  between 80% train and 20% test set


Step 5: Feature Scaling
the feature scaling is done using standard scaler for continuous numeric variables


Step 6: Looking at Correlations
Dropping highly correlated dummy variables


Step 7: Model Building
using RFE feature selection we have selected important variables for the model 
Vif method to check the collinearity for the variables 
We have build models based on below given algorithm 
* Linear Regression


Step 8: Model Evaluation
Based on the r2_score for the train set the accuracy is 68% and for  the test data accuracy on the Linear Regression Model is 67%. The model was able to predict 67% of unseen data which is good for prediction.