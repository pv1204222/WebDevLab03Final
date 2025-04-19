import streamlit as st
import requests
import pandas as pd
import google.generativeai as genai

#LLM configuration
genai.configure(api_key=st.secrets["gemini"]["api_key"])

#Header and prompt
st.title("Gemini Forecast Comparison!")
st.write("Please enter two different cities! Using our API it will present a weather graph and forecast with Gemini as a weatherman!")
city1 = st.text_input("Enter City #1:", key = "input_city1")
city2 = st.text_input("Enter City #2:", key = "input_city2")
citya = city1
cityb = city2
if city1 and city2:
    st.session_state["city1"] = city1
    st.session_state["city2"] = city2

#Lat and Lon
def coordinates(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    response = requests.get(url).json()
    try:
        return response["results"][0]["latitude"], response["results"][0]["longitude"]
    except:
        return None, None
    
#Weather Data
def weatherData(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max",
        "timezone": "auto"
    }
    response = requests.get(url, params=params).json()
    return response["daily"]["time"], response["daily"]["temperature_2m_max"]

#Main code
if city1 and city2:
    city1 = st.session_state.get("city1")
    city2 = st.session_state.get("city2")
    lat1, lon1 = coordinates(city1)
    lat2, lon2 = coordinates(city2)

    if lat1 and lat2:
            dates1, temps1 = weatherData(lat1, lon1)
            dates2, temps2 = weatherData(lat2, lon2)
            df = pd.DataFrame({
            "Date": dates1,
            f"{city1} Max Temp (°C)": temps1,
            f"{city2} Max Temp (°C)": temps2
            })
            st.subheader("Temperature Forecast 7-Day")
            st.line_chart(df.set_index("Date"))
            st.dataframe(df)
            prompt = f"""
                    Present a 7-day forecast comparison report like a weatherman using {city1} and {city2}.
                    Here is the forecast data:
                    {citya} forecast: {list(zip(dates1, temps1))}
                    {cityb} forecast: {list(zip(dates2, temps2))}
                    Write the script comparing the two cities over the 7 days.
                    Include a summary on which city has the more favorable weather.
                """
            try:
                with st.spinner("Gemini is generating the forecast script..."):
                    model = genai.GenerativeModel("models/gemini-1.5-flash")
                    response = model.generate_content(prompt)
                    st.subheader("🎤 Gemini's Weatherman Forecast")
                    st.write(response.text)
            except Exception as e:
                st.error("Gemini failed to generate a forecast.")
                st.code(str(e))
    else:
        st.error("Could not retrieve coordinates for one or both cities.")