from weather import get_weather,get_coordinates,get_soil_moisture
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()

# Groq model name and API key
llm=ChatGroq(model="Llama-3.3-70b-Versatile",api_key=os.getenv("GROQ_API_KEY"))
chat_history=ChatMessageHistory()

# prompt template to make sure the model is able to understand the data and provide a detailed analysis of the weather data
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a weather analysis assistant that provides detailed insights using real-time weather data.
        Focus STRICTLY on the data provided and avoid any assumptions or generalizations. Do not answer any other questions.POLITELY REDIRECT THOSE QUESTIONS.        Analyze the following aspects:
        1. Current weather conditions and description
        2. Temperature analysis (actual vs feels like)
        3. Humidity levels and implications
        4. Wind speed and its effects
        5. Soil moisture conditions and agricultural implications
        
        Provide specific analysis based on the provided weather data.
        AFTER THE ANALYSIS, I want you to recomend all food crops that can be grown in this location based on the data provided.
        ADDITIONALLY,FOR THE CROPS YOU SUGGEST,I want you to provide the PESTICIDES,FERTILISERS,WEEDICIDES AND THE NATURAL HERBICIDE ALTERNATIVES
        IN THE FORM OF TEXTBOX.FOR OTHER CASES,I WANT YOU TO PRESENT THE OUTPUT IN A KEY VALUE FORMAT
        """
    ),
    (
        "human",
        """Analyze the following weather data for {location}:
        
        Location Details:
        {coordinates}
        
        Weather Information:
        {weather_info}
        
        Soil Conditions:
        {soil_moisture}
        
        Please provide a comprehensive analysis of these conditions."""
    ),
    MessagesPlaceholder(variable_name="chat_history"),
])

chain=prompt | llm | StrOutputParser()


# In a new cell, add this function to process location and weather data
def process_weather_query(location):
    """Process weather data for a given location"""
    try:
        # Get API keys from environment variables
        google_maps_token = os.getenv("google_maps_token")
        openweather_api_key = os.getenv("openweather_api_key")
        
        # Get coordinates
        coordinates = get_coordinates(location, google_maps_token)
        if not coordinates:
            return "Could not get coordinates for this location."
            
        # Get weather data
        weather_info = get_weather(coordinates[0], coordinates[1], openweather_api_key)
        
        # Get soil moisture
        soil_moisture = get_soil_moisture(coordinates[0], coordinates[1])
        
        return {
            "location": location,
            "coordinates": f"({coordinates[0]}, {coordinates[1]})",
            "weather_info": weather_info,
            "soil_moisture": soil_moisture
        }
    except Exception as e:
        return f"Error processing weather data: {str(e)}"

#the main interaction loop
flag = True
while(flag):
    # Get location from user
    location = input("Enter location (or 'exit' to quit): ")
    if location.lower() == 'exit':
        break
    # Get coordinates for the location
    latitude, longitude = get_coordinates(location, os.getenv("google_maps_token"))
    print(f"Coordinates for '{location}': Latitude {latitude}, Longitude {longitude}")
    
    # Get the weather data using the coordinates
    weather_info = get_weather(latitude, longitude, os.getenv("openweather_api_key"))
    print(weather_info)
    
    # Get the soil moisture data using the coordinates
    soil_moisture_info = get_soil_moisture(latitude, longitude)
    print(soil_moisture_info)
    # Process weather data
    weather_data = process_weather_query(location)

    if isinstance(weather_data, dict):
        # If weather data was successfully retrieved
        try:
            # Invoke the model with weather data
            response = chain.invoke({
                "location": weather_data["location"],
                "coordinates": weather_data["coordinates"],
                "weather_info": weather_data["weather_info"],
                "soil_moisture": weather_data["soil_moisture"],
                "chat_history": chat_history.messages
            })
            
            # Add interaction to chat history
            chat_history.add_user_message(f"Analyze weather for {location}")
            chat_history.add_ai_message(response)
            
            # Print response
            print("\nAnalysis:")
            print(response)
            
        except Exception as e:
            print(f"Error analyzing weather data: {str(e)}")
    else:
        # If there was an error getting weather data
        print(weather_data)  # Print error message

    # Ask to continue
    answer = input("\nDo you want to check another location? (yes/no): ")
    if answer.lower() == "no":
        for message in chat_history.messages:
            if isinstance(message, HumanMessage):
                print(f"User said: {message.content}")
            elif isinstance(message, AIMessage):
                print(f"AI responded: {message.content}")
        flag = False
