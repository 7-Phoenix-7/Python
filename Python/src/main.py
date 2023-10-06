# Import the Bureau and the 'agent' from the respective modules
from uagents import Bureau
from agents.temperature import agent

# Create a Bureau instance with the specified endpoint (you may want to replace 'h' with the actual endpoint)
bureau = Bureau(endpoint='h')

# Check if the script is the main program
if __name__ == "__main__":
    # Print a message indicating that the agent is being added to the Bureau
    print(f"Adding agent to Bureau: {agent.address}")

    # Add the 'agent' to the Bureau
    bureau.add(agent)

    # Run the Bureau's event loop
    bureau.run()
