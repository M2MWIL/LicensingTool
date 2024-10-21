import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import plotly.express as px
import pickle
from streamlit_option_menu import option_menu
from model import return_model


#################### Load Data #######################

df = pd.read_csv('AGCOdataset.csv')

map_data= pd.read_csv('map.csv')

# Convert 'Application_Date' to datetime format, handling errors
df['Application_Date'] = pd.to_datetime(df['Application_Date'], errors='coerce')

# Remove any rows where 'Application_Date' could not be converted
df = df.dropna(subset=['Application_Date'])

#################### Load Model #######################
# with open('rf_model.pkl', 'rb') as file:
#     loaded_model = pickle.load(file)

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

    if selected == "Licensing Module":
        section = st.selectbox("Select Section", ["Dashboard", "Model"])

# Main content based on sidebar selection
if selected == "Home":
    st.title("🏠 Home")
    st.write("Welcome to the Home page.")
    
elif selected == "Licensing Module":
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
        col6, col7 = st.columns(2)    
        stacked_data = df.groupby(['Licensing_Decision', 'Premises_Type']).size().reset_index(name='Counts')
        stacked_fig = px.bar(stacked_data, x='Premises_Type', y='Counts', color='Licensing_Decision',
                              title='Licensing Decision by Premises Type', barmode='stack')
        st.plotly_chart(stacked_fig)
        
        # Add two columns for other charts (Risk by Region and Volume Trends)
        col6, col7 = st.columns(2)
        
        # Location Hotspot: Risk by Region (col4)
        with col6:
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
        with col7:
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
        
        
    elif section == "Model":
        # Dropdowns for each feature based on the unique values extracted from your data
        Premises_Type = st.selectbox('Select Premises Type', ['Restaurant', 'Night Club', 'Bar', 'Banquet Hall'])
        Applicant_Type = st.selectbox('Select Applicant Type', ['Corporation', 'Sole Proprietor', 'Partnership'])
        Area_Type = st.selectbox('Select Area Type', ['Urban', 'Suburban', 'Rural'])
        Previous_Licenses_Held = st.selectbox('Previous Licenses Held', ['Yes', 'No'])
        Compliance_History = st.selectbox('Compliance History', ['No Violations', 'Minor Violations', 'Major Violations'])
        Tax_Compliance_Status = st.selectbox('Tax Compliance Status', ['Compliant', 'Non-compliant'])
        Premises_Ownership = st.selectbox('Premises Ownership', ['Owned', 'Leased'])
        Business_Longevity = st.selectbox('Business Longevity', ['Less than 1 year', '1-3 years', '3-5 years', 'More than 5 years'])
        Licensed_Areas = st.selectbox('Licensed Areas', ['None', 'Outdoor Seating', 'VIP Rooms'])
        Automated_Liquor_Dispensers = st.selectbox('Automated Liquor Dispensers', ['Yes', 'No'])
        Lineups_on_Public_Property = st.selectbox('Lineups on Public Property', ['Yes', 'No'])
        Ancillary_Areas = st.selectbox('Ancillary Areas', ['Yes', 'No'])
        Proximity_to_Residential_Area = st.selectbox('Proximity to Residential Area', ['Yes', 'No'])
        Proximity_to_School = st.selectbox('Proximity to School', ['Yes', 'No'])
        Fire_Safety_Certificate = st.selectbox('Fire Safety Certificate', ['Valid', 'Expired', 'Not Available'])
        Municipal_Approval = st.selectbox('Municipal Approval', ['Approved', 'Pending', 'Rejected'])
        Application_Status = st.selectbox('Application Status', ['Approved', 'Pending', 'Rejected'])

        # Collect the input features into an array for prediction
        input_data = np.array([[Premises_Type, Applicant_Type, Area_Type, Previous_Licenses_Held,
                                Compliance_History, Tax_Compliance_Status, Premises_Ownership, Business_Longevity,
                                Licensed_Areas, Automated_Liquor_Dispensers, Lineups_on_Public_Property, Ancillary_Areas,
                                Proximity_to_Residential_Area, Proximity_to_School, Fire_Safety_Certificate,
                                Municipal_Approval, Application_Status]])

        # Convert the NumPy array to a pandas DataFrame
        input_df = pd.DataFrame(input_data, columns=[
            'Premises_Type', 'Applicant_Type', 'Area_Type', 'Previous_Licenses_Held', 'Compliance_History',
            'Tax_Compliance_Status', 'Premises_Ownership', 'Business_Longevity', 'Licensed_Areas',
            'Automated_Liquor_Dispensers', 'Lineups_on_Public_Property', 'Ancillary_Areas',
            'Proximity_to_Residential_Area', 'Proximity_to_School', 'Fire_Safety_Certificate', 'Municipal_Approval',
            'Application_Status'
        ])
        
        with open('rf_model.pkl', 'rb') as file:
            loaded_model = pickle.load(file)

        if st.button('Predict'):
            print(type(input_df))
            prediction = return_model(input_df)
            st.write(f"The predicted output is: {prediction[0]}")
