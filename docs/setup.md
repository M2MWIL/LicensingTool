# Licensing Tool Set up Documentation

This document provides detailed information on how to set up and run the pipeline for this regulatory licencing tool.

## Table of Contents
1. Prerequisites
2. Cloning the Repository
3. Installing Dependencies
4. Data
5. Environment Variables


## 1. Prerequisites

Before you begin, ensure you have the following installed on your local system: 

- Python 3.10 + 
- Git 
- Pip (to install Python packages)

## 2. Cloning the Repository

1. Clone the LicencingTool repository to your local machine using: 

```bash
git clone https://github.com/M2MWIL/LicensingTool
```

2. Change directory to the backend directory: 

```bash
cd backend
```

## 3. Installing Dependencies

1. Ensure pip and wheel are up to date: 

```bash
pip install --upgrade pip wheel
```

2. Install all dependencies from requirements.txt: 

``` bash
pip install -r requirements.txt
```

## 4. Data

Make sure your data is in .csv format and is accessible. In order to preprocess your data in this repo, use this command: 

```bash
python data_preprocessing.py data/synthetic_licensing_data.csv
```

Feature List:

1. Application_ID: a unique id that identifies the applicant

2. Applicant_Name: the first and last name of the applicant

3. Business_Name: the name of the business that is applying

4. Application_Date: the date the applicant applied

5. Business_Address: the address of the business 

6. Premises_Type: the type of business such as cafe, restaurant, bar etc. 

7. Applicant_Type: the type of body applying such as sole proprieter, coroporation etc. 

8. Seating_Capacity: the maximum number of people the restaurant can seat

9. Area_Type: type of seating such as indoor seating, outdoor seating or both

10. Previous_Licenses_Held: Has the business held a licence before yes or no 

11. Compliance_History: Has the business had any compliance issues in the past. Could me none, minor, multiple or severe

12. Tax_Compliance_Status: Is the business under complient or non complient tax status

13. Premises_Ownership: Does the business own the land they operate on yes or no

14. Business_Longevity: How long has the business been operating? Could be one year, under one year, more than 5 years etc.

15. Licensed_Areas: Is the business licenced for special seating? Could be none, outdoor seating or VIP rooms

16. Automated_Liquor_Dispensers: Does the business have automated liquor dispensers yes or no

17. Lineups_on_Public_Property: Does the business have lineups on public property yes or no 

18. Ancillary_Areas: are there ancillary areas in the business yes or no 

19. Proximity_to_Residential_Area: Is the business close to a residential area yes or no

20. Proximity_to_School: Is the business close to a school yes or no

21. Fire_Safety_Certificate: Does the business have a valid fire safety certificate? Takes on values valid and expired 

22. Municipal_Approval: Does the business have approval from the city? Could be pending or approved

23. Application_Status: Status of the application. Could be submitted or under review

## Data Extraction and Usage Method: 

- This data is synthetic and is meant to closely represent the features of a company that is a low, medium or high compliance risk in real observations
- The label for the data is a risk classification with values low, medium and high
- There is a risk score calculation which is a numerical value representing the risk level of a company based on the features in the data. The higher the risk score, the riskier the company

## 5. Environment Variables

Make sure you have a .env file that contains: 
- OPENAI_API_KEY: your openai api key

To set up your environment with this key, run the following command: 

```bash
python config.py
```