# AI-WEATHER-APP
# AI Weather App - Agricultural Intelligence System

> An intelligent weather analysis application that combines real-time weather data with AI-powered crop recommendations and agricultural insights for farmers and agricultural professionals.

## 🌟 Features

### 🌤️ Weather Intelligence
- **Real-time Weather Data** - Current conditions including temperature, humidity, wind speed, and atmospheric pressure using OpenWeatherMap API[1]
- **Location-based Analysis** - Weather information based on coordinates from Google Maps Geocoding API[1]
- **Soil Moisture Monitoring** - Real-time soil moisture data using Open-Meteo API[1]
- **Multi-parameter Analysis** - Comprehensive environmental data for informed decision-making[1]

### 🤖 AI-Powered Agricultural Insights
- **Intelligent Crop Recommendations** - AI suggests suitable crops based on current weather and soil conditions[1]
- **Agricultural Input Guidance** - Recommendations for pesticides, fertilizers, weedicides, and natural alternatives[1]
- **Natural Language Processing** - Conversational interface using Groq's Llama-3.3-70b model[1]
- **Structured Analysis** - Formatted weather analysis with key insights and actionable recommendations[1]

### 📱 User Interface
- **Streamlit Web App** - Clean, intuitive interface with real-time data visualization[1]
- **Interactive Chat History** - Track previous analyses and recommendations[1]
- **Downloadable Reports** - Export weather analysis reports as text files[1]
- **Responsive Design** - Works seamlessly across devices[1]

## 🛠️ Technology Stack

| Category | Technologies |
|----------|-------------|
| **Frontend** | Streamlit, Python |
| **Weather APIs** | OpenWeatherMap API|
| **Geolocation** | Google Maps Geocoding API |
| **AI/LLM** | Groq API (Llama-3.3-70b-Versatile) |
| **Data Processing** | LangChain, Python |
| **Environment** | Python-dotenv for configuration |

## 📋 Prerequisites

- Python 3.8 or higher
- API keys for:
  - OpenWeatherMap API
  - Google Maps Geocoding API  
  - Groq API
- Required Python packages (see requirements.txt)[1]

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/josondev/AI-WEATHER-APP.git
cd AI-WEATHER-APP/SRC
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the SRC directory with your API keys:
```env
google_maps_token=your_google_maps_api_key
openweather_api_key=your_openweathermap_api_key
GROQ_API_KEY=your_groq_api_key
```

### 4. Run the Application

**Full Deployed App :**
```
https://ai-weather-app-01.streamlit.app/
```
**Streamlit Web App :**
```bash
streamlit run streamlit_app.py
```

**Command Line Interface:**
```bash
python test.py
```

**Basic Weather Testing:**
```bash
python weather.py
```

## 📁 Project Structure

```
SRC/
├── final_app.py          # Main Streamlit web application
├── test.py              # Command-line interface version  
├── weather.py           # Core weather data fetching functions
├── requirements.txt     # Python dependencies
└── .env                # Environment variables (create this)
```

## 💡 Usage Guide

### Web Application Interface

1. **Launch the App**: Run `streamlit run final_app.py`
2. **Enter Location**: Type any city name or address
3. **Get Analysis**: Click "Analyze Weather" for comprehensive insights
4. **View Results**: See structured weather analysis, crop recommendations, and agricultural inputs
5. **Download Reports**: Export analysis as text files for future reference

### Key Features Explained

- **Weather Analysis**: Detailed breakdown of current conditions and their implications
- **Temperature Insights**: Analysis of actual vs. feels-like temperatures
- **Humidity Impact**: Understanding moisture levels and their effects on agriculture
- **Wind Conditions**: Assessment of wind speed and environmental impact
- **Soil Moisture**: Critical data for irrigation and planting decisions
- **Crop Suggestions**: AI-recommended crops suitable for current conditions
- **Agricultural Inputs**: Specific recommendations for pesticides, fertilizers, and natural alternatives

## 🔧 Core Functions

### Weather Data Retrieval
- `get_coordinates(address, api_key)` - Convert location to GPS coordinates[1]
- `get_weather(lat, lon, api_key)` - Fetch comprehensive weather data[1]  
- `get_soil_moisture(lat, lon)` - Retrieve soil moisture information[1]

### AI Analysis
- Processes weather data through advanced language models[1]
- Generates contextual agricultural recommendations[1]
- Provides structured output with key-value summaries[1]

## 📊 Sample Output

The application provides structured analysis including:

- **Current Conditions**: Weather description and implications
- **Temperature Analysis**: Detailed temperature breakdown
- **Environmental Factors**: Humidity, wind, and soil conditions  
- **Agricultural Recommendations**: Suitable crops and farming inputs
- **Key Metrics Summary**: Quick reference data table

## 🤝 Contributing

We welcome contributions to improve this agricultural intelligence system:

### Development Guidelines
- Follow existing code structure and commenting standards[1]
- Test thoroughly with different locations and weather conditions
- Update documentation for new features
- Ensure API rate limits are respected

### Areas for Enhancement
- Additional weather parameters integration
- Expanded crop database
- Historical weather data analysis
- Multi-language support for global use

## 📄 API Usage & Limits

- **OpenWeatherMap**: Weather data with standard rate limits
- **Google Maps**: Geocoding with generous free tier
- **Groq**: AI processing with API key authentication
- **Open-Meteo**: Soil moisture data (free service)

## 🔐 Security Notes

- Store API keys securely in `.env` file[1]
- Never commit API keys to version control
- Use environment variables for production deployment
- Monitor API usage to avoid rate limit violations

## 📞 Support & Contact

- **GitHub Repository**: [josondev/AI-WEATHER-APP](https://github.com/josondev/AI-WEATHER-APP)
- **Issues**: Report bugs and request features via GitHub Issues
- **Developers**: [@josondev](https://github.com/josondev)][@<0xethjayadithya_g7dev/>](https://github.com/jayadithya-g7)]

## 🙏 Acknowledgments

- OpenWeatherMap for reliable weather data APIs
- Google Maps for accurate geocoding services  
- Groq for advanced AI language model access
- Open-Meteo for comprehensive soil moisture data
- Streamlit for rapid web application development
