# Import the Model class from the uagents library
from uagents import Model

# Define a message model named Alert
class Alert(Model):
    # Define an attribute 'text' to store the text of the alert message
    text: str
