import streamlit as st
from weather import get_weather, get_coordinates, get_soil_moisture
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Groq model name and API key
llm = ChatGroq(model="Llama-3.3-70b-Versatile", api_key=os.getenv("GROQ_API_KEY"))

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory()

# Update the prompt template to ensure structured output
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a weather analysis assistant that provides detailed insights using real-time weather data.
        Focus STRICTLY on the data provided and avoid any assumptions or generalizations.
        
        Structure your response in the following format:
        
        ### Weather Analysis for {location}
        
        #### 1. Current Weather Conditions and Description
        - Description and implications
        
        #### 2. Temperature Analysis
        - Actual Temperature details
        - Feels Like Temperature analysis
        - Implications
        
        #### 3. Humidity Levels and Implications
        - Humidity percentage
        - Impact analysis
        
        #### 4. Wind Speed and Its Effects
        - Wind speed measurements
        - Effects on environment
        
        #### 5. Soil Moisture Analysis
        - Soil moisture levels
        - Agricultural implications
        
        ### Crop Recommendations
        List suitable crops based on conditions
        
        ```plaintext
        Agricultural Inputs:
        - Pesticides:
          * Chemical options
          * Natural alternatives
        - Fertilizers:
          * Chemical options
          * Natural alternatives
        - Weedicides:
          * Chemical options
          * Natural alternatives
        ```
        
        ```plaintext
        Key-Value Summary:
        Location: {coordinates}
        Weather: {description}
        Temperature: {temp}°C
        Feels Like: {feels_like}°C
        Humidity: {humidity}%
        Wind Speed: {wind_speed} m/s
        Soil Moisture: {soil_moisture}
        ```"""
    ),
    (
        "human",
        """Analyze the following weather data for {location}:
        
        Location Details:
        {coordinates}
        
        Weather Information:
        {weather_info}
        
        Soil Conditions:
        {soil_moisture}"""
    ),
    MessagesPlaceholder(variable_name="chat_history"),
])

chain = prompt | llm | StrOutputParser()

# Update the process_weather_query function to parse weather info correctly
def process_weather_query(location):
    """Process weather data for a given location with proper weather info parsing"""
    try:
        # Get API keys from environment variables
        google_maps_token = os.getenv("google_maps_token")
        openweather_api_key = os.getenv("openweather_api_key")

        # Get coordinates
        coordinates = get_coordinates(location, google_maps_token)
        if not coordinates:
            return "Could not get coordinates for this location."

        # Get weather data as string
        weather_info_str = get_weather(coordinates[0], coordinates[1], openweather_api_key)
        
        # Parse weather info string into components
        weather_data = {}
        for line in weather_info_str.split('\n'):
            if "Description:" in line:
                weather_data['description'] = line.split(': ')[1].strip()
            elif "Temperature:" in line:
                weather_data['temp'] = float(line.split(': ')[1].replace('°C', ''))
            elif "Feels like:" in line:
                weather_data['feels_like'] = float(line.split(': ')[1].replace('°C', ''))
            elif "Humidity:" in line:
                weather_data['humidity'] = int(line.split(': ')[1].replace('%', ''))
            elif "Wind speed:" in line:
                weather_data['wind_speed'] = float(line.split(': ')[1].replace(' m/s', ''))

        # Get soil moisture
        soil_moisture = get_soil_moisture(coordinates[0], coordinates[1])

        return {
            "location": location,
            "coordinates": f"({coordinates[0]}, {coordinates[1]})",
            "description": weather_data['description'],
            "temp": weather_data['temp'],
            "feels_like": weather_data['feels_like'],
            "humidity": weather_data['humidity'],
            "wind_speed": weather_data['wind_speed'],
            "soil_moisture": soil_moisture,
            "weather_info": weather_info_str  # Keep original string for display
        }
    except Exception as e:
        return f"Error processing weather data: {str(e)}"

# Streamlit app
st.title("Weather + Farmer Helper")

# User input for location
location = st.text_input("Enter location:")

def display_analysis(response):
    """Format and display the analysis with proper styling"""
    try:
        # Display Key-Value Summary first if present
        if "Key-Value Summary:" in response:
            summary_section = response.split("Key-Value Summary:")[1].split("```")[0]
            st.markdown("### 📊 Key-Value Summary")
            st.code(summary_section.strip(), language="plaintext")
        
        # Split sections for remaining content
        sections = response.split("###")
        
        for section in sections:
            if section.strip():
                # Skip Key-Value Summary as it's already displayed
                if "Key-Value Summary:" not in section:
                    # Main title
                    if "Weather Analysis" in section:
                        st.markdown(f"### {section.splitlines()[0].strip()}")
                        
                        # Display subsections
                        for subsection in section.split("####"):
                            if subsection.strip():
                                st.markdown(f"#### {subsection.strip()}")
                    
                    # Crop recommendations
                    elif "Crop Recommendations" in section:
                        st.markdown(f"### {section.splitlines()[0].strip()}")
                        remaining_lines = "\n".join(section.splitlines()[1:])
                        st.markdown(remaining_lines)
                    
                    # Code blocks
                    elif "```plaintext" in section:
                        code_blocks = section.split("```plaintext")
                        for block in code_blocks:
                            if block.strip():
                                st.code(block.strip(), language="plaintext")
                    
                    else:
                        st.markdown(section)
                    
    except Exception as e:
        st.error(f"Error formatting analysis: {str(e)}")
        st.write(response)  # Fallback to raw display

# Update the main app section
if st.button("Analyze Weather"):
    if location:
        with st.spinner("Analyzing weather data..."):
            weather_data = process_weather_query(location)
            
            if isinstance(weather_data, dict):
                try:
                    # Get analysis from model with all required variables
                    response = chain.invoke({
                        "location": weather_data["location"],
                        "coordinates": weather_data["coordinates"],
                        "description": weather_data["description"],
                        "temp": weather_data["temp"],
                        "feels_like": weather_data["feels_like"],
                        "humidity": weather_data["humidity"],
                        "wind_speed": weather_data["wind_speed"],
                        "soil_moisture": weather_data["soil_moisture"],
                        "weather_info": weather_data["weather_info"],
                        "chat_history": st.session_state.chat_history.messages
                    })
                    
                    # Rest of the code remains the same
                    st.session_state.chat_history.add_user_message(
                        f"Analyze weather for {location}")
                    st.session_state.chat_history.add_ai_message(response)
                    
                    display_analysis(response)
                    
                    st.download_button(
                        "📥 Download Analysis",
                        response,
                        file_name=f"weather_analysis_{location}.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"Error analyzing weather data: {str(e)}")
            else:
                st.error(weather_data)
    else:
        st.warning("Please enter a location.")

# Update chat history display
if st.checkbox("Show Chat History"):
    st.subheader("💬 Chat History")
    for message in st.session_state.chat_history.messages:
        if isinstance(message, HumanMessage):
            st.info(f"👤 User: {message.content}")
        elif isinstance(message, AIMessage):
            with st.expander("🤖 AI Response", expanded=True):
                display_analysis(message.content)
