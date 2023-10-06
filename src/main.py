from uagents import Bureau
from agents.temperature import agent

if __name__ == "__main__":
    try:
        agent.run()
    except KeyboardInterrupt:
        print("Process interrupted.")
