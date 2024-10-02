import requests
import streamlit as st
from openai import OpenAI

# Set up the Streamlit app
st.title("Weather Suggestion Bot with OpenAI")

# Function to fetch current weather information from OpenWeather API
def fetch_weather_data(city, api_key):
    # Clean the input city name
    city = city.split(",")[0].strip() if "," in city else city.strip()

    base_url = "https://api.openweathermap.org/data/2.5/"
    endpoint = f"weather?q={city}&appid={api_key}"
    full_url = base_url + endpoint

    response = requests.get(full_url)
    weather_info = response.json()

    if response.status_code != 200:
        st.error("Unable to retrieve weather data. Please verify the city name.")
        return None

    # Convert temperature from Kelvin to Celsius
    main_data = weather_info['main']
    return {
        "city": city,
        "temperature": round(main_data['temp'] - 273.15, 2),
        "feels_like": round(main_data['feels_like'] - 273.15, 2),
        "min_temp": round(main_data['temp_min'] - 273.15, 2),
        "max_temp": round(main_data['temp_max'] - 273.15, 2),
        "humidity": round(main_data['humidity'], 2)
    }

# Initialize OpenAI API client
def initialize_openai_client():
    return OpenAI(api_key=st.secrets["open_api_key"])

# Create a response from the OpenAI chatbot
def create_chatbot_response(user_input, weather_info):
    client = initialize_openai_client()

    # Create a context-rich message
    context = [
        {"role": "system", "content": f"The weather in {weather_info['city']} is:\n"
                                      f"Temperature: {weather_info['temperature']}°C\n"
                                      f"Feels Like: {weather_info['feels_like']}°C\n"
                                      f"Min Temperature: {weather_info['min_temp']}°C\n"
                                      f"Max Temperature: {weather_info['max_temp']}°C\n"
                                      f"Humidity: {weather_info['humidity']}%"},
        {"role": "user", "content": user_input}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=context
    )

    return response.choices[0].message.content

# User input for city name
city_input = st.text_input("Enter a city (e.g., London, England):", "London, England")

if city_input:
    weather_info = fetch_weather_data(city_input, st.secrets["weather_api_key"])

    if weather_info:
        st.write("### Current Weather Details:")
        st.write(weather_info)

        # User question for the chatbot
        user_query = st.text_area("Ask about the weather (e.g., What should I wear?):", "What should I wear today?")

        if user_query:
            with st.spinner("Generating a response..."):
                chatbot_reply = create_chatbot_response(user_query, weather_info)
                st.write("### Chatbot Response:")
                st.write(chatbot_reply)
