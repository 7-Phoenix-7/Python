from uagents import Model

class TemperatureRequest(Model):
    location: str
    min_temperature: float
    max_temperature: float


class TemperatureResponse(Model):
    location: str
    current_temperature: float


class Error(Model):
    error: str
