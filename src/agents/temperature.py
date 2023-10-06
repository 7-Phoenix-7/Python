from uagents import Agent, Context
import json
import http

min_temp = None
max_temp = None
location = None

API_KEY = "f059d8455amsh4b068c5adade5bep1d646ajsn754b5adadb37"

# Creating the agent and funding it if needed
agent = Agent(
    name="tempmAgent",
    seed="temperature alert agent"
)

def fetch_data(city):
  conn = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")

  headers = {
    'X-RapidAPI-Key': API_KEY,
    'X-RapidAPI-Host': "weatherapi-com.p.rapidapi.com"
  }

  city = city.replace(" ", "_")
  conn.request("GET", f'/current.json?q={city}', headers=headers)

  res = conn.getresponse()
  data = res.read()

  return data.decode("utf-8")

#Function to check if the current temperature is outside of the user's preferred range.
def get_info(ctx: Context) -> bool:
  global min_temp
  global max_temp
  global location

  
  location = input("Enter Location: ")
  ctx.storage.set("location", location)

  
  min_temp = int(input("Enter Minimum Temperature: "))
  max_temp = int(input("Enter Maximum Temperature: "))
  ctx.storage.set("minTemp", min_temp)
  ctx.storage.set("maxTemp", max_temp)
  ctx.logger.info(f'Minimum Temperature set to {min_temp} and Maximum temperature set to {max_temp}.')
  
@agent.on_interval(period=120)
async def check_weather_status(ctx: Context):
    # start from here if the error occurs
    if min_temp is None or max_temp is None or location is None: 
       get_info(ctx)
    data = retrieve_info(ctx, location)
    
    if data is not None:
        curr_temp = data['current']['temp_c']
        ctx.logger.info(f'Current Temperature: {curr_temp}.')
        temperature_alert_message(ctx, min_temp, max_temp, curr_temp)
    else:
        ctx.logger.info("There was an Error getting weather status for the given location, please consider checking if the location is a valid city name.")


def retrieve_info(ctx: Context, location):
    while True:
        try:
          data = json.loads(fetch_data(location)) 
          curr_temp = data['current']['temp_c']
          return data
        except KeyError:
            ctx.logger.info("There was an Error getting weather status for the given location, please consider checking if the location is a valid city name.")
            location = input("Enter Location: ")
            ctx.storage.set("location", location)

# Message handler for temperature alert requests'
def temperature_alert_message(ctx: Context,min_temp: int, max_temp: int, curr_temp: int):
  if(curr_temp > max_temp):
    ctx.logger.info("Alert! Current temperature is above than your preffered temperature range.")
  elif(curr_temp < min_temp):
    ctx.logger.info("Alert! Current temperature is below than your preffered temperature range.")
  else:
    pass


