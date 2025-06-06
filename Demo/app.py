import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import plotly.express as px
import pickle
import os
from streamlit_option_menu import option_menu
import requests
import matplotlib.pyplot as plt


#################### Load Data #######################


df = pd.read_csv('Demo/AGCOdataset.csv')

map_data= pd.read_csv('Demo/map.csv')

# Initialize flagged applications DataFrame with the same columns as `df`
if 'flagged_df' not in st.session_state:
    st.session_state['flagged_df'] = pd.DataFrame()  # Empty DataFrame as a placeholder

# Convert 'Application_Date' to datetime format, handling errors
df['Application_Date'] = pd.to_datetime(df['Application_Date'], errors='coerce')

# Reference the DataFrame from session state

# Remove any rows where 'Application_Date' could not be converted
df = df.dropna(subset=['Application_Date'])

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
        menu_icon="select", 
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
        <li><b>Licensing Application List</b>: View a comprehensive list of all licensing applications. This section allows you to explore individual applications, review details of each entity, flag items for follow-up, and make or adjust decisions as needed.</li>
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
            ["Dashboard", "Licensing Application List", "Decision Predictor" ],
            icons=["bar-chart", "list", "activity"],  # You can replace these with relevant icons
            menu_icon="select", 
            default_index=0
        )
    # Display a greeting message and today's date
    st.write(f"Date: {today} ")
    st.write(f"{greeting}, Welcome to the Licensing Module!")

    if section == "Dashboard":

        st.header("License Application Dashboard")

        # Sidebar filters
        st.sidebar.title('Filter Pane')
        #premises_types = st.sidebar.multiselect("Select Premises Type", df['Premises_Type'].unique(), default=df['Premises_Type'].unique())
        #applicant_types = st.sidebar.multiselect("Select Applicant Type", df['Applicant_Type'].unique(), default=df['Applicant_Type'].unique())
        risk_class = st.sidebar.multiselect("Select Risk Classification", df['Risk_Classification'].unique(), default=df['Risk_Classification'].unique())
        licensing_decision = st.sidebar.multiselect("Licensing Decision", df['Licensing_Decision'].unique())
        renewal_status = st.sidebar.radio("Renewal Status", options=["All", "New", "Renewal"])
        premises_type = st.sidebar.multiselect("Premises Type", df['Premises_Type'].unique())
        compliance_history = st.sidebar.selectbox("Compliance History", options=["All", "Compliant", "Non-Compliant", "Unknown"])
        # Apply filters
        df_filtered = df[df['Risk_Classification'].isin(risk_class)]
        
        if licensing_decision:
            df_filtered = df_filtered[df_filtered['Licensing_Decision'].isin(licensing_decision)]

        if renewal_status == "New":
            df_filtered = df_filtered[df_filtered['Is_Renewal'] == "No"]
        elif renewal_status == "Renewal":
            df_filtered = df_filtered[df_filtered['Is_Renewal'] == "Yes"]

        if premises_type:
            df_filtered = df_filtered[df_filtered['Premises_Type'].isin(premises_type)]

        if compliance_history and compliance_history != "All":
            df_filtered = df_filtered[df_filtered['Compliance_History'] == compliance_history]

        # Calculate counts
        total_count = df.shape[0]  # Total number of records
        filtered_count = df_filtered.shape[0]  # Number of records after filtering

        # Display the count in Streamlit
        st.sidebar.write(f"Displaying {filtered_count} out of {total_count} entities")

        # Create columns layout (3 columns for better organization)
        col1, col2, col3 = st.columns([2, 3, 1])

 
 #################### Application Status Overview (col1) ####################### 
        with col1:
            st.subheader("Licensing Decision Overview")
            # Group by Licensing Decision
            licensing_counts = df_filtered['Licensing_Decision'].value_counts().reset_index()
            licensing_counts.columns = ['Licensing_Decision', 'Count']
            fig_licensing = px.pie(licensing_counts, values='Count', names='Licensing_Decision', 
                                title='Licensing Decision Distribution')
            st.plotly_chart(fig_licensing, use_container_width=True)

#################### Risk Classification Distribution (col2) ####################### 
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


