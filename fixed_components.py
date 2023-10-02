import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
#from google.oauth2 import service_account
#import gspread
#from oauth2client.service_account import ServiceAccountCredentials
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode
import io
import numpy as np
import requests
from requests_oauthlib import OAuth2Session
import csv
        
# Insert consent
def add_consent():
    st.session_state['consent'] = True
    data = st.session_state['data']


def consent_form():
    placeholder = st.empty()
    with placeholder.container():
        with st.expander("Consent", expanded=True):
            st.markdown("""
            By submitting the form below you agree to your data being used for research purposes. 
            """)
            agree = st.checkbox("I understand and consent.")
            if agree:
                st.markdown("You have consented. Select \"Next\" to start the survey.")
                st.button('Next', on_click=add_consent)


def user_full_name():
    st.text_input("Please write your full name and surname:", key = 'user_full_name')

def user_position():
    st.text_input("Please write your working position:", key = 'user_position')

def user_professional_category():
    # Professional Category Checkbox
    st.selectbox('Specify your professional category:', ('Policymaker', 'Expert', 'Entrepreneur/Manager'), key="professional_category")

def personal_information():
    placeholder = st.empty()
    with placeholder.container():
        with st.expander("Personal Information", expanded=True):
            user_full_name()
            user_position()
            user_professional_category()

TITLE_INSTRUCTIONS = '''1. Instructions'''

SUBTITLE_INSTRUCTIONS = '''We are interested in learning what you expect the effects of being offered the full Colombia Productiva program are for these firms. \\
For each of the questions, you have to allocate probabilities to different intervals, based on the probability that you think a specific event will happen. You cannot allocate more than 100\%. \\
      As an example, suppose I ask your beliefs of what is going to be the max temperature in Celsius degrees in your city/town tomorrow, it's summer and the weather forecast predicts heavy rain in the morning. 
      
    '''
CAPTION_INSTRUCTIONS = '''As illustrated in the table, you predicted that there's a 45\% chance of having 25 Celsius degrees, 20% chance of having 26 Celsius degrees and so on. \\
   The bar graph shows the distribution of the probabilities assigned to the different temperatures.  '''


# BEGINNING OF THE SURVEY

def instructions():

# Create some example data
    #data_container = st.container()
    placeholder = st.empty()
    with placeholder.container():
        with st.expander("Instruction's example", expanded=True):
            st.subheader(TITLE_INSTRUCTIONS)
            st.write(SUBTITLE_INSTRUCTIONS)

            st.subheader("Temperature Forecast Tomorrow in Your City")
            st.write('Please scroll on the table to see all available options.')

            #with data_container:
            table, plot = st.columns([0.3, 0.7], gap = "large")
            with table:

                # Define Ag-Grid options
                gb = GridOptionsBuilder()
                gb.configure_column("Temperature", editable=False, resizable=True)
                gb.configure_column("Probability", editable=False, resizable=True)

                # Create some example data as a Pandas DataFrame
                values_column = list(range(10, 31))
                zeros_column = [0 for _ in values_column]
                data = {'Temperature': values_column, 'Probability': zeros_column}
                df = pd.DataFrame(data)

                df.at[0, "Temperature"] = '< 10'
                df.at[20, "Temperature"] = '> 30'
                df.at[13, "Probability"] = 5
                df.at[14, "Probability"] = 15
                df.at[15, "Probability"] = 45
                df.at[16, "Probability"] = 20
                df.at[17, "Probability"] = 15

                df['Temperature'] = df['Temperature'].astype('str')


                # Initialize Ag-Grid
                grid_return = AgGrid(df, gridOptions=gb.build(), height=400, fit_columns_on_grid_load=True)
                bins_grid = grid_return["data"]
            
            st.write(CAPTION_INSTRUCTIONS)

            with plot:
            # Display the distribution of probabilities with a bar chart 
                fig, ax = plt.subplots(figsize=(4, 2.5))  # Adjust the figure size as needed

                # Your data plotting code
                ax.bar(bins_grid['Temperature'], bins_grid['Probability'])
                ax.set_xlabel('Temperature', fontsize=8)  # Adjust fontsize as needed
                ax.set_ylabel('Probability', fontsize=8)  # Adjust fontsize as needed
                ax.set_title("Probability Distribution over Tomorrow's Temperatures", fontsize=8)  # Adjust fontsize as needed
                ax.set_xticks(df['Temperature'])
                ax.set_xticklabels(df['Temperature'], fontsize=6)  # Adjust fontsize as needed
                ax.set_yticks(df['Probability'])
                ax.set_yticklabels(df['Probability'], fontsize=6)
                plt.tight_layout()

                # Adjust the title and labels proportions
                fig.subplots_adjust(top=0.9, right=0.95)  # Adjust the values as needed

                st.pyplot(fig, use_container_width=False)
