from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from langchain_core.output_parsers import StrOutputParser
from config import Config 

class LLMHandler():
    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Make sure it's set in the environment.")
        self.model= ChatOpenAI(model="gpt-4o-mini", openai_api_key=self.api_key)
    def generate_explanation(self, decision_path, prediction, data):
        prompt = f"""
        You are a alcohol licensing representitive at a company. A machine learning model has come up with the following tree path
        to predict risk about the following enterprise(s). 
        Given the following decision path:
        - {decision_path}
        Here are the weights for some of the encoded variables:
        premises type weights:
        'Adult Entertainment': 3, 
        'Arcade-style Facility': 1
        'Art Gallery': 1, 
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
        
        compliance history weights: 
        "Minor": 2, 
        "Multiple": 3, 
        "Severe": 4
        
        tax compliance held weights:
        'Compliant': 1, 
        'Non-Compliant': 2
        
        proximity weights: 
        "Yes": 1
        "No": 0
        
        fire safety weights:  
        'Valid': 1 
        'Expired': 2
        
        municipal approval weights: 
        'Approved': 1,
        'Pending': 2

        
        Some of the features were highlighted to be more important than other like so 
        'Compliance_History': 400, 'Previous_Licenses_Held': 100, 'Premises_Type': 100,
        'Proximity_to_Residential_Area': 100, 'Proximity_to_School': 100,
        'Fire_Safety_Certificate': 100, 'Municipal_Approval': 100
        
        
        Here is also the raw table entry without the encodings:
        - {data}
        Explain why the Random Forest model predicted the risk classification of '{prediction}' for this sample. With reference to what you see
        in the raw table entry
        Please explain why this classification is appropriate or inapropriate based on the provided data.
        If the risk classification is 'Moderate', the application will be a conditional approval. Please explain in detail what conditions the 
        applicant must follow with their conditional approval

        """
        response = self.model.invoke(prompt)
        
        return response.content