#################### New vs Renewal #######################        

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


#################### Feature Importance ####################### 
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
        df1 = pd.DataFrame(datafi)

        # Waterfall chart using Plotly
        fig = go.Figure(go.Waterfall(
            name = "Feature Importance",
            orientation = "v",
            x = df1['Feature'],
            y = df1['Importance'],
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
        col4, col5 = st.columns(2)

#################### Location Map: By Risk Col 4 ####################### 

        with col4:
            st.write("#### Map Location")
            color_map = {}
            if "High" in risk_class:
                color_map["High"] = "red"
            if "Moderate" in risk_class:
                color_map["Moderate"] = "orange"
            if "Low" in risk_class:
                color_map["Low"] = "green"

            # Assign colors to points based on risk classification selection
            # Create a list of colors based on filter pane selections
            colors = [color for risk, color in color_map.items()]

            # Rename latitude and longitude columns in map_data (if not already done)
            if 'Latitude' in map_data.columns and 'Longitude' in map_data.columns:
                map_data.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'}, inplace=True)

            # Add a dummy column in map_data for color based on risk classifications
            map_data['color'] = np.random.choice(colors, size=len(map_data))

            # Create the map with selected colors
            fig = px.scatter_mapbox(
                map_data, 
                lat='lat', 
                lon='lon', 
                hover_name='Business_Name',  # Adjust column name based on map_data structure
                hover_data={'Business_Address': True},
                color='color',  
                color_discrete_map={'red': 'red', 'orange': 'orange', 'green': 'green'},  # Color options based on filter
                zoom=10, 
                height=500
            )

            # Update the layout for custom marker size and style
            fig.update_traces(marker=dict(size=18, symbol='circle'), selector=dict(mode='markers'))
            fig.update_layout(mapbox_style="open-street-map")

            # Display the map in Streamlit
            st.plotly_chart(fig)
          
           
#################### Application Volume Trends (col5) #######################       
        with col5:
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
        


 #################### Licensing Decision Predictor #######################

    elif section == "Decision Predictor":
        st.title("Licensing Risk Prediction")
        
        # Custom CSS for styling the borders and the container
       
        
        # Create columns with 1:3 ratio
        col1, col2 = st.columns([1, 3])

        # Left column: Input Fields
        with col1:
            
            st.header("Input Fields")
            with st.container():
            # Collect input data from user
                input_data = {
                    'Business_Name': st.text_input('Business Name'),
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
            

        # Right column: Prediction results
        with col2:
            
            st.header("Prediction Results")

            # Instructional helper text
            st.caption("Click to analyze inputs and classify risk level of the licensing application.")

            
            with st.container():
                if st.button('Predict Licensing Risk'):
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
                            feature_importance = result['Feature_Importance']
                    
                    
                            st.write("### Feature Importance")
                            features = list(feature_importance.keys())
                            importances = list(feature_importance.values())

                            # Create a bar chart using matplotlib
                            features.append(features[0])
                            importances.append(importances[0])

                            colors = [
                                '#FF6347', '#4682B4', '#32CD32', '#FFD700', '#6A5ACD', 
                                '#FF4500', '#1E90FF', '#228B22', '#FFA07A', '#8A2BE2', 
                                '#FF1493', '#ADFF2F', '#FF69B4', '#20B2AA'
                            ]
                            # Create the radar chart using Plotly
                            fig = go.Figure()

                            for i, feature in enumerate(features[:-1]):  # Exclude the last one (the duplicate to close the loop)
                                fig.add_trace(go.Scatterpolar(
                                    r=[0, importances[i], 0],  # Value for the current feature
                                    theta=[features[i], features[i], features[i]],  # Label the current feature
                                    fill='toself',  # Fill area under the feature
                                    name=feature,
                                    line=dict(color=colors[i % len(colors)]),  # Cycle through colors if more than 14
                                    marker=dict(size=5)
                                ))

                            max_importance = np.max(importances)
                            # Customize the layout of the radar chart
                            fig.update_layout(
                                title='Feature Importance as Spider Chart',
                                polar=dict(
                                    radialaxis=dict(
                                        visible=True,
                                        range=[0, max_importance],  # Set dynamic range based on the maximum value
                                    ),
                                    angularaxis=dict(
                                        tickfont=dict(size=12),  # Adjust size of the angular axis labels (feature names)
                                    ),
                                ),
                                showlegend=True,  # Enable the legend to show each feature's color
                                height=600,
                                width=600
                            )

                            # Display the radar chart in Streamlit
                            st.plotly_chart(fig)
                            st.write("---")
                    except Exception as e:
                        st.error(f"Error occurred: {e}")
            # Show info before button is clicked
                elif 'response_data' not in st.session_state:
                    st.info("Prediction results will appear here after analysis.")
                

 #################### Drill down functionality #######################

    elif section == "Licensing Application List":
        st.title("Licensing Application List")

        if df.empty:
            st.warning("No data available to display.")
        else:
            st.write("### Application Directory")

        # Display the dataframe
        st.dataframe(df)

        # Simulate row selection: Allow the user to select an application by `Application_ID`
        selected_row = st.selectbox("Select Application by ID:", df['Application_ID'])

        # Store the selected entity in session state
        st.session_state['selected_entity'] = selected_row

        # Display the selected row's details in an expander
        if st.session_state.get('selected_entity'):
            selected_data = df[df['Application_ID'] == st.session_state['selected_entity']].iloc[0]

            with st.expander(f"Details for Application ID {st.session_state['selected_entity']}", expanded=True):
                col1, col2 = st.columns(2)

                # Column 1: General details
                with col1:
                    st.write(f"**Applicant Type**: {selected_data['Applicant_Type']}")
                    st.write(f"**Business Address**: {selected_data['Business_Address']}")
                    st.write(f"**Seating Capacity**: {selected_data['Seating_Capacity']}")
                    st.write(f"**Previous Licenses Held**: {selected_data['Previous_Licenses_Held']}")
                    st.write(f"**Compliance History**: {selected_data['Compliance_History']}")
                    st.write(f"**Premises Ownership**: {selected_data['Premises_Ownership']}")

                # Column 2: Other details, including docs with icons
                with col2:
                    st.write(f"**Is Renewal**: {selected_data['Is_Renewal']}")
                    st.write(f"**Risk Classification**: {selected_data['Risk_Classification']}")
                    st.write(f"**Fire Safety Certificate**: {selected_data['Fire_Safety_Certificate']} 🔗 [Open](#)")
                    st.write(f"**Municipal Approval**: {selected_data['Municipal_Approval']} 🔗 [Open](#)")
                    st.write(f"**Business Longevity**: {selected_data['Business_Longevity']}")
                    st.write(f"**Application Date**: {selected_data['Application_Date']}")

                # Licensing Decision and Flag Decision in the same row
                decision_col1, decision_col2 = st.columns([1, 3])

                with decision_col1:
                    st.write(f"**Licensing Decision**: {selected_data['Licensing_Decision']}")

                with decision_col2:  
                    # Action button: Flag Decision
                    if st.button("Flag Decision"):
                        # Append the entire row (all columns) to the flagged DataFrame
                        st.session_state['flagged_df'] = pd.concat([st.session_state['flagged_df'], pd.DataFrame([selected_data])], ignore_index=True)
                        st.success(f"Application {selected_data['Application_ID']} flagged.")

                # Change decision option
                new_decision = st.selectbox("Change Decision", ['Approved', 'Conditional Approval', 'Rejected'], key="decision_change")

                if st.button("Submit Change"):
                    # Update the decision in the DataFrame
                    df.loc[df['Application_ID'] == selected_row, 'Licensing_Decision'] = new_decision
                    
                    # Store the updated DataFrame back into session state
                    st.session_state['df'] = df

                    # Print the updated licensing decision
                    updated_decision = df.loc[df['Application_ID'] == selected_row, 'Licensing_Decision'].values[0]
                    st.success(f"Decision for Application {selected_row} changed to {new_decision}.")
                    st.write(f"**Updated Licensing Decision:** {updated_decision}")

            # Display flagged applications
            st.write("### Flagged Applications")
            st.dataframe(st.session_state['flagged_df'])

