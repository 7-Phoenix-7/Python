# Import the Model class from the uagents library
from uagents import Model

# Define a message model named UserPreference
class UserPreference(Model):
    # Define three attributes:
    # - 'minTemp' to store the preferred minimum temperature as a float
    # - 'maxTemp' to store the preferred maximum temperature as a float
    # - 'location' to store the preferred location as a string
    minTemp: float
    maxTemp: float
    location: str
