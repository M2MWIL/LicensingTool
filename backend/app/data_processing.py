import pandas as pd
from sklearn.preprocessing import LabelEncoder

class DataProcessor:
    def __init__(self):
        # Define weights
        self.premises_type_weights = {
            'Adult Entertainment': 3, 
        'Arcade-style Facility': 1, 'Art Gallery': 1, 
        'Athletic Club': 2, 
        'Auditorium': 1, 
        'Automotive / Marina': 1, 
        'Banquet Hall': 1, 
        'Bar / Sports Bar': 3, 
        'Big Box Retail Store': 1, 
        'Billiard / Pool Hall': 2, 
        'Bingo Hall': 1, 
        'Bookstore': 1, 
        'Bowling Alley': 2, 
        'Community Centre': 1, 
        'Convenient Store': 2, 
        'Educational Facility-Over 19 yrs of age': 1, 
        'Funeral Home': 1, 
        'General Store': 2, 
        'Golf Course': 1, 
        'Grocery Store': 2, 
        'Hair Salon / Barber Shop': 1, 
        'Historical Site / Landmark': 1, 
        'Hotel / Motel': 2, 
        'Internet Cafe': 1, 
        'Karaoke Bar / Restaurant': 3, 
        'Laundromat': 1, 
        'Live Theatre': 2, 
        'Medical Facility': 1, 
        'Military': 1, 
        'Motion Picture Theatre': 2, 
        'Museum': 1, 
        'Night Club': 3, 
        'Other': 3, 
        'Railway Car': 1, 
        'Restaurant (Franchise)': 2, 
        'Restaurant / Bar': 3, 
        'Retirement Residence': 1, 
        'Social Club': 3, 
        'Spa': 1, 
        'Speciality Food Store': 1, 
        'Specialty Merchandise Store': 1, 
        'Stadium': 2, 
        'Train': 1
        }
        self.compliance_history_weights = {
            "Minor": 2, "Multiple": 3, "Severe": 4
        }
        self.tax_compliance_held_weights = {
            'Compliant': 1, 'Non-Compliant': 2
        }
        self.proximity_weights = {"Yes": 1, "No": 0}
        self.fire_safety_weights = {'Valid': 1, 'Expired': 2}
        self.municipal_approval_weights = {'Approved': 1, 'Pending': 2}

        # Define feature weights
        self.weights_encoded = {
            'Compliance_History': 400, 'Previous_Licenses_Held': 100, 'Premises_Type': 100,
            'Proximity_to_Residential_Area': 100, 'Proximity_to_School': 100,
            'Fire_Safety_Certificate': 100, 'Municipal_Approval': 100
        }

        # Columns that need label encoding
        self.columns_to_encode = [
            'Applicant_Type', 'Area_Type', 'Premises_Ownership', 'Business_Longevity',
            'Licensed_Areas', 'Lineups_on_Public_Property', 
            
        ]
        self.label_encoder = LabelEncoder()

    def apply_weights(self, X):
        # Apply all the mappings for weighted features
        X['Compliance_History'] = X['Compliance_History'].map(self.compliance_history_weights).fillna(1)
        X['Tax_Compliance_Status'] = X['Tax_Compliance_Status'].map(self.tax_compliance_held_weights).fillna(0)
        X['Premises_Type'] = X['Premises_Type'].map(self.premises_type_weights).fillna(0)
        X['Previous_Licenses_Held'] = X['Previous_Licenses_Held'].map(self.proximity_weights)
        X['Proximity_to_Residential_Area'] = X['Proximity_to_Residential_Area'].map(self.proximity_weights)
        X['Proximity_to_School'] = X['Proximity_to_School'].map(self.proximity_weights)
        X['Fire_Safety_Certificate'] = X['Fire_Safety_Certificate'].map(self.fire_safety_weights)
        X['Municipal_Approval'] = X['Municipal_Approval'].map(self.municipal_approval_weights)

        # Apply weight scaling to the features
        for feature, weight in self.weights_encoded.items():
            X[feature] = X[feature] * weight

        return X

    def encode_columns(self, X):
        for col in self.columns_to_encode:
            X[col] = self.label_encoder.fit_transform(X[col])
        return X