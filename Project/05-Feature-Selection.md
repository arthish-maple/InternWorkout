<html>
  <head>
    <h1>Feature Selection</h1>
  </head>
  <body>
    <h3>Feature Selection is done using Recursive feature elimination (RFE) is a feature selection method that fits a model and removes the weakest feature (or features) until the specified number of features is reached.</h3>
    <ul>
      <li>from sklearn.feature_selection import RFE  :  to import rfe for feature selection </li>
      <li>def selector(model_name,model, X_set , y_set): we have implemented the code to work as a function that helps derive feature selection for each model</li>
      <li>RFE(estimator=model,n_features_to_select=15) : The method is used for feature selection  </li>
      <li>The function returns important columns </li>
      <li>The important columns for each model is saved in dictionary  </li>
    </ul>

  
  </body>
</html>
