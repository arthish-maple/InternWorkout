Objective:


Housing Data Case Study
To use Lasso regularisation on overfit model
Step 1: Importing and Merging Data
 importing libraries and  dataset 




Step 2: Inspecting the Dataframe
Checking the shape of the data frame and looking for statistical aspects using info() method and describe() method


Step 3: Data Preparation
Dropping the repeated variables
Checking for Missing Values and Inputting Them
Variables creating dummy variables for the remaining categorical variables To overfit the model to test the regularisation method






Step 4: Test-Train Split
The dataset is split as train and test set using train_test_split method from sklearn library the split is done  between 80% train and 20% test set


Step 5: Model Building
We have build models based on below given algorithm 
* Linear Regression


Step 6: Model Evaluation
Based on the r2_score for the train set the accuracy is 68% and for  the test data accuracy on the Linear Regression Model is 13%. The model is clearly overfitting so we have used lasso regularisation. The model is now able  to predict 66% of test data which is good for prediction.