# Import the Bureau class from the uagents library
from uagents import Bureau

# Import the temperature_alert_agent and user_agent from their respective modules (not shown in this snippet)
from agents.temperature import temperature_alert_agent
from agents.user import user_agent

# Create an instance of the Bureau class
bureau = Bureau()

# Add the user_agent and temperature_alert_agent to the agent bureau
bureau.add(user_agent)
bureau.add(temperature_alert_agent)

# Check if the script is being run as the main program
if __name__ == "__main__":
    try:
        # Run the agent bureau
        bureau.run()
    except KeyboardInterrupt:
        # Handle a KeyboardInterrupt (e.g., when the user presses Ctrl+C)
        print("Process interrupted.")
