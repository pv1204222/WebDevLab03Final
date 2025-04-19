import streamlit as st
import google.generativeai as genai

#LLM config
genai.configure(api_key=st.secrets["gemini"]["api_key"])

#Headers and prompt
st.title("Gemini Travel Advisor")
st.write("Enter a certain aspect for each city that you want compared! (ex. safety, activities, weather, etc...) Help Decide your dream destination!")

city1 = st.session_state.get("city1")
city2 = st.session_state.get("city2")
if not city1 or not city2:
    st.warning("Please enter and compare cities on the weather comparison page first.")
    st.stop()

#Set up Chatbot
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

#Input and prompt
user_in = st.chat_input("Ask about safety, activities, weather, etc...")
if user_in:
    st.session_state.chat_history.append({"role": "user", "content": user_in})
    with st.chat_message("user"):
        st.markdown(user_in)
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        history = ""
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                history += f"User: {msg['content']}\n"
            else:
                history += f"Gemini: {msg['content']}\n"
        prompt = f"""
                Pretend you are a helpful travel advisor. The user is comparing two cities: {city1} and {city2}.
                They will ask questions about aspects of the cities such as safety, nature, activities, weather, etc...
                Give friendly, practical comparisons.
                {history}
                User: {user_in}
                Gemini:
                """
        response = model.generate_content(prompt)
        reply = response.text
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
            
    except Exception as e:
        st.error("⚠️ Gemini could not generate a response.")
        st.code(str(e))