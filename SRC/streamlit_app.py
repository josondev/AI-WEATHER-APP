import streamlit as st
from weather import get_weather, get_coordinates, get_soil_moisture
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Weather & Farmer Helper",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    .stButton>button {
        width: 100%;
        background-color: #667eea;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #764ba2;
    }
    </style>
""", unsafe_allow_html=True)

# Load environment variables
load_dotenv()

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = ChatMessageHistory()
    if 'last_analysis' not in st.session_state:
        st.session_state.last_analysis = None
    if 'analysis_timestamp' not in st.session_state:
        st.session_state.analysis_timestamp = None

init_session_state()

# Initialize LLM
@st.cache_resource
def get_llm():
    """Initialize and cache the language model"""
    return ChatGroq(
        model="Llama-3.3-70b-Versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3
    )

llm = get_llm()

# Enhanced prompt template
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an expert agricultural and weather analysis assistant. Your role is to provide actionable insights for farmers.

**IMPORTANT**: Only respond to weather and agriculture-related queries. For other topics, politely redirect users.

Structure your response as follows:

### 🌤️ Weather Analysis for {location}

#### 📍 Location Information
{coordinates}

#### 🌡️ Current Conditions
**Description:** {description}
**Temperature:** {temp}°C (Feels like: {feels_like}°C)
**Humidity:** {humidity}%
**Wind Speed:** {wind_speed} m/s
**Soil Moisture:** {soil_moisture}

#### 📊 Detailed Analysis

**Temperature Impact:**
- Analyze the temperature range and its suitability for different crops
- Consider the "feels like" temperature for outdoor work conditions

**Humidity Assessment:**
- Evaluate humidity levels and their implications for plant growth
- Discuss disease risk based on moisture levels

**Wind Conditions:**
- Assess wind speed effects on crops and farming operations
- Consider pollination and spray application conditions

**Soil Moisture Analysis:**
- Interpret soil moisture data for irrigation planning
- Recommend water management strategies

#### 🌾 Crop Recommendations

Based on current conditions, recommend suitable crops with specific rationale.

#### 🧪 Agricultural Inputs

```plaintext
PESTICIDES:
Chemical Options:
  • [List specific pesticides with application rates]

Natural Alternatives:
  • [List organic/natural pest control methods]

FERTILIZERS:
Chemical Options:
  • [List NPK ratios and specific fertilizers]

Organic Alternatives:
  • [List compost, manure, and natural fertilizer options]

WEEDICIDES:
Chemical Options:
  • [List selective and non-selective herbicides]

Natural Alternatives:
  • [List mulching, manual, and organic weed control methods]
```

#### ⚠️ Recommendations & Precautions
- List specific actions farmers should take
- Include timing recommendations
- Safety considerations

---
*Analysis generated at {timestamp}*
"""
    ),
    (
        "human",
        """Analyze weather conditions for {location}.

Location: {coordinates}
Weather Data: {weather_info}
Soil Conditions: {soil_moisture}

Provide comprehensive agricultural guidance based on this data."""
    ),
    MessagesPlaceholder(variable_name="chat_history"),
])

chain = prompt | llm | StrOutputParser()

def parse_weather_data(weather_str):
    """Parse weather information string into structured data"""
    weather_data = {}
    try:
        for line in weather_str.split('\n'):
            if "Description:" in line:
                weather_data['description'] = line.split(': ', 1)[1].strip()
            elif "Temperature:" in line:
                weather_data['temp'] = float(line.split(': ')[1].replace('°C', '').strip())
            elif "Feels like:" in line:
                weather_data['feels_like'] = float(line.split(': ')[1].replace('°C', '').strip())
            elif "Humidity:" in line:
                weather_data['humidity'] = int(line.split(': ')[1].replace('%', '').strip())
            elif "Wind speed:" in line:
                weather_data['wind_speed'] = float(line.split(': ')[1].replace(' m/s', '').strip())
    except Exception as e:
        st.error(f"Error parsing weather data: {str(e)}")
    return weather_data

