            
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode
import io
import numpy as np
import requests
from requests_oauthlib import OAuth2Session
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

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



def question_1(config_test):

    data_container = st.container()
    placeholder = st.empty()
    with placeholder.container():
        with st.expander("Question 1", expanded=True):

            st.subheader(config_test['title_question_1'])
            st.write(config_test['subtitle_question_1'])

            x_axis_question_1 = range(
            int(config_test['min_value_graph_1']),
            int(config_test['max_value_graph_1']),
            int(config_test['step_size_graph_1']))

            
            y_axis_question_1 = np.zeros(len(x_axis_question_1))
            question_1_df = pd.DataFrame(list(zip(x_axis_question_1, y_axis_question_1)))
            
            question_1_df.rename(columns = {'0': config_test['column_1_question_1'], '1': config_test['column_2_question_1'] }, inplace = True)
            data_container = st.container()

            with data_container:
                table_1, plot_1 = st.columns([0.3, 0.7], gap = "large")
                with table_1:

                    # Set up Ag-Grid options
                    gb_1 = GridOptionsBuilder()
                    gb_1.configure_column("0", header_name= config_test['column_1_question_1'], editable=False, resizable=True)
                    gb_1.configure_column("1", header_name= config_test['column_2_question_1'], editable=True, resizable=True)

                    # Initialize Ag-Grid
                    grid_return_1 = AgGrid(question_1_df, gridOptions=gb_1.build(), height=400, fit_columns_on_grid_load = True, update_mode=GridUpdateMode.VALUE_CHANGED)

                    # Get the modified data from Ag-Grid
                    bins_grid_question_1 = grid_return_1["data"]
                    
                    st.write(bins_grid_question_1)
                    #st_aggrid(bins_grid, height=400, fit_columns_on_grid_load=True)
                    
                    # Initialize the counter
                    total_percentage_question_1 = int(100)
                    # Calculate the new total sum
                    percentage_inserted_question_1 = sum(bins_grid_question_1.iloc[:, 1])
                    # Calculate the difference in sum
                    percentage_difference_question_1 = total_percentage_question_1 - percentage_inserted_question_1
                    # Update the counter
                    total_percentage_question_1 = percentage_difference_question_1

                    # Display the counter
                    if percentage_difference_question_1 >= 0:
                        st.write(f"**You still have to allocate {percentage_difference_question_1} percent probability.**")
                    else:
                        st.write(f'**:red[You have inserted {abs(percentage_difference_question_1)} percent more, please review your percentage distribution.]**')
                
                num_bins_question_1 = len(bins_grid_question_1.iloc[:, 0])

                with plot_1:
                    # Calculate dynamic values based on the number of bins
                    if (num_bins_question_1 <= 15):

                        figsize_width = num_bins_question_1 * 0.40 # Adjust the multiplier as needed
                        title_fontsize = max(num_bins_question_1 * 0.25, 10)  # Adjust the minimum fontsize as needed
                        label_fontsize = max(num_bins_question_1 * 0.25, 8)  # Adjust the minimum fontsize as needed
                        tick_fontsize = max(num_bins_question_1 * 0.25, 5)   # Adjust the minimum fontsize as needed
                    elif (15 < num_bins_question_1 <= 25):
                        figsize_width = num_bins_question_1 * 0.16 # Adjust the multiplier as needed
                        title_fontsize = max(num_bins_question_1 * 0.16, 10)  # Adjust the minimum fontsize as needed
                        label_fontsize = max(num_bins_question_1 * 0.16, 8)  # Adjust the minimum fontsize as needed
                        tick_fontsize = max(num_bins_question_1 * 0.16, 5)   # Adjust the minimum fontsize as needed

                    elif (25 < num_bins_question_1 <= 35):
                        figsize_width = num_bins_question_1 * 0.09 # Adjust the multiplier as needed
                        title_fontsize = max(num_bins_question_1 * 0.1, 10)  # Adjust the minimum fontsize as needed
                        label_fontsize = max(num_bins_question_1 * 0.1, 8)  # Adjust the minimum fontsize as needed
                        tick_fontsize = max(num_bins_question_1 * 0.1, 5)   # Adjust the minimum fontsize as needed                        
                    # Create the figure with dynamic figsize
                    fig_1, ax_1 = plt.subplots(figsize=(figsize_width, 2.5))  # Adjust the height (2.5) as needed

                    # Your data plotting code
                    ax_1.bar(bins_grid_question_1.iloc[:, 0], bins_grid_question_1.iloc[:, 1])
                    ax_1.set_xlabel(config_test['title_x_axis_question_1'], fontsize=label_fontsize)
                    ax_1.set_ylabel(config_test['title_y_axis_question_1'], fontsize=label_fontsize)
                    ax_1.set_title(config_test['title_barchart_question_1'], fontsize=title_fontsize)
                    ax_1.set_xticks(bins_grid_question_1.iloc[:, 0])
                    ax_1.set_xticklabels(bins_grid_question_1.iloc[:, 0], fontsize=tick_fontsize)
                    ax_1.set_yticks(range(0, 101, 10))
                    ax_1.set_yticklabels(range(0, 101, 10), fontsize=tick_fontsize)

                    fig_1.subplots_adjust(top=0.9, right=0.95)
                    plt.tight_layout()
                    st.pyplot(fig_1, use_container_width=False)

            updated_bins_question_1_df = pd.DataFrame(bins_grid_question_1)

            return updated_bins_question_1_df

