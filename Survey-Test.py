import streamlit as st
import json
from fixed_components import *

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


