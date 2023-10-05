from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low
from messages import TemperatureRequest, TemperatureResponse
from ast import Tuple
import os
import requests
import json
import http

def get_weather_data(city):
    conn = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")

    headers = {
    'X-RapidAPI-Key': "f059d8455amsh4b068c5adade5bep1d646ajsn754b5adadb37",
    'X-RapidAPI-Host': "weatherapi-com.p.rapidapi.com"
}

    conn.request("GET", "/current.json?q=Nasik", headers=headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")

# Creating the agent and funding it if needed
agent = Agent(
    name="timAgent",
    seed="temperature_alert_agent"
)

#fund_agent_if_low(agent.wallet.address)

#Function to log the request information
async def log_request(ctx: Context, sender: str, request: TemperatureRequest):
    ctx.logger.info(f"Got request from {sender} for temperature of : {request.location}")

#Function to fetch cuerrent temperature for specified lcation
def fetch_temperature(ctx: Context, sender: str, request: TemperatureRequest):

    current_temp = json.loads(get_weather_data(requests.location))["current"]["temp_c"]

    # Extract the current temperature from the response.
    current_temperature = temperature_response["main"]["temp"]

    return current_temperature

#Function to check if the current temperature is outside of the user's preferred range.
async def check_temp_range(ctx: Context, sender: str) -> Tuple[float, float]:
    # Prompt the user to enter their preferred minimum temperature.
  await ctx.send(sender, "Enter your preferred minimum temperature: ")
  min_temp_str = await ctx.receive(sender)

  # Prompt the user to enter their preferred maximum temperature.
  await ctx.send(sender, "Enter your preferred maximum temperature: ")
  max_temp_str = await ctx.receive(sender)

  # Convert the temperature strings to floats.
  min_temp = float(min_temp_str)
  max_temp = float(max_temp_str)

  return min_temp, max_temp

@agent.on_interval(period=120)
async def fetch_weather_data(ctx: Context):
    data = json.loads(get_weather_data("Nasik"))
    curr_temp = data['current']['temp_c']
    ctx.logger.info(f'Temperature: {curr_temp}')

# Message handler for temperature alert requests'
@agent.on_message(model=TemperatureRequest)
async def handle_temperature_alert_request(ctx: Context, sender: str, request: TemperatureRequest):
  # Prompt the user to enter their preferred temperature range.
  min_temp, max_temp = await check_temp_range(ctx, sender)

  # Fetch the current temperature for the specified location.
  current_temperature = await fetch_temperature(ctx, sender, request)

  # If the temperature is outside of the user's preferred range, send them a message.
  if current_temperature is not None:
    if current_temperature > max_temp:
      ctx.send(sender, f"The temperature in {request.location} is above your preferred maximum of {max_temp} degrees Celsius.")
    elif current_temperature < min_temp:
      ctx.send(sender, f"The temperature in {request.location} is below your preferred minimum of {min_temp} degrees Celsius.")


# Getting location of the user to calculate the temperature
def Location ( ) :

    response = requests.get("https://ipinfo.io") # getting user location using ipinfo API

    if response.status_code == 200 :

        data = response.json( )
        
        lat = data.get("loc").split(',')[0]
        lon = data.get("loc").split(',')[1]

        global region 
        region = data.get('region') 
        
        return lat , lon 

    else :  
        return None , None


# Humidity suggestions structure
def Humidity_Suggestions ( humidity , ctx : Context ) :

    if humidity < 10 :

        ctx.logger.info (f"At {humidity}% Humidity: Extremely dry conditions. Consider using moisturizer and staying hydrated.")

    elif humidity < 20 :

        ctx.logger.info (f"At {humidity}% Humidity: Very dry conditions. Lips and throat may feel dry. Consider using a humidifier indoors.")

    elif humidity < 30 :

        ctx.logger.info (f"At {humidity}% Humidity: Dry conditions. Moisturizing may help.")

    elif humidity < 40 :

        ctx.logger.info (f"At {humidity}% Humidity: Moderate humidity level. Comfortable for many")

    elif humidity < 50: 

        ctx.logger.info(f"At {humidity}% Humidity: Generally suitable for everyone.")

    elif humidity < 60 :
            
        ctx.logger.info (f"At {humidity}% Humidity: Mildly humid conditions.")

    elif humidity < 70: 

        ctx.logger.info (f"At {humidity}% Humidity: Noticeably humid. May feel muggy.")        

    elif humidity < 80 :
            
        ctx.logger.info (f"At {humidity}% Humidity: Humid conditions. Consider using fans for comfort.")

    elif humidity < 90 :
            
        ctx.logger.info (f"At {humidity}% Humidity: Very humid conditions. Use fans and stay cool.")

    else :

        ctx.logger.info(f"At {humidity}% Humidity: Fully saturated air. Very uncomfortable.")


# Display the Information in structured manner 
def Display ( ctx : Context ) :

    current_weather = {

    'Clear': 'Clear sky',
    'Clouds': 'Cloudy',
    'Rain': 'Rainy',
    'Drizzle': 'Drizzling',
    'Thunderstorm': 'Thunderstorms',
    'Snow': 'Snowy',
    'Mist': 'Misty',

    }

    os.system('cls')
    ctx.logger.info (f"Region: {region}")
    ctx.logger.info (f"Temperature: {celsius}")
    ctx.logger.info (f"Weather Status: {current_weather[main]}")
    
    ctx.logger.info(f"Temperature feels like it is - {feelsC}")
    Humidity_Suggestions(humidity)
    ctx.logger.info (f"Weather Description: {description}")


lat , lon = Location ( ) 

if ( lat != None or lon != None ) : # returned values should not be None

    API_KEY = "030a8d86c227cbd62f1b8d541a283b38"
    API_URL = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"

    response = requests.get(API_URL) # OpenWeatherMap API to get the temperature as per the latitude and longitude 

if response.status_code == 200 :
    
    data = response.json( ) # Converting the API response to json object

    # Extracting specific data from the response object
    main = data.get('weather')[0]['main']

    kelvin = data.get('main').get("temp") # object contains Temperature in kelvin units
    temperature_response , celsius = str(round ( kelvin - 273.15 , 2 )) + "°C" # 273.15°K = 0°C

    feelsK = data.get('main').get('feels_like') 
    feelsC = str( round ( feelsK - 273.15 , 2 )) + "°C" 
    
    humidity = data.get('main').get('humidity')

    description =  data.get('weather')[0]['description']

Display ( ) 

if __name__ == "__main__":
    agent.run()
