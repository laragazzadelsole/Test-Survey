import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
#from google.oauth2 import service_account
#import gspread
#from oauth2client.service_account import ServiceAccountCredentials
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode
import requests
import io
import numpy as np

def initialize_session_state():
    if 'key' not in st.session_state:
        st.session_state['key'] = 'value'
        st.session_state['consent'] = False
        st.session_state['submit'] = False
        st.session_state['No answer'] = ''
       
    if 'data' not in st.session_state:
        st.session_state['data'] = {
            'Minimum Effect Size': [],
            'User Full Name': [],
            'User Working Position': [],
            'User Professional Category': []
        }
    
def safe_var(key):
    if key in st.session_state:
        return st.session_state[key]
    #return st.session_state['No answer']
        
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
    st.selectbox('Specify your professional category:', ('Policymaker', 'Expert', 'Entrepeneur'), key="professional_category")

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
    st.subheader(TITLE_INSTRUCTIONS)
    st.write(SUBTITLE_INSTRUCTIONS)

def instructions_table():

# Create some example data
    data_container = st.container()

    with data_container:
        table, plot = st.columns(2)
        with table:
            # Create Streamlit app
            st.subheader("Temperature Forecast Tomorrow in Your City")

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
        with plot:
        # Display the distribution of probabilities with a bar chart 
        
            fig, ax = plt.subplots()
            ax.bar(bins_grid['Temperature'], bins_grid['Probability'])
            ax.set_xlabel('Temperature')
            ax.set_ylabel('Probability')
            ax.set_title('Probability Distribution over Tomorrow\'s Temperatures')
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)

            st.write(CAPTION_INSTRUCTIONS)


def question_1(config):
    x_axis = range(config['min_value_graph_1'], config['max_value_graph_1'], config['bin_size_graph_1'])
    y_axis = np.zeros(len(x_axis))
    df = pd.DataFrame(list(zip(x_axis, y_axis)))
    data_container = st.container()

    with data_container:
        table, plot = st.columns(2)
        with table:

            # Set up Ag-Grid options
            gb = GridOptionsBuilder()
            gb.configure_column("Probability", editable=False, resizable=True)
            gb.configure_column("Percentage", editable=True, resizable=True)

            # Initialize Ag-Grid
            grid_return = AgGrid(df, gridOptions=gb.build(), height=400, fit_columns_on_grid_load = True, update_mode=GridUpdateMode.VALUE_CHANGED)

            # Get the modified data from Ag-Grid
            bins_grid = grid_return["data"]
            #st_aggrid(bins_grid, height=400, fit_columns_on_grid_load=True)

            # Initialize the counter
            total_percentage = 100
            # Calculate the new total sum
            percentage_inserted = sum(bins_grid['Percentage'])
            # Calculate the difference in sum
            percentage_difference = total_percentage - percentage_inserted

            # Update the counter
            total_percentage = percentage_difference

        
            # Display the counter

            if percentage_difference >= 0:
                st.write(f"**You still have to allocate {percentage_difference} percent probability.**")
            else:
                st.write(f'**:red[You have inserted {abs(percentage_difference)} percent more, please review your percentage distribution.]**')

        with plot:
        # Display the distribution of probabilities with a bar chart 
        
            fig, ax = plt.subplots()
            ax.bar(df, bins_grid['Percentage'])
            ax.set_xlabel('Probability Bins')
            ax.set_ylabel('Percentage of Beliefs')
            ax.set_title('Distribution of Beliefs about the Impact on the Number of Products that Firms Export')
            ax.set_xticks(df)
            ax.set_xticklabels(df, rotation=80)
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)

    new_bins_df = pd.DataFrame(bins_grid)


    return new_bins_df, fig, bins_grid