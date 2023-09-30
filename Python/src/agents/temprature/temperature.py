from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low
import os
import requests

WEATHER_API = ""

# Creating the agent and funding it if needed
agent = Agent(
    name="timAgent",
    seed="temperature_alert_agent"
)

fund_agent_if_low(agent.wallet.address)

#Function to log the request information
async def log_request(ctx: Context, sender: str, request: TemperatureAlertRequest):
    ctx.logger.info(f"Got request from {sender} for temperature of : {request.location}")

#Function to fetch cuerrent temperature for specified lcation
async def fetch_temperature(ctx: Context, sender: str, request: TemperatureAlertRequest):
    temp_response =  await requests.get(
        WEATHER_API.format(location=request.location)
    )
    # Extract the current temperature from the response.
    current_temperature = temperature_response["main"]["temp"]

    return current_temperature

#Function to check if the current temperature is outside of the user's preferred range.
def check_temp_range():
    
# Message handler for temperature alert requests
    @temperature_alert_agent.on_message(model=TemperatureAlertRequest)
    async def handle_temperature_alert_request(ctx: Context, sender: str, request: TemperatureAlertRequest):
    # Fetch the current temperature for the specified location.
        current_temperature = await fetch_temperature(ctx, sender, request)