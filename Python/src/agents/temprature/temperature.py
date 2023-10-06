from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low
from messages import TemperatureRequest, TemperatureResponse
from typing import Tuple
import os
import requests
import json
import http

# Function to get weather data from a specified city
def get_weather_data(city):
    # Establish a connection to the weather API
    conn = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")

    # Set headers with API key
    headers = {
        'X-RapidAPI-Key': "f059d8455amsh4b068c5adade5bep1d646ajsn754b5adadb37",
        'X-RapidAPI-Host': "weatherapi-com.p.rapidapi.com"
    }

    # Make a request to the API
    conn.request("GET", f"/current.json?q={city}", headers=headers)

    # Get the response and read the data
    res = conn.getresponse()
    data = res.read()

    # Decode the data and return as a string
    return data.decode("utf-8")

# Creating the agent and funding it if needed
agent = Agent(
    name="timAgent",
    seed="temperature_alert_agent"
)

# Function to log the request information
@agent.on_message(model=TemperatureRequest)
async def log_request(ctx: Context, sender: str, request: TemperatureRequest):
    ctx.logger.info(f"Got request from {sender} for temperature of : {request.location}")

# Function to fetch current temperature for a specified location
async def fetch_temperature(ctx: Context, sender: str, request: TemperatureRequest):

    # Fetch weather data using the get_weather_data function
    data = json.loads(get_weather_data(request.location))  # Use request.location instead of requests.location
    current_temperature = data["current"]["temp_c"]

    return current_temperature

# Create an instance of the protocol with label "timAgent"
tempAgent = Protocol(name="timAgent", version="0.6.2")

# Function to check if the current temperature is outside of the user's preferred range
async def prompt_and_parse_user(ctx: Context, sender: str) -> Tuple[float, float, str]:

    await ctx.send(sender, "Enter your preferred city: ")
    location = await ctx.receive(sender)

    # Prompt the user to enter their preferred minimum temperature
    await ctx.send(sender, "Enter your preferred minimum temperature: ")
    min_temp_str = await ctx.receive(sender)

    # Prompt the user to enter their preferred maximum temperature
    await ctx.send(sender, "Enter your preferred maximum temperature: ")
    max_temp_str = await ctx.receive(sender)

    # Convert the temperature strings to floats
    min_temp = float(min_temp_str)
    max_temp = float(max_temp_str)

    return (min_temp, max_temp, location)

# Define an interval for fetching weather data
@agent.on_interval(period=120)
async def fetch_weather_data(ctx: Context):

    preferred_city = await prompt_and_parse_user(ctx, "some_sender")[-1]

    data = json.loads(get_weather_data(preferred_city))
    curr_temp = data['current']['temp_c']
    ctx.logger.info(f'Temperature: {curr_temp}')

# Message handler for temperature alert requests
@agent.on_message(model=TemperatureRequest)
async def handle_temperature_alert_request(ctx: Context, sender: str, request: TemperatureRequest):
    # Prompt the user to enter their preferred temperature range
    min_temp, max_temp, preferred_city = await prompt_and_parse_user(ctx, sender)

    # Fetch the current temperature for the specified location
    current_temperature = await fetch_temperature(ctx, sender, request)

    # If the temperature is outside of the user's preferred range, send them a message
    if current_temperature is not None:
        if current_temperature > max_temp:
            ctx.send(sender, f"The temperature in {request.location} is above your preferred maximum of {max_temp} degrees Celsius.")
        elif current_temperature < min_temp:
            ctx.send(sender, f"The temperature in {request.location} is below your preferred minimum of {min_temp} degrees Celsius.")

# Include the protocol in the agent
agent.include(tempAgent)

# Run the agent's event loop
if __name__ == "__main__":
    agent.run()
