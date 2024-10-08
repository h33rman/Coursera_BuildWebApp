import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px # Plotly is a graphing library that makes interactive, publication-quality graphs online

DATA_URL = (
    "/home/herman/Documents/DataScience/WebApp_Streamlit_Coursera/Motor_Vehicle_Collisions_-_Crashes.csv"
)
# Add a title
st.title("Motor Vehicle Collisions in New York City")

# Add some text
st.markdown("This application is a Streamlit dashboard that can be used "
            "to analyze motor vehicle collisions in NYC 🗽💥🚗")

# ST CACHE
@st.cache_data(persist=True) # Cache data so it doesn't reload every time

# Load data
def load_data(n_rows):
    data = pd.read_csv(DATA_URL, nrows=n_rows, parse_dates=[['CRASH_DATE', 'CRASH_TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True) # Drop rows with missing lat/long
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
    return data


data_test = load_data(100000)
original_data = data_test


# Explore the data
st.subheader('Where are the most people injured in NYC?')
injured_people = st.slider("Number of persons injured in vehicle collisions", 0, 19) # Min: 0, Max: 19
st.map(data_test.query("injured_persons >= @injured_people")[['latitude', 'longitude']].dropna(how="any")) # Show map with lat/long

st.subheader('How many collisions occur during a given time of day?')
hour = st.slider("Hour to look at", 0, 23) # Choose hour of the day
data_test = data_test[data_test['date/time'].dt.hour == hour] # Filter data
st.markdown(f"Collisions between {hour}:00 and {hour + 1}:00")
st.map(data_test[['latitude', 'longitude']].dropna(how="any"))

st.markdown("Vehicle collisions by hour between %i:00 and %i:00" % (hour, (hour + 1) % 24))

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": np.average(data_test['latitude']), # OR midpoint[0]
        "longitude": np.average(data_test['longitude']), # OR midpoint[1]
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=data_test[['date/time', 'latitude', 'longitude']],
            get_position=["longitude", "latitude"],
            radius=100,
            extruded=True,
            pickable=True,
            elevation_scale=4,
            elevation_range=[0, 1000],
        ),
    ],
))

# Using Plotly
st.subheader('Breakdown by minute between %i:00 and %i:00' % (hour, (hour + 1) % 24))
filtered = data_test[
    (data_test['date/time'].dt.hour >= hour) & (data_test['date/time'].dt.hour < (hour + 1))
]
hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({'minute': range(60), 'crashes': hist})
fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)
st.write(fig)

# Select data using dropdowns
st.header("Top 5 dangerous streets by affected type")
select = st.selectbox('Affected type of people', ['Pedestrians', 'Cyclists', 'Motorists'])
if select == 'Pedestrians':
    st.write(original_data.query("injured_pedestrians >= 1")[['on_street_name', 'injured_pedestrians']].sort_values(by=['injured_pedestrians'],
                                                                                                                    ascending=False).dropna(how="any")[:5])
elif select == 'Cyclists':
    st.write(original_data.query("injured_cyclists >= 1")[['on_street_name', 'injured_cyclists']].sort_values(by=['injured_cyclists'],
                                                                                                              ascending=False).dropna(how="any")[:5])
else:
    st.write(original_data.query("injured_motorists >= 1")[['on_street_name', 'injured_motorists']].sort_values(by=['injured_motorists'],
                                                                                                                ascending=False).dropna(how="any")[:5])


# Show data
if st.checkbox("Show Raw Data", False):
    st.subheader('Raw Data')
    st.write(data_test)

