from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low
from messages import TemperatureRequest, TemperatureResponse
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
def check_temp_range(ctx:Context):
    ctx.send(f'Enter preferred minimum tempreature: '{min_temp})
    ctx.send(f'Enter preferred maximum tempreature: '{max_temp})

    current_temp = fetch_temperature()

    if curr_temp > max_temp:
        ctx.send(sender, TemperatureRequest(Model))
    
    elif curr_temp<min_temp:
        ctx.send(sender, TemperatureRequest(Model))


@agent.on_interval(period=120)
async def fetch_weather_data(ctx: Context):
    data = json.loads(get_weather_data("Nasik"))
    curr_temp = data['current']['temp_c']
    ctx.logger.info(f'Temperature: {curr_temp}')

# Message handler for temperature alert requests'
@agent.on_message(model=TemperatureRequest)
async def handle_temperature_alert_request(ctx: Context, sender: str, request: TemperatureRequest):
    # Fetch the current temperature for the specified location.
    current_temperature = await fetch_temperature(ctx, sender, request)


if __name__ == "__main__":
    agent.run()

