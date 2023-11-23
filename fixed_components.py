import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
#from google.oauth2 import service_account
#import gspread
#from oauth2client.service_account import ServiceAccountCredentials
import io
import numpy as np
import requests
from requests_oauthlib import OAuth2Session
import csv
import altair as alt
        
# Insert consent
def add_consent():
    st.session_state['consent'] = True
    data = st.session_state['data']


def consent_form():
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
    user_full_name()
    user_position()
    user_professional_category()

def secrets_to_json():
    return {
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"],
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"],
        "universe_domain": st.secrets["universe_domain"]
    }

# EXAMPLE 

TITLE_INSTRUCTIONS = '''1. Instructions'''

SUBTITLE_INSTRUCTIONS = '''We are interested in learning what you expect the effects of being offered the full Colombia Productiva program are for these firms. \\
For each of the questions, you have to allocate probabilities to different intervals, based on the probability that you think a specific event will happen. You cannot allocate more than 100\%. \\
      As an example, suppose I ask your beliefs of what is going to be the max temperature in Celsius degrees in your city/town tomorrow, it's summer and the weather forecast predicts heavy rain in the morning. 
      
    '''
CAPTION_INSTRUCTIONS = '''As illustrated in the table, you predicted that there's a 45\% chance of having 25 Celsius degrees, 20% chance of having 26 Celsius degrees and so on. \\
   The bar graph shows the distribution of the probabilities assigned to the different temperatures.  '''

def instructions():
    st.subheader(TITLE_INSTRUCTIONS)
    st.write(SUBTITLE_INSTRUCTIONS)

    st.subheader("Temperature Forecast Tomorrow in Your City")
    st.write('Please scroll on the table to see all available options.')

    table, plot = st.columns([0.4, 0.6], gap = "large")

    with table:
        # Create some example data as a Pandas DataFrame
        values_column = list(range(10, 31))
        zeros_column = [0 for _ in values_column]
        data = {'Temperature': values_column, 'Probability': zeros_column}
        df = pd.DataFrame(data)
        df['Temperature'] = df['Temperature'].astype('object')
        first_value = str('< 10')
        last_value = str('> 30')

        df.at[0, "Temperature"] = first_value
        df.at[20, "Temperature"] = last_value
        df.at[13, "Probability"] = 5
        df.at[14, "Probability"] = 15
        df.at[15, "Probability"] = 45
        df.at[16, "Probability"] = 20
        df.at[17, "Probability"] = 15

       # df['Temperature'] = df['Temperature'].astype('str')
        edited_data = st.data_editor(df, use_container_width=True, hide_index=True, disabled=('Temperature', "Probability"))
            
    st.write(CAPTION_INSTRUCTIONS)

    with plot:
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('Temperature', sort=None),
            y='Probability'
        )

        # Display the chart using st.altair_chart
        st.altair_chart(chart, use_container_width=True)

def submit(): 
    st.session_state['submit'] = True