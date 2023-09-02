import streamlit as st
import json

config_file = open('config.json')

config = json.load(config_file)

st.title(config['title'])