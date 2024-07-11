# -*- coding: utf-8 -*-
"""AcademicClassification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iGmXKipswYZGdvDzpM7KUwHO-Ig_pPNt
"""

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

"""## Initial Data Load



"""

academic_data = pd.read_csv("/content/train.csv")

academic_data.head()

academic_data.shape

#Checking data types
academic_data.info()

#Checking null values
academic_data.isnull().sum()

#Checking for duplicate rows

academic_data.duplicated().sum()

academic_data = academic_data.dropna()

academic_data.describe()

#dropping irrelavant columns

academic_data.drop(columns = ["id" , "International", "Nacionality"], axis = 1 , inplace = True)
academic_data.head()

"""## Exploratory data analysis (EDA)"""

#Identifying number of unique values in each columns

for i in academic_data.columns:
  print(f"The column {i} has {academic_data[i].nunique()} values")

"""### Visualisation"""

#Target Distribution

plt.figure(figsize = (10,8))
sns.countplot(x = "Target" , data = academic_data )
plt.title("Target Variable Distribution ")
plt.xlabel('Target Variable')
plt.ylabel('Count')
plt.show()

"""### Numerical Variable Distribution"""

numerical_cols = ['Admission grade',
               'Age at enrollment',
               'Curricular units 1st sem (credited)',
               'Curricular units 1st sem (enrolled)',
               'Curricular units 1st sem (evaluations)',
               'Curricular units 1st sem (approved)',
               'Curricular units 1st sem (grade)',
               'Curricular units 1st sem (without evaluations)',
               'Curricular units 2nd sem (credited)',
               'Curricular units 2nd sem (enrolled)',
               'Curricular units 2nd sem (evaluations)',
               'Curricular units 2nd sem (approved)',
               'Curricular units 2nd sem (grade)',
               'Curricular units 2nd sem (without evaluations)',
               'Unemployment rate',
               'Inflation rate',
               'GDP']

plt.figure(figsize=(18, 40))
plotnumber = 1

for column in numerical_cols:
    if plotnumber <= len(numerical_cols):
        plt.subplot(9, 3, plotnumber)
        sns.kdeplot(academic_data[column], color='green', fill=True)

        plt.xlabel(column)


    plotnumber += 1

plt.suptitle('Numerical Variables Distribution', fontsize=38, y=1)
plt.tight_layout()
plt.show()

"""### Categorical Variable Distribution"""

categorical_cols = ['Marital status',
               'Application mode',
               'Application order',
               'Daytime/evening attendance',
               'Previous qualification',
               'Nacionality',
               "Mother's qualification",
               "Father's qualification",
               "Mother's occupation",
               "Father's occupation",
               'Displaced',
               'Educational special needs',
               'Debtor',
               'Tuition fees up to date',
               'Gender',
               'Scholarship holder',
               'International']

#There is significately less scholarship holders in dropouts

plt.figure(figsize=(10,7))
sns.countplot(academic_data , x ='Target' ,  hue = "Scholarship holder")

plt.show()

#The data was already processed
#one of the genders has less graduates and almost has significant dropouts

plt.figure(figsize=(10,7))
sns.countplot(academic_data , x ='Target' ,  hue = "Gender")

plt.show()

#Tuition fees is not upto date for dropouts compared to other variables

plt.figure(figsize=(10,7))
sns.countplot(academic_data , x ='Target' ,  hue = "Tuition fees up to date")

plt.show()

#Educational special needs is significantly lower

plt.figure(figsize=(10,7))
sns.countplot(academic_data , x ='Target' ,  hue = "Educational special needs")

plt.show()

#The age group above 20 has more  dropouts
plt.figure(figsize=(10,7))
sns.boxplot(data=academic_data, x="Age at enrollment", y="Target")

plt.show()

#the unemployment rate in graduates is almosts similar to dropouts

plt.figure(figsize=(10,7))
sns.boxplot(data=academic_data, x="Unemployment rate", y="Target" , hue = "Gender")

plt.show()

#data['Unemployment rate'].head()

#average inflation rate for graduates is low compared to other variables
plt.figure(figsize=(10,7))
sns.boxplot(data=academic_data, x="Inflation rate", y="Target")

plt.show()

plt.figure(figsize=(10,7))
sns.boxplot(data=academic_data, x="GDP", y="Target")

plt.show()

#The debtors in dropouts are more compared to other variables
#but it does not signify the increase in dropouts because large sum of dropouts are not debtors

