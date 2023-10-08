from uagents import Agent, Context
from messages.alert_msg import Alert
from messages.userpreference_msg import UserPreference
from messages.request import Request
from uagents import Model
# from temperature import temperature_alert_agent

user_agent = Agent(
    name="user_agent",
    seed="user agent for the temperature alert system"
)

# Global variables for user preferences
min_temp = None
max_temp = None
location = None

@user_agent.on_message(model=Request)
async def get_user_prefernce(ctx: Context, sender: str, msg: Request):
    global min_temp
    global max_temp
    global location
    if min_temp is None or max_temp is None or location is None:
        # get location
        location = input("Enter Location: ")
        # get preffered minimum and maximum range
        min_temp = int(input("Enter Minimum Temperature: "))
        max_temp = int(input("Enter Maximum Temperature: "))
        await ctx.send(msg.response_address, UserPreference(minTemp=min_temp, maxTemp=max_temp, location=location))
        ctx.logger.info(f'Minimum Temperature set to {min_temp} and Maximum temperature set to {max_temp}.')

@user_agent.on_message(model=Alert)
async def handle_alert_message(ctx: Context, sender: str, msg: Alert):
   ctx.logger.info(f'Message: {msg.text}')


