import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import plotly.express as px
import pickle
import os
from data_processing import DataProcessor  # Import DataProcessor from data_processing.py
from models import ModelHandler  # Import ModelHandler from models.py
#from llm import LLMHandler  # Import LLMHandler from llm.py
from streamlit_option_menu import option_menu
import requests


#################### Load Data #######################

df = pd.read_csv('Demo/AGCOdataset.csv')

map_data= pd.read_csv('Demo/map.csv')

# Convert 'Application_Date' to datetime format, handling errors
df['Application_Date'] = pd.to_datetime(df['Application_Date'], errors='coerce')

# Remove any rows where 'Application_Date' could not be converted
df = df.dropna(subset=['Application_Date'])

#################### Load Model #######################
# with open('rf_model.pkl', 'rb') as file:
# Set the path to the random forest model
model_path = os.path.join(os.path.dirname(__file__), 'models/random_forest_model.pickle')

# Initialize model handler and load the model
model_handler = ModelHandler()
model_handler.load_model(model_path)
#llm_handler = LLMHandler()


# Initialize data processor
data_processor = DataProcessor()

#################### Streamlit Layout #######################

# Set the layout to wide
st.set_page_config(layout="wide")

# Get current time
now = datetime.now()
# Get today's date in the desired format
today = now.strftime('%Y-%m-%d')
# Determine the greeting based on the time of day
current_hour = now.hour
if current_hour < 12:
    greeting = "Good Morning"
elif 12 <= current_hour < 18:
    greeting = "Good Afternoon"
else:
    greeting = "Good Evening"

# Sidebar setup
with st.sidebar:
    # Home with icon
    selected = option_menu(
        "Main Menu", 
        ["Home", "Licensing Module"], 
        icons=["house", "gear"],  # Icons for the items
        menu_icon="cast", 
        default_index=0
    )

    

# Main content based on sidebar selection
if selected == "Home":
    st.title("🏠 Home")
    st.title("Welcome to the Licensing Tool for Regulators")

    st.markdown(
    """
    <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px; border: 1px solid #ddd; max-width: 800px; margin: 0 auto;">
    <h3>How to Use This Tool</h3>
    <p>The Licensing Module in this tool is designed to help regulators with the licensing decision process.</p>
    <ul>
        <li><b>Dashboard</b>: Use the dashboard to view high-level metrics and insights related to the licensing process. This section provides an overview of trends and statistics that can help in monitoring and decision-making.</li>
        <li><b>Licensing Decision Predictor</b>: Use this section to predict the outcome of licensing decisions. You can input various data points to get a prediction, and view the reasoning analysis done by the LLM (Large Language Model) to understand the basis for the decision. Additionally, you can see recommendations based on the predicted results, which can assist in making informed regulatory decisions.</li>
    </ul>
    </div>
    """, 
    unsafe_allow_html=True
    )
  
    
