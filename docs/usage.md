# Usage Guide for LicencingTool Pipeline

This document provides an overview of all functions within the pipeline that are necessary for the LicencingTool app to work. 

## Functions Overview

## data_processing.py

1. def apply_weights(self, X)

- Objective: apply weights to each of the features
- Parameters: 
self(Self@DataProcessor): class that contains the columns of data to process
X(pd.DataFrame): contains the feature data of original pandas dataframe
- Returns: dataframe with weights applied to each feature

2. encode_columns(self, X)

- Objective: convert the feature columns to weighted forms
- Parameters: 
self(Self@DataProcessor): DataProcessor class that contains the columns to encode
X(pd.DataFrame): contains the feature data of the original pandas dataframe
- Returns: encoded columns

## models.py

1. train_model(self, X_train, y_train)

- Objective: train the model on subset of feature and label data
- Parameters: 
self(Self@ModelHandler): class that contains the model to be handled 
X_train(pd.DataFrame): the training data for the features
y_train(pd.DataFrame): the training data for the label
- Returns: model, feature importances, accuracy and model report

2. predict(self, X_test)

- Objective: get the model's testing predictions
- Parameters: 
self(Self@ModelHandler): contains the model to be handled
X_test(pd.DataFrame): dataframe for the feature testing data
- Returns: predictions for the label on feature testing data

3. save_model(self, filepath)

- Objective: save the model results to another file
- Parameters:
self(Self@ModelHandler): contains the model to be handled
filepath: path to the file with model results
- Returns: file that model has been saved to 

4. load_model(self, filepath)

- Objective: load the model that was saved in save_model
- Parameters: 
self(Self@ModelHandler): class containing the model to be loaded
filepath: path to file containing the model
- Returns: loaded model

## llm.py

1. get_licensing_process(self)

- Objective: feed the licencing process information into the LLM to give it context
- Parameters: 
self(Self@LLMHandler): class that contains LLM being used 
- Returns: read file that contains information about the process of licencing businesses

2. generate_explanation(self, decision_path, prediction, data)

- Objective: get explanation from LLM as to why the model made the predictions it did
- Parameters:
self(Self@LLMHandler): class that contains the LLM being handled
decision_path: the path to the predictions made by the model 
prediction: the prediction made by the model such as high, medium or low risk
data: the data before encoding
- Returns: an LLM explanation as to why the model made the predictions it did

## app.py

1. extract_decision_path_for_prediction(sample_data, rf_model, trees)

- Objective: extract the decision tree path for prediction
- Parameters: 
sample_data: sample data to help extract the decision tree path
rf_model(BufferedReader): class that reads saved model 
trees: the different decision trees in the random forest
- Returns: the decision path for the prediction

2. def predict()

- Objective: run the model prediction 
- Parameters: N/A
- Returns: json of the resulting predictions