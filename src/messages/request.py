# Import the Model class from the uagents library
from uagents import Model

# Define a message model named Request
class Request(Model):
    # Define an attribute 'response_address' to store the response address for the request
    response_address: str
