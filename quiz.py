"""
In the following code-snippet, a dataset is loaded into a pandas dataframe and
the NA values are dropped when the load_data() is called.
The load_data() function is called twice: first after the function definition and
the second time after missing values are counted.

How many times do you think the entire dataset is loaded into a pandas dataframe using the read_csv() function?
"""

import pandas as pd
import streamlit as st

@st.cache(persist=True)
def load_data():
    data = pd.read_csv('dataset.csv')
    data.dropna(inplace=True)
    return data

df = load_data()
count_missing_vals = df.isnull().sum()
df = load_data()