def process_weather_query(location):
    """Process weather data for a given location"""
    try:
        google_maps_token = os.getenv("google_maps_token")
        openweather_api_key = os.getenv("openweather_api_key")

        if not google_maps_token or not openweather_api_key:
            return "⚠️ API keys not found. Please check your .env file."

        # Get coordinates
        coordinates = get_coordinates(location, google_maps_token)
        if not coordinates:
            return f"❌ Could not find coordinates for '{location}'. Please check the location name."

        # Get weather data
        weather_info_str = get_weather(coordinates[0], coordinates[1], openweather_api_key)
        weather_data = parse_weather_data(weather_info_str)

        if not weather_data:
            return "❌ Failed to retrieve weather data. Please try again."

        # Get soil moisture
        soil_moisture = get_soil_moisture(coordinates[0], coordinates[1])

        return {
            "location": location,
            "coordinates": f"Lat: {coordinates[0]:.4f}, Lon: {coordinates[1]:.4f}",
            "description": weather_data.get('description', 'N/A'),
            "temp": weather_data.get('temp', 0),
            "feels_like": weather_data.get('feels_like', 0),
            "humidity": weather_data.get('humidity', 0),
            "wind_speed": weather_data.get('wind_speed', 0),
            "soil_moisture": soil_moisture,
            "weather_info": weather_info_str,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return f"❌ Error: {str(e)}"

def display_weather_metrics(data):
    """Display weather metrics in a clean card layout"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🌡️ Temperature", f"{data['temp']}°C", f"Feels like {data['feels_like']}°C")
    with col2:
        st.metric("💧 Humidity", f"{data['humidity']}%")
    with col3:
        st.metric("💨 Wind Speed", f"{data['wind_speed']} m/s")
    with col4:
        st.metric("🌱 Soil Moisture", data['soil_moisture'])

def display_analysis(response):
    """Display formatted analysis with proper styling"""
    try:
        # Split by main sections
        sections = response.split("###")
        
        for section in sections:
            section = section.strip()
            if not section:
                continue
            
            # Handle code blocks separately
            if "```plaintext" in section:
                parts = section.split("```plaintext")
                for i, part in enumerate(parts):
                    if i == 0 and part.strip():
                        st.markdown(part)
                    elif part.strip():
                        code_content = part.split("```")[0]
                        st.code(code_content.strip(), language="plaintext")
                        remaining = "```".join(part.split("```")[1:])
                        if remaining.strip():
                            st.markdown(remaining)
            else:
                # Display markdown sections
                st.markdown("### " + section)
        
    except Exception as e:
        st.error(f"Error displaying analysis: {str(e)}")
        st.markdown(response)

# Main App Header
st.markdown('<div class="main-header"><h1>🌤️ Weather & Farmer Helper 🌾</h1><p>Real-time Weather Analysis & Agricultural Guidance</p></div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("---")
    
    show_history = st.checkbox("💬 Show Chat History", value=False)
    show_raw_data = st.checkbox("📊 Show Raw Weather Data", value=False)
    
    st.markdown("---")
    st.subheader("ℹ️ About")
    st.info("""
    This app provides:
    - Real-time weather analysis
    - Soil moisture data
    - Crop recommendations
    - Agricultural input guidance
    - Natural alternatives
    """)
    
    if st.button("🗑️ Clear History"):
        st.session_state.chat_history = ChatMessageHistory()
        st.session_state.last_analysis = None
        st.success("History cleared!")

# Main content area
col1, col2 = st.columns([3, 1])

with col1:
    location = st.text_input(
        "📍 Enter Location",
        placeholder="e.g., New York, London, Tokyo, Mumbai",
        help="Enter a city name or region"
    )

with col2:
    st.write("")  # Spacer
    st.write("")  # Spacer
    analyze_button = st.button("🔍 Analyze Weather", type="primary")

# Process analysis
if analyze_button:
    if location:
        with st.spinner("🌐 Fetching weather data and generating analysis..."):
            weather_data = process_weather_query(location)
            
            if isinstance(weather_data, dict):
                # Display weather metrics
                st.subheader(f"📊 Current Weather - {weather_data['location']}")
                display_weather_metrics(weather_data)
                
                if show_raw_data:
                    with st.expander("📋 Raw Weather Data"):
                        st.code(weather_data['weather_info'], language="plaintext")
                
                st.markdown("---")
                
                try:
                    # Generate analysis
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
                        "timestamp": weather_data["timestamp"],
                        "chat_history": st.session_state.chat_history.messages
                    })
                    
                    # Save to chat history
                    st.session_state.chat_history.add_user_message(f"Analyze weather for {location}")
                    st.session_state.chat_history.add_ai_message(response)
                    st.session_state.last_analysis = response
                    st.session_state.analysis_timestamp = weather_data["timestamp"]
                    
                    # Display analysis
                    display_analysis(response)
                    
                    # Download button
                    col1, col2, col3 = st.columns([1, 1, 2])
                    with col1:
                        st.download_button(
                            "📥 Download Report",
                            response,
                            file_name=f"weather_analysis_{location.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    
                except Exception as e:
                    st.error(f"❌ Error generating analysis: {str(e)}")
                    st.exception(e)
            else:
                st.error(weather_data)
    else:
        st.warning("⚠️ Please enter a location to analyze.")

# Chat history display
if show_history and len(st.session_state.chat_history.messages) > 0:
    st.markdown("---")
    st.subheader("💬 Conversation History")
    
    for i, message in enumerate(st.session_state.chat_history.messages):
        if isinstance(message, HumanMessage):
            st.info(f"👤 **You:** {message.content}")
        elif isinstance(message, AIMessage):
            with st.expander(f"🤖 Analysis #{i//2 + 1}", expanded=(i == len(st.session_state.chat_history.messages) - 1)):
                display_analysis(message.content)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 1rem;'>
    <p>🌾 Weather & Farmer Helper | Powered by OpenWeather, Google Maps & Groq AI</p>
    <p style='font-size: 0.8rem;'>For agricultural guidance only. Consult local experts for critical decisions.</p>
</div>
""", unsafe_allow_html=True)
