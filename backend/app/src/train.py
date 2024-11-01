import pandas as pd
from backend.app.src.data_processing import DataProcessor
from backend.app.src.models import ModelHandler

def main():
    # Load your dataset
    file_shortened = pd.read_csv('data/synthetic_licensing_data.csv')
    
    # Define your features and labels
    X = file_shortened[['Premises_Type', 'Applicant_Type', 'Area_Type', 'Previous_Licenses_Held',
               'Compliance_History', 'Tax_Compliance_Status', 'Premises_Ownership', 'Business_Longevity',
               'Licensed_Areas', 'Lineups_on_Public_Property',
               'Proximity_to_Residential_Area', 'Proximity_to_School', 'Fire_Safety_Certificate',
               'Municipal_Approval']]
    y = file_shortened['Risk_Classification']

    # Initialize the processor and model handler
    processor = DataProcessor()
    model_handler = ModelHandler()

    # Preprocess the data
    
    X = processor.apply_weights(X)
    X = processor.encode_columns(X)

    # Train the model
    model, accuracy, feature_importances = model_handler.train_model(X, y)

    # Save the model
    model_handler.save_model('models/random_forest_model.pickle')

if __name__ == '__main__':
    main()