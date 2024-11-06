import streamlit as st
import numpy as np
import pandas as pd
from io import StringIO
import time
import sys
from linkml_runtime.utils.schema_as_dict import schema_as_dict
from schema_automator.generalizers.csv_data_generalizer import CsvDataGeneralizer


if 'is_converting' not in st.session_state:
  st.session_state.is_converting = False
if 'is_converted' not in st.session_state:
  st.session_state.is_converted = False
if 'data' not in st.session_state:
  st.session_state.data = "Placeholder data"

def convert():
  st.session_state.is_converting = True
  st.session_state.is_converted = False

st.header('Data Model Conversion')
uploaded_file = st.file_uploader("Upload a file to convert")

if uploaded_file:
  # File path located at => uploaded_file._file_urls.upload_url
  # To convert to a string based IO:
  stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
  st.write('File Preview:')
  with st.container(height=500):
    st.code(stringio.read(), language='tsv', line_numbers=True)

  output_model = st.selectbox('Select the model for the output file', ['OMOP', 'Phenopackets', 'B1MG'])

st.button(
  'Convert',
  disabled=not uploaded_file or st.session_state.is_converting,
  help="Please upload a file to convert" if not uploaded_file else "",
  on_click=convert,
)
st.divider()

if st.session_state.is_converting:
  with st.spinner('Converting...'):
    # TODO - While running LinkML..
    st.session_state.is_converting = False
    st.session_state.is_converted = True
    st.success('Conversion Completed!')

if uploaded_file and st.session_state.is_converted:
  st.download_button(
    label="Download yaml",
    data=st.session_state.data,
    file_name="output.yml",
    mime="application/x-yaml",
  )
