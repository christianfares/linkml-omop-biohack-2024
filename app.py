import streamlit as st
import numpy as np
import pandas as pd
from io import StringIO
import time
import sys
import json
import yaml
import pandas
from linkml_runtime.utils.schema_as_dict import schema_as_dict
from schema_automator.generalizers.csv_data_generalizer import CsvDataGeneralizer
from schema_builders.omop.transformer import convert_to_standard

INPUT_FILENAME = 'input.tsv'

profiler = CsvDataGeneralizer()

if 'is_converting' not in st.session_state:
  st.session_state.is_converting = False
if 'is_converted' not in st.session_state:
  st.session_state.is_converted = False
if 'data' not in st.session_state:
  st.session_state.data = "Placeholder data"

def convert():
  st.session_state.is_converting = True
  st.session_state.is_converted = False

def format_output_data(format, uploaded_file):
  schema = profiler.convert(file=INPUT_FILENAME, class_name='ClassName', schema_name='SchemeName')
  df = pandas.read_csv(uploaded_file, sep='\t')
  omop_rows = df.apply(lambda row: convert_to_standard(row[['sex', 'age', 'disease']].to_dict()), axis=1)
  persons = [item['person'] for item in omop_rows]
  concept_occurences = [item['condition_occurence'] for item in omop_rows]

  all = {
    'persons': persons,
    'concept_occurences': concept_occurences
  }

  if format == 'YAML':
    return yaml.safe_dump(all, sort_keys=False)
  elif format == 'JSON':
    return json.dumps(all)
  else:
    return 'Hello world?'

def format_output_extension(format, filename='output'):
  if format == 'YAML':
    return f'{filename}.yml'
  elif format == 'JSON':
    return f'{filename}.json'
  else:
    return f'{filename}.txt'
  
def format_output_mimetype(format):
  if format == 'YAML':
    return 'application/x-yml'
  elif format == 'JSON':
    return 'application/json'
  else:
    return 'text/plain'

st.header('Data Model Conversion')
uploaded_file = st.file_uploader("Upload a file to convert")

if uploaded_file:
  # File path located at => uploaded_file._file_urls.upload_url
  # To convert to a string based IO:
  stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

  # Save to filesystem so we can reference later
  with open(INPUT_FILENAME, 'wb') as f: 
    f.write(uploaded_file.getvalue())

  st.write('File Preview:')
  with st.container(height=500):
    st.code(stringio.read(), language='tsv', line_numbers=True)

  output_model = st.selectbox('Select the model the input file should conform to', ['OMOP', 'Phenopackets', 'B1MG'])
  output_format = st.selectbox('Select the output file format', ['JSON', 'YAML'])

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
    st.session_state.data = stringio
    st.session_state.is_converting = False
    st.session_state.is_converted = True
    st.success('Conversion Completed!')

if uploaded_file and st.session_state.is_converted:
  st.download_button(
    label=f"Download {output_format}",
    data=format_output_data(output_format, uploaded_file),
    file_name=format_output_extension(output_format),
    mime=format_output_mimetype(output_format),
  )
