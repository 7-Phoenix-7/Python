from uagents import Bureau
from agents.temperature import agent

bureau = Bureau(agent)

if __name__ == "__main__":
    bureau.run()
