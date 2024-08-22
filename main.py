import streamlit as st


# Title
st.title('Streamlit Tutorial')

# Markdown
st.markdown('## This is a markdown title')

st.sidebar.header('User Input Features')
st.sidebar.markdown('This is a markdown in the sidebar.')
st.sidebar.slider('Slider', 0, 100, (30, 70))
st.sidebar.selectbox('Selectbox', ['option 1', 'option 2', 'option 3'])