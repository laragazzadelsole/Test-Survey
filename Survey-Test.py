import streamlit as st
import json
from fixed_components import *
from changing_components import *

st.set_page_config(layout="wide")

initialize_session_state()

config_file = open('config_test.json')
config_test = json.load(config_file)

st.title(config_test['survey_title'])
st.write(config_test['survey_description'])

consent_form()

if st.session_state['consent']:

    personal_information()
    instructions()

    updated_bins_question_1_df = question_1(config_test)
    updated_bins_question_2_df = question_2(config_test)


