# Import the Model class from the uagents module
from uagents import Model

# Define a custom model class 'TemperatureRequest' that inherits from Model
class TemperatureRequest(Model):
    # Define fields for the model class
    location: str            # Represents the location for which temperature is requested
    min_temperature: float   # Represents the minimum preferred temperature
    max_temperature: float   # Represents the maximum preferred temperature

# Define another custom model class 'TemperatureResponse' that inherits from Model
class TemperatureResponse(Model):
    # Define fields for the model class
    location: str            # Represents the location for which temperature is responded
    current_temperature: float   # Represents the current temperature at the specified location

# Define another custom model class 'Error' that inherits from Model
class Error(Model):
    # Define fields for the model class
    error: str               # Represents an error message