def question_2(config_test):

    data_container = st.container()
    placeholder = st.empty()
    with placeholder.container():
        with st.expander("Question 2", expanded=True):

            st.subheader(config_test['title_question_2'])
            st.write(config_test['subtitle_question_2'])

            x_axis_question_2 = range(
            int(config_test['min_value_graph_2']),
            int(config_test['max_value_graph_2']),
            int(config_test['step_size_graph_2']))

            
            y_axis_question_2 = np.zeros(len(x_axis_question_2))
            question_2_df = pd.DataFrame(list(zip(x_axis_question_2, y_axis_question_2)))
            
            question_2_df.rename(columns = {'0': config_test['column_1_question_2'], '1': config_test['column_2_question_2'] }, inplace = True)
            data_container_2 = st.container()

            with data_container_2:
                table_2, plot_2 = st.columns([0.3, 0.7], gap = "large")
                with table_2:

                    # Set up Ag-Grid options
                    gb_2 = GridOptionsBuilder()
                    gb_2.configure_column("0", header_name= config_test['column_1_question_2'], editable=False, resizable=True)
                    gb_2.configure_column("1", header_name= config_test['column_2_question_2'], editable=True, resizable=True)

                    # Initialize Ag-Grid
                    grid_return_2 = AgGrid(question_2_df, gridOptions=gb_2.build(), height=400, fit_columns_on_grid_load = True, update_mode=GridUpdateMode.VALUE_CHANGED)

                    # Get the modified data from Ag-Grid
                    bins_grid_question_2 = grid_return_2["data"]
                    #bins_grid_question_2 = pd.concat([question_2_df, new_data], ignore_index=True)
                    
                    st.write(bins_grid_question_2)
                    #st_aggrid(bins_grid, height=400, fit_columns_on_grid_load=True)
                    
                    # Initialize the counter
                    total_percentage_question_2 = int(100)
                    # Calculate the new total sum
                    percentage_inserted_question_2 = sum(bins_grid_question_2.iloc[:, 1])
                    # Calculate the difference in sum
                    percentage_difference_question_2 = total_percentage_question_2 - percentage_inserted_question_2
                    # Update the counter
                    total_percentage_question_2 = percentage_difference_question_2

                    # Display the counter
                    if percentage_difference_question_2 >= 0:
                        st.write(f"**You still have to allocate {percentage_difference_question_2} percent probability.**")
                    else:
                        st.write(f'**:red[You have inserted {abs(percentage_difference_question_2)} percent more, please review your percentage distribution.]**')
                
                num_bins_question_2 = len(bins_grid_question_2.iloc[:, 0])

                with plot_2:
                    # Calculate dynamic values based on the number of bins
                    if (num_bins_question_2 <= 15):

                        figsize_width_2 = num_bins_question_2 * 0.40 # Adjust the multiplier as needed
                        title_fontsize_2 = max(num_bins_question_2 * 0.25, 10)  # Adjust the minimum fontsize as needed
                        label_fontsize_2 = max(num_bins_question_2 * 0.25, 8)  # Adjust the minimum fontsize as needed
                        tick_fontsize_2 = max(num_bins_question_2 * 0.25, 5)   # Adjust the minimum fontsize as needed
                    elif (15 < num_bins_question_2 <= 25):
                        figsize_width_2 = num_bins_question_2 * 0.16 # Adjust the multiplier as needed
                        title_fontsize_2 = max(num_bins_question_2 * 0.16, 10)  # Adjust the minimum fontsize as needed
                        label_fontsize_2 = max(num_bins_question_2 * 0.16, 8)  # Adjust the minimum fontsize as needed
                        tick_fontsize_2 = max(num_bins_question_2 * 0.16, 5)   # Adjust the minimum fontsize as needed

                    elif (25 < num_bins_question_2 <= 35):
                        figsize_width_2 = num_bins_question_2 * 0.09 # Adjust the multiplier as needed
                        title_fontsize_2 = max(num_bins_question_2 * 0.1, 10)  # Adjust the minimum fontsize as needed
                        label_fontsize_2 = max(num_bins_question_2 * 0.1, 8)  # Adjust the minimum fontsize as needed
                        tick_fontsize_2 = max(num_bins_question_2 * 0.1, 5)   # Adjust the minimum fontsize as needed      

                    # Create the figure with dynamic figsize
                    fig_2, ax_2 = plt.subplots(figsize=(figsize_width_2, 2.5))  # Adjust the height (2.5) as needed

                    ax_2.bar(bins_grid_question_2.iloc[:, 0], bins_grid_question_2.iloc[:, 1])
                    ax_2.set_xlabel(config_test['title_x_axis_question_2'], fontsize=label_fontsize_2)
                    ax_2.set_ylabel(config_test['title_y_axis_question_2'], fontsize=label_fontsize_2)
                    ax_2.set_title(config_test['title_barchart_question_2'], fontsize=title_fontsize_2)
                    ax_2.set_xticks(bins_grid_question_2.iloc[:, 0])
                    ax_2.set_xticklabels(bins_grid_question_2.iloc[:, 0], fontsize=tick_fontsize_2)
                    ax_2.set_yticks(range(0, 101, 10))
                    ax_2.set_yticklabels(range(0, 101, 10), fontsize=tick_fontsize_2)

                    fig_2.subplots_adjust(top=0.9, right=0.95)
                    plt.tight_layout()
                    st.pyplot(fig_2, use_container_width=False)

            updated_bins_question_2_df = pd.DataFrame(bins_grid_question_2)

            return updated_bins_question_2_df


# Submission button + saving data 

def add_submission(updated_bins_question_1_df, updated_bins_question_2_df):
    st.session_state['submit'] = True 
    
    # Update session state
    data = st.session_state['data']

    USER_FULL_NAME = 'User Full Name'
    USER_PROF_CATEGORY = 'User Professional Category'
    USER_POSITION = 'User Working Position'
    MIN_EFF_SIZE = 'Minimum Effect Size'

    data[MIN_EFF_SIZE].append(safe_var('input_question_1'))
    data[USER_FULL_NAME].append(safe_var('user_full_name'))
    data[USER_POSITION].append(safe_var('user_position'))
    data[USER_PROF_CATEGORY].append(safe_var('professional_category'))

    st.session_state['data'] = data
    session_state_df = pd.DataFrame(data)