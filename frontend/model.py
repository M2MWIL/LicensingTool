import pickle
from sklearn.preprocessing import LabelEncoder

def return_model(input):
    input = data_formatter(input)
    # Load the saved Random Forest model
    with open('rf_model.pkl', 'rb') as file:
        rf_model = pickle.load(file)
    return rf_model.predict(input)

def data_formatter(X):

    # Assign weights to the Premise
    premises_type_weights = {
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

    compliance_history_weights = {
        "Minor": 2,
        "Multiple": 3,
        "Severe": 4
    }

    tax_compliance_held_weights = {
        'Compliant':1,
        'Non-Compliant': 2
        
    }
    columns_to_encode = [
    'Applicant_Type', 'Area_Type', 'Premises_Ownership', 'Business_Longevity',
    'Licensed_Areas', 'Automated_Liquor_Dispensers', 'Lineups_on_Public_Property', 
    'Ancillary_Areas',  'Application_Status'
    ]
    label_encoder = LabelEncoder()

    for col in columns_to_encode:
        X[col] = label_encoder.fit_transform(X[col])


    X['Compliance_History'] = X['Compliance_History'].map(compliance_history_weights).fillna(1)
    X['Tax_Compliance_Status'] = X['Tax_Compliance_Status'].map(tax_compliance_held_weights).fillna(0)
    X['Premises_Type'] = X['Premises_Type'].map(premises_type_weights).fillna(0)

    proximity_weights = {"Yes": 1, "No": 0}
    fire_safety_weights = {'Valid': 1, 'Expired': 2}
    municipal_approval_weights = {'Approved': 1, 'Pending': 2}

    X['Previous_Licenses_Held'] = X['Previous_Licenses_Held'].map(proximity_weights)
    X['Proximity_to_Residential_Area'] = X['Proximity_to_Residential_Area'].map(proximity_weights)
    X['Proximity_to_School'] = X['Proximity_to_School'].map(proximity_weights)
    X['Fire_Safety_Certificate'] = X['Fire_Safety_Certificate'].map(fire_safety_weights)
    X['Municipal_Approval'] = X['Municipal_Approval'].map(municipal_approval_weights)

    return X