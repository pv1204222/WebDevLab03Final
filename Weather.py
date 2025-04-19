import streamlit as st
import requests
import pandas as pd

input = st.sidebar.text_input("Enter your name:", placeholder ="Type your name here...") #New
if input:
    st.title(f"{input}'s Weather Forecast")
else:
    st.title("🌤️Weather Forecast")
st.write("Welcome to a weather app using Open Meteo API where you can input your whereabouts and recieve an accurate weather report.")

st.sidebar.header("Instructions")
st.sidebar.write("""
1. Type in your name to personlize the page!
2. Enter a location using longitude and latitude and click enter
3. View the week's forecast
""")

url = "https://api.open-meteo.com/v1/forecast" 

st.header("Enter Location📍")
lat = st.number_input("Latitude:", value=33.7501, step=0.5)  
long = st.number_input("Longitude:", value= -84.3885, step=0.5) #New

st.header("Weekly Weather")
information = {
    "latitude": lat,
    "longitude": long,
    "daily": ["temperature_2m_max", "temperature_2m_min"],
    "timezone": "auto"
}
response = requests.get(url, params = information)
weatherF = pd.DataFrame()

if response.status_code == 200:
    data = response.json().get("daily")
    if data:
        maximum = data["temperature_2m_max"]
        minimum = data["temperature_2m_min"]
        dates = data["time"]

        weatherF = pd.DataFrame({
            "Max Temperature(C°)": maximum,
            "Min Temperature(C°)": minimum,
            "Date": dates
        })
        st.dataframe(weatherF) #NEW
    else:
        st.warning("Data not found. Try again") #NEW
else:
    st.error("Error, try again") #NEW

st.header("Temperature Graph")
if not weatherF.empty:
    st.line_chart(weatherF.set_index("Date")) 
else:
    st.info("Data not found.") 