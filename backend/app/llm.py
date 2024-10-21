from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from langchain_core.output_parsers import StrOutputParser
class LLMHandler():
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model= ChatOpenAI(model="gpt-4o-mini", openai_api_key=self.api_key)
    def generate_explanation(self, decision_path, prediction, data):
        prompt = f"""
        You are a alcohol licensing representitive at a company. A machine learning model has come up with the following tree path
        to predict risk about the following enterprise(s). 
        Given the following decision path:
        - {decision_path}
        Here is also the raw table entry without the encodings:
        - {data}
        Explain why the Random Forest model predicted the risk classification of '{prediction}' for this sample. With reference to what you see
        in the raw table entry
        Please explain why this classification is appropriate or inapropriate based on the provided data.

        """
        response = (self.model | StrOutputParser).invoke(prompt)
        
        return response.content