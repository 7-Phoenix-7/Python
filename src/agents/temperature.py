# Import necessary libraries and modules
from uagents import Agent, Context
from messages.alert_msg import Alert
from messages.request import Request
from messages.userpreference_msg import UserPreference
import json
import http

# Import user_agent and API_KEY from related modules (not shown in this code snippet)
from .user import user_agent
from .config import API_KEY

# Creating the TemperatureAlertAgent
temperature_alert_agent = Agent(
    name="TemperatureAlertAgent",
    seed="Temperature Alert Agent"
)

# Function to fetch weather forecast data for a given location
def fetch_weather_data(city):
    conn = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': API_KEY,
        'X-RapidAPI-Host': "weatherapi-com.p.rapidapi.com"
    }

    # Replace whitespaces with underscores in the city name
    city = city.replace(" ", "_")
    conn.request("GET", f'/forecast.json?q={city}&days=1', headers=headers)

    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

# Check weather status every 10 seconds
@temperature_alert_agent.on_interval(period=10)
async def check_weather_status(ctx: Context):
    # Send a request to user_agent
    await ctx.send(user_agent.address, Request(response_address=temperature_alert_agent.address))
    
    # Get the location from the storage
    loc = ctx.storage.get("location")
    
    if loc:
        current_temp, forecasted_temp = retrieve_weather_info(ctx, loc)
        ctx.logger.info(f'Current Temperature: {current_temp}.')
        ctx.logger.info(f'Forecasted Temperature of 24 hrs: {forecasted_temp}')
        await temperature_alert_message(ctx, ctx.storage.get("minTemp"), ctx.storage.get("maxTemp"), current_temp, forecasted_temp)

# Retrieve necessary weather information from fetched data
def retrieve_weather_info(ctx: Context, location):
    while True:
        try:
            data = json.loads(fetch_weather_data(location))
            current_temp = data['current']['temp_c']
            forecasted_temp = data['forecast']['forecastday'][0]['day']['avgtemp_c']
            return current_temp, forecasted_temp
        except KeyError:
            ctx.logger.info("Error getting weather status for the given location. Please check if the location is valid.")
            location = input("Enter Location: ")
            ctx.storage.set("location", location)

# Message handler for temperature alerts
async def temperature_alert_message(ctx: Context, min_temp: float, max_temp: float, current_temp: float, forecasted_temp: float):
    if current_temp > max_temp:
        await ctx.send(user_agent.address,Alert(text="Alert! Current temperature is above your preferred temperature range."))
    elif current_temp < min_temp:
        await ctx.send(user_agent.address,Alert(text="Alert! Current temperature is below your preferred temperature range."))
    else:
        ctx.logger.info("You will be informed if the temperature goes out of your preferred range.")

    if forecasted_temp > max_temp:
        await ctx.send(user_agent.address,Alert(text="Alert! Forecasted temperature for the next 24 hours is above your preferred temperature range."))
    elif forecasted_temp < min_temp:
        await ctx.send(user_agent.address,Alert(text="Alert! Forecasted temperature for the next 24 hours is below your preferred temperature range."))
    else:
        pass

# Message handler for receiving user preferences
@temperature_alert_agent.on_message(model=UserPreference)
async def handle_message(ctx: Context, sender: str, msg: UserPreference):
    ctx.storage.set("minTemp", msg.minTemp)
    ctx.storage.set("maxTemp",msg.maxTemp)
    ctx.storage.set("location", msg.location)
