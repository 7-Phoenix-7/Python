# Import necessary modules and message classes
from uagents import Agent, Context
from messages.alert_msg import Alert
from messages.userpreference_msg import UserPreference
from messages.request import Request
from uagents import Model

# Create the user_agent
user_agent = Agent(
    name="user_agent",
    seed="user agent for the temperature alert system"
)

# Global variables for user preferences
min_temp = None
max_temp = None
location = None

# Handle incoming Request messages
@user_agent.on_message(model=Request)
async def get_user_preference(ctx: Context, sender: str, msg: Request):
    global min_temp
    global max_temp
    global location
    if min_temp is None or max_temp is None or location is None:
        # Prompt user for location
        location = input("Enter Location: ")
        # Prompt user for preferred minimum and maximum temperature range
        min_temp = int(input("Enter Minimum Temperature: "))
        max_temp = int(input("Enter Maximum Temperature: "))
        # Send UserPreference message with user-defined preferences as a response
        await ctx.send(msg.response_address, UserPreference(minTemp=min_temp, maxTemp=max_temp, location=location))
        ctx.logger.info(f'Minimum Temperature set to {min_temp} and Maximum temperature set to {max_temp}.')

# Handle incoming Alert messages
@user_agent.on_message(model=Alert)
async def handle_alert_message(ctx: Context, sender: str, msg: Alert):
    # Log the received alert message
    ctx.logger.info(f'Message: {msg.text}')
