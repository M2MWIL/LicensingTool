import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu

#load all data frames

# define funtions

#convert data types

#Streamlit page
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
    st.title("🔑 Licensing Module")

    if section == "Dashboard":
        st.write("This is the Licensing Module Dashboard section.")
    elif section == "Model":
        st.write("This is the Licensing Module Model section.")