plt.figure(figsize=(10,7))
sns.countplot(academic_data , x ='Target' ,  hue = "Debtor")

plt.show()

#more gradutaes compared to other variables are displaced

plt.figure(figsize=(10,7))
sns.countplot(data=academic_data, x="Target" ,hue="Displaced")

plt.show()

#data['Displaced'].unique()

# attendance is significantly higher for all the variables

plt.figure(figsize=(10,7))
sns.countplot(data=academic_data, x="Target" ,hue='Daytime/evening attendance')

plt.show()

#data['Daytime/evening attendance'].unique()

academic_data['Target'] = academic_data['Target'].map({'Graduate': 0, 'Dropout': 1, 'Enrolled': 2})

from sklearn.preprocessing import LabelEncoder
encode = LabelEncoder()
academic_data['Course'] = encode.fit_transform(academic_data['Course'])

academic_data['Course'].value_counts()

#Heat map
plt.figure(figsize=(22, 18))
sns.heatmap(academic_data.corr(), annot=True, cmap='coolwarm', fmt='.1f', linewidths=2, linecolor='lightgrey')
plt.suptitle('Correlation Matrix', fontsize=38, y=1)
plt.show()

#split the data

X = academic_data.drop(columns = "Target" ,axis = 1)
y = academic_data["Target"]

#train test split

X_train , X_test , y_train , y_test = train_test_split(X , y , test_size = 0.3 , random_state = 40 , stratify= y )
print(X.shape , X_train.shape , X_test.shape)

"""## Model Building"""

#model building
from sklearn.ensemble import RandomForestClassifier , GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

models = {
    "Logistic Regression" : LogisticRegression(max_iter= 10),
    "Decision Tree" : DecisionTreeClassifier(),
    "Random Forest" : RandomForestClassifier(),
    "Gradient Boosting" : GradientBoostingClassifier(),



}

#feature_selection function
from sklearn.feature_selection import RFE

def feature_selection(model, X_set , y_set):
  model.fit(X_set, y_set)
  selector = RFE(estimator = model, n_features_to_select=15)
  selector = selector.fit(X_set, y_set)
  cols = X_train.columns[selector.support_]

  return cols

#Evalution  function


def evaluate_model(model, X_train, y_train, X_val, y_val):

    cols= feature_selection(model,X_train, y_train)
    X_train = X_train[cols]
    X_val = X_val[cols]

    model.fit(X_train , y_train)

    y_train_pred = model.predict(X_train)
    y_val_pred = model.predict(X_val)


    metrics = {
        'Train Accuracy': accuracy_score(y_train, y_train_pred),
        'Validation Accuracy': accuracy_score(y_val, y_val_pred),
        'Train Precision': precision_score(y_train, y_train_pred, average='weighted'),
        'Validation Precision': precision_score(y_val, y_val_pred, average='weighted'),
        'Train Recall': recall_score(y_train, y_train_pred, average='weighted'),
        'Validation Recall': recall_score(y_val, y_val_pred, average='weighted'),
        'Train F1': f1_score(y_train, y_train_pred, average='weighted'),
        'Validation F1': f1_score(y_val, y_val_pred, average='weighted'),
    }

    return metrics

import warnings
warnings.filterwarnings('ignore')

results = {}
for model_name, model in models.items():
    results[model_name] = evaluate_model(model, X_train, y_train, X_test, y_test)

results_df = pd.DataFrame(results).T
results_df

"""## Model Selection"""

from sklearn.model_selection import RandomizedSearchCV

param_dist = {
    'n_estimators' :[50 , 100],
    'learning_rate': [0.01 , 0.05, 0.1,0.2],
    'max_depth': [3,4,5,6],
    'min_samples_split' : [2,5,10],
    'min_samples_leaf':[1,2,4]
}

gb_model = GradientBoostingClassifier()

cols= feature_selection(model,X_train, y_train)
X_train = X_train[cols]
X_test = X_test[cols]


random_search = RandomizedSearchCV(estimator = gb_model , param_distributions=param_dist ,
                                   n_iter = 100 , cv = 3 , n_jobs = -1 , verbose = 2 , random_state = 42)

random_search.fit(X_train , y_train)

best_params = random_search.best_params_
print("Best parameters :", best_params)

random_search.best_estimator_

from sklearn.metrics import classification_report

final_model = random_search.best_estimator_

final_model.fit(X_train , y_train)

y_test_pred = final_model.predict(X_test)

print(classification_report(y_test_pred , y_test))