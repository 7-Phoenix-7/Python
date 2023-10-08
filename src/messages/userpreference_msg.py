from uagents import Model

class UserPreference(Model):
    minTemp: float
    maxTemp: float
    location: str