elif selected == "Licensing Module":
    with st.sidebar:
        section = option_menu(
            "Options", 
            ["Dashboard", "Licensing Decision Predictor"],
            icons=["bar-chart", "activity"],  # You can replace these with relevant icons
            menu_icon="list", 
            default_index=0
        )
    # Display a greeting message and today's date
    st.write(f"Date: {today}")
    st.title(f"{greeting}, Welcome to the Licensing Module!")

    if section == "Dashboard":

        st.header("License Application Dashboard")

        # Sidebar filters
        st.sidebar.title('Filter Pane')
        #premises_types = st.sidebar.multiselect("Select Premises Type", df['Premises_Type'].unique(), default=df['Premises_Type'].unique())
        #applicant_types = st.sidebar.multiselect("Select Applicant Type", df['Applicant_Type'].unique(), default=df['Applicant_Type'].unique())
        risk_class = st.sidebar.multiselect("Select Risk Classification", df['Risk_Classification'].unique(), default=df['Risk_Classification'].unique())

        # Apply filters
        df_filtered = df[df['Risk_Classification'].isin(risk_class)]

        # Create columns layout (3 columns for better organization)
        col1, col2, col3 = st.columns([2, 3, 1])

        # Application Status Overview (col1)
        with col1:
            st.subheader("Licensing Decision Overview")
            # Group by Licensing Decision
            licensing_counts = df_filtered['Licensing_Decision'].value_counts().reset_index()
            licensing_counts.columns = ['Licensing_Decision', 'Count']
            fig_licensing = px.pie(licensing_counts, values='Count', names='Licensing_Decision', 
                                title='Licensing Decision Distribution')
            st.plotly_chart(fig_licensing, use_container_width=True)

        # Risk Classification Distribution (col2)
        with col2:
            st.write("#### Risk Category Distribution")

            # Group data by 'Risk Classification' and count the number of entities
            grouped_data_risk = df_filtered.groupby('Risk_Classification').size().reset_index(name='Entity Count')

            # Define custom color mapping for Risk Classification
            custom_colors = {'High': 'red', 'Low': 'green', 'Moderate': 'orange'}
            
            # Create bubble chart for Risk Classification Distribution
            fig_risk_bubble = px.scatter(grouped_data_risk, 
                                        x="Risk_Classification", 
                                        y="Entity Count", 
                                        size="Entity Count", 
                                        color="Risk_Classification", 
                                        hover_name="Risk_Classification",
                                        color_discrete_map=custom_colors,  # Apply custom colors
                                        size_max=60)  # Set max size for bubbles
            
            fig_risk_bubble.update_layout(
                xaxis_title="Risk Classification",
                yaxis_title="Count of Entities",
                title="Risk Classification Distribution (Bubble Chart)"
            )
    
            # Display the bubble chart
            st.plotly_chart(fig_risk_bubble, use_container_width=True)

        
        # New vs Renewal
        with col3:
            st.write("#### New vs Renewal")

            # Filter data for renewal and new applications
            total_count = df_filtered.shape[0]
            renewal_count = df_filtered[df_filtered['Is_Renewal'] == 'Yes'].shape[0]
            new_count = total_count - renewal_count

            # Calculate percentages
            renewal_percentage = (renewal_count / total_count) * 100
            new_percentage = (new_count / total_count) * 100

            # Create resized donut chart for 'New' applications
            fig_new = go.Figure(data=[go.Pie(values=[new_percentage, 100 - new_percentage], 
                                            labels=['New', ''],
                                            hole=0.6,  # Reduce the hole size to make the chart smaller
                                            marker_colors=['blue', 'lightgray'])])  # Blue for new
            fig_new.update_layout(
                height=175,  # Adjust height to match other charts
                margin=dict(t=20, b=20, l=0, r=0),  # Adjust margins for more compact fit
                showlegend=False, 
                annotations=[dict(text=f'{new_percentage:.0f}%', x=0.5, y=0.5, font_size=18, showarrow=False)]
            )
            fig_new.update_traces(textinfo='none')

            # Create resized donut chart for 'Renewal' applications
            fig_renewal = go.Figure(data=[go.Pie(values=[renewal_percentage, 100 - renewal_percentage], 
                                                labels=['Renewal', ''], 
                                                hole=0.6,  # Reduce the hole size
                                                marker_colors=['green', 'lightgray'])])  # Green for renewal
            fig_renewal.update_layout(
                height=175,  # Adjust height to match other charts
                margin=dict(t=20, b=20, l=0, r=0),  # Adjust margins
                showlegend=False, 
                annotations=[dict(text=f'{renewal_percentage:.0f}%', x=0.5, y=0.5, font_size=18, showarrow=False)]
            )
            fig_renewal.update_traces(textinfo='none')

            # Display the donut charts on top of each other
            st.write("New Applications")
            st.plotly_chart(fig_new, use_container_width=True)
            
            st.write("Renewal Applications")
            st.plotly_chart(fig_renewal, use_container_width=True)
        
        # Add two columns for other charts (Feature importance AND approval by premises type)
         
       
        st.write("#### Licensing Decision by Premises Type") 
        stacked_data = df.groupby(['Licensing_Decision', 'Premises_Type']).size().reset_index(name='Counts')
        stacked_fig = px.bar(stacked_data, x='Premises_Type', y='Counts', color='Licensing_Decision',
                                title='Licensing Decision by Premises Type', barmode='stack')
        st.plotly_chart(stacked_fig)
        
        st.write("#### Feature Importance")
        # Data
        datafi = {
           'Feature': [
               'Proximity_to_Residential_Area', 'Premises_Ownership', 'Municipal_Approval', 
                'Tax_Compliance_Status', 'Proximity_to_School', 'Premises_Type', 
                'Compliance_History', 'Area_Type', 'Fire_Safety_Certificate', 
                'Lineups_on_Public_Property', 'Business_Longevity', 'Licensed_Areas', 
                'Applicant_Type', 'Previous_Licenses_Held'
            ],
            'Importance': [
                0.164621, 0.157167, 0.096508, 0.095660, 0.086620, 0.074360, 0.074295, 
                0.073622, 0.065535, 0.039895, 0.031250, 0.029291, 0.005958, 0.005216
            ]
        }

        # Create DataFrame
        df = pd.DataFrame(datafi)

        # Waterfall chart using Plotly
        fig = go.Figure(go.Waterfall(
            name = "Feature Importance",
            orientation = "v",
            x = df['Feature'],
            y = df['Importance'],
            decreasing = {"marker":{"color":"red"}},
            increasing = {"marker":{"color":"green"}},
            totals = {"marker":{"color":"blue"}}
        ))

        # Add chart title and layout
        fig.update_layout(
            title = "Feature Importance Waterfall Chart",
            waterfallgap = 0.2,
            showlegend = True
        )

        # Display the chart in Streamlit
        st.plotly_chart(fig)
        col8, col9 = st.columns(2)
        
        # Location Hotspot: Risk by Region (col4)
        with col8:
            st.write("#### Map Location")
            # Rename latitude and longitude columns
            map_data.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'}, inplace=True)

            # Randomly assign colors to each point
            colors = np.random.choice(['red', 'orange', 'green'], size=len(map_data))
            map_data['color'] = colors

            # Create the map using Plotly with random colors and custom markers
            fig = px.scatter_mapbox(map_data, 
                                    lat='lat', 
                                    lon='lon', 
                                    hover_name='Business_Name',  # Column to display on hover
                                    hover_data={'Business_Address': True},  # Additional details to display on hover
                                    color='color',  # Color by the 'color' column
                                    color_discrete_map={'red': 'red', 'orange': 'orange', 'green': 'green'},  # Force specific colors
                                    zoom=10, 
                                    height=500)

            # Update the layout to use custom markers/icons
            fig.update_traces(marker=dict(size=18, symbol='circle'),  # Set the size and symbol of the markers
                            selector=dict(mode='markers'))

            # Set the mapbox style
            fig.update_layout(mapbox_style="open-street-map")

            # Display the map in Streamlit
            st.plotly_chart(fig)
            
        
        # Application Volume Trends (col5)
        with col9:
            # Ensure 'Application_Date' is in datetime format
            df['Application_Date'] = pd.to_datetime(df['Application_Date'], errors='coerce')

            # Application Volume Trends (New vs. Renewal)
            st.write("#### Application Volume Trends (New vs. Renewal)")
            

            # Extract 'Year_Month' as a string for proper serialization
            df['Year_Month'] = df['Application_Date'].dt.to_period('M').astype(str)

            # Group data by 'Year_Month' and 'Is_Renewal'
            volume_trends = df.groupby(['Year_Month', 'Is_Renewal']).size().reset_index(name='Count')

            # Create a line chart to show volume trends
            fig_volume = px.line(volume_trends, x='Year_Month', y='Count', color='Is_Renewal', title='Application Volume Trends (New vs. Renewal)')
            st.plotly_chart(fig_volume, use_container_width=True)
        
        st.header("Licensing Application Directory")
        st.dataframe(df)  
        
    elif section == "Licensing Decision Predictor":
        st.title("Licensing Risk Prediction")
        
        # Custom CSS for styling the borders and the container
        st.markdown("""
        <style>
            .custom-container {
                padding: 20px;
                border: 2px solid #ccc;
                border-radius: 15px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                background-color: #f9f9f9;
                margin-bottom: 20px;
            }
            .centered {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Create columns with 1:3 ratio
        col1, col2 = st.columns([1, 3])

        # Left column: Input Fields
        with col1:
            st.markdown('<div class="custom-container centered">', unsafe_allow_html=True)
            st.header("Input Fields")
            
            # Collect input data from user
            input_data = {
                'Applicant_Type': st.selectbox('Applicant Type', ['Individual', 'Company', 'Partnership']),
                'Area_Type': st.selectbox('Area Type', ['Urban', 'Rural']),
                'Premises_Ownership': st.selectbox('Premises Ownership', ['Owned', 'Rented']),
                'Business_Longevity': st.slider('Business Longevity (in years)', 0, 20, 2),
                'Licensed_Areas': st.slider('Number of Licensed Areas', 1, 10, 2),
                'Automated_Liquor_Dispensers': st.selectbox('Automated Liquor Dispensers', ['Yes', 'No']),
                'Lineups_on_Public_Property': st.selectbox('Lineups on Public Property', ['Yes', 'No']),
                'Ancillary_Areas': st.selectbox('Ancillary Areas', ['Yes', 'No']),
                'Application_Status': st.selectbox('Application Status', ['Pending', 'Approved', 'Rejected']),
                'Compliance_History': st.selectbox('Compliance History', ['Minor', 'Multiple', 'Severe']),  
                'Tax_Compliance_Status': st.selectbox('Tax Compliance Status', ['Compliant', 'Non-Compliant']), 
                'Premises_Type': st.selectbox('Premises Type', [
                    'Adult Entertainment', 'Arcade-style Facility', 'Art Gallery', 'Athletic Club', 
                    'Auditorium', 'Automotive / Marina', 'Banquet Hall', 'Bar / Sports Bar', 
                    'Big Box Retail Store', 'Billiard / Pool Hall', 'Bingo Hall', 'Bookstore', 
                    'Bowling Alley', 'Community Centre', 'Convenient Store', 
                    'Educational Facility-Over 19 yrs of age', 'Funeral Home', 'General Store', 
                    'Golf Course', 'Grocery Store', 'Hair Salon / Barber Shop', 
                    'Historical Site / Landmark', 'Hotel / Motel', 'Internet Cafe', 
                    'Karaoke Bar / Restaurant', 'Laundromat', 'Live Theatre', 'Medical Facility', 
                    'Military', 'Motion Picture Theatre', 'Museum', 'Night Club', 'Other', 
                    'Railway Car', 'Restaurant (Franchise)', 'Restaurant / Bar', 
                    'Retirement Residence', 'Social Club', 'Spa', 'Speciality Food Store', 
                    'Specialty Merchandise Store', 'Stadium', 'Train'
                ]),
                'Previous_Licenses_Held': st.selectbox('Previous Licenses Held', ['Yes', 'No']),
                'Proximity_to_Residential_Area': st.selectbox('Proximity to Residential Area', ['Yes', 'No']),
                'Proximity_to_School': st.selectbox('Proximity to School', ['Yes', 'No']),
                'Fire_Safety_Certificate': st.selectbox('Fire Safety Certificate', ['Valid', 'Expired']),
                'Municipal_Approval': st.selectbox('Municipal Approval', ['Approved', 'Pending'])
            }
            st.markdown('</div>', unsafe_allow_html=True)

        # Right column: Prediction results
        with col2:
            st.markdown('<div class="custom-container centered">', unsafe_allow_html=True)
            st.header("Prediction Results")
            
            if st.button('Predict'):
                data = {
                    "features": [input_data]  # Send as a list of dictionaries
                }
                api_url = "https://flask-api-regulatory-7f5479effcc5.herokuapp.com/predict"
                try:
                    res = requests.post(api_url, json=data)
                    response_data = res.json()
                    st.subheader("Prediction Results")
                    
                    # Display results
                    for result in response_data:
                        risk_classification = result['Predicted_Risk_Classification']
                        if risk_classification == 'Low':
                            st.success(f"Predicted Risk Classification: {risk_classification}")
                        elif risk_classification == 'Moderate':
                            st.warning(f"Predicted Risk Classification: {risk_classification}")
                        else:
                            st.error(f"Predicted Risk Classification: {risk_classification}")
                        
                        st.markdown(f"**Application Result:** {result['Application_Result']}")
                        with st.expander("Show Explanation"):
                            st.write(f"Explanation: {result['Explanation']}")
                        st.write("---")
                except Exception as e:
                    st.error(f"Error occurred: {e}")
            st.markdown('</div>', unsafe_allow_html=True)