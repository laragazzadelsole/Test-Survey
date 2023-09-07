import streamlit as st
import json
from fixed_components import *

st.set_page_config(layout="wide")

initialize_session_state()

config_file = open('config.json')
config = json.load(config_file)

st.title(config['title'])
st.write(config['description'])

consent_form()

if st.session_state['consent']:

    personal_information()
    instructions()
    instructions_table()

    st.subheader(config['title_question_1'])
    st.write(config['subtitle_question_1'])

    new_bins_df, fig, bins_grid = question_1()