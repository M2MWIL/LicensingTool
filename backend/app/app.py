from flask import Flask, request, jsonify
import pandas as pd
import pickle
from llm import LLMHandler
import os


with open('model/random_forest_model.pickle', 'rb') as model_file:
    rf_model = pickle.load(model_file)

app = Flask(__name__)

# Initialize LLM handler
llm_handler = LLMHandler()

# Helper function to extract decision path
def extract_decision_path_for_prediction(sample_data, rf_model, trees):
    decision_path_text = ""
    for i, tree in enumerate(trees):
        decision_path = tree.decision_path(sample_data)
        node_indicator = decision_path.indices
        
        decision_path_text += f"Tree {i+1}:\n"
        for node_id in node_indicator:
            if node_id < tree.tree_.node_count:
                feature = tree.tree_.feature[node_id]
                threshold = tree.tree_.threshold[node_id]
                feature_name = sample_data.columns[feature]
                decision_path_text += f"  Node {node_id}: Feature '{feature_name}' <= {threshold}\n"
        leaf_node = tree.apply(sample_data)
        decision_path_text += f"  Reached leaf node: {leaf_node[0]}\n"
    
    return decision_path_text

# Define API endpoint for making predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from the request
        input_data = request.json
        test_data = pd.DataFrame(input_data['features'])

        # Filter columns according to the trained model's columns
        df_test_filtered = test_data[rf_model.feature_names_in_]

        # Make predictions
        y_test_pred = rf_model.predict(df_test_filtered)

        # Extract decision paths for each prediction
        decision_paths = rf_model.apply(df_test_filtered)

        # Store the results
        results = []
        trees = rf_model.estimators_

        for i, (pred, path) in enumerate(zip(y_test_pred, decision_paths)):
            sample_data = df_test_filtered.iloc[[i]]
            raw_data = test_data.iloc[i]
            decision_path = extract_decision_path_for_prediction(sample_data, rf_model, trees)
            
            # Generate explanation from the LLM
            explanation = llm_handler.generate_explanation(decision_path, pred, raw_data.to_dict())

            # Prepare the result for this entry
            application_result = ''
            if pred == 'Low':
                application_result = 'Approved'
            elif pred == 'Moderate':
                application_result = 'Approved With Condition'
            else:
                application_result = 'Rejected'

            results.append({
                "Application_Result": application_result,
                "Predicted_Risk_Classification": pred,
                "Decision_Path": decision_path,
                "Explanation": explanation
            })

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)