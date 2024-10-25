# Usage Guide for LicencingTool Pipeline

This document provides an overview of all functions within the pipeline that are necessary for the LicencingTool app to work. 

## Functions Overview

## data_processing.py

1. `apply_weights(self, X)`

### Objective: 
- Apply weights to each of the features.

### Parameters: 
- **self** (*Self@DataProcessor*): Class that contains the columns of data to process.
- **X** (*pd.DataFrame*): Contains the feature data of the original pandas DataFrame.

### Returns: 
- DataFrame with weights applied to each feature.

---

2. `encode_columns(self, X)`

### Objective: 
- Convert the feature columns to weighted forms.

### Parameters: 
- **self** (*Self@DataProcessor*): DataProcessor class that contains the columns to encode.
- **X** (*pd.DataFrame*): Contains the feature data of the original pandas DataFrame.

### Returns: 
- Encoded columns.

---

## models.py

1. `train_model(self, X_train, y_train)`

### Objective: 
- Train the model on a subset of feature and label data.

### Parameters: 
- **self** (*Self@ModelHandler*): Class that contains the model to be handled.
- **X_train** (*pd.DataFrame*): The training data for the features.
- **y_train** (*pd.DataFrame*): The training data for the label.

### Returns: 
- Model, feature importances, accuracy, and model report.

---

2. `predict(self, X_test)`

### Objective: 
- Get the model's testing predictions.

### Parameters: 
- **self** (*Self@ModelHandler*): Contains the model to be handled.
- **X_test** (*pd.DataFrame*): DataFrame for the feature testing data.

### Returns: 
- Predictions for the label on feature testing data.

---

3. `save_model(self, filepath)`

### Objective: 
- Save the model results to another file.

### Parameters: 
- **self** (*Self@ModelHandler*): Contains the model to be handled.
- **filepath**: Path to the file with model results.

### Returns: 
- File that the model has been saved to.

---

4. `load_model(self, filepath)`

### Objective: 
- Load the model that was saved in `save_model`.

### Parameters: 
- **self** (*Self@ModelHandler*): Class containing the model to be loaded.
- **filepath**: Path to the file containing the model.

### Returns: 
- Loaded model.

---

## llm.py

1. `get_licensing_process(self)`

### Objective: 
- Feed the licensing process information into the LLM to give it context.

### Parameters: 
- **self** (*Self@LLMHandler*): Class that contains the LLM being used.

### Returns: 
- Read file that contains information about the process of licensing businesses.

---

2. `generate_explanation(self, decision_path, prediction, data)`

### Objective: 
- Get an explanation from the LLM as to why the model made the predictions it did.

### Parameters: 
- **self** (*Self@LLMHandler*): Class that contains the LLM being handled.
- **decision_path**: The path to the predictions made by the model.
- **prediction**: The prediction made by the model, such as high, medium, or low risk.
- **data**: The data before encoding.

### Returns: 
- An LLM explanation as to why the model made the predictions it did.

---

## app.py

1. `extract_decision_path_for_prediction(sample_data, rf_model, trees)`

### Objective: 
- Extract the decision tree path for a prediction.

### Parameters: 
- **sample_data**: Sample data to help extract the decision tree path.
- **rf_model** (*BufferedReader*): Class that reads the saved model.
- **trees**: The different decision trees in the random forest.

### Returns: 
- The decision path for the prediction.

---

2. `predict()`

### Objective: 
- Run the model prediction.

### Parameters: 
- **N/A**

### Returns: 
- JSON of the resulting predictions.
