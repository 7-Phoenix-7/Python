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

#Create a instance of protocol with label "timAgent"
agent = Protocol(name="timAgent", version="0.6.2")

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

if __name__ == "__main__":
    agent.run()
