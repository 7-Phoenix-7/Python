from uagents import Bureau
from agents.temperature import temperature_alert_agent
from agents.user import user_agent

bureau = Bureau()
bureau.add(user_agent)
bureau.add(temperature_alert_agent)

if __name__ == "__main__":
    try:
        bureau.run()
    except KeyboardInterrupt:
        print("Process interrupted.")
