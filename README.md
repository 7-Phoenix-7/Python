# Temperature Alert System

## Description

The Temperature Alert System is a Python-based agent-based system that monitors weather conditions and sends temperature alerts to users based on their preferences. It consists of two main agents: `user_agent` for user interaction and preferences input, and `temperature_alert_agent` for fetching weather data and sending alerts. The system allows users to set their preferred temperature range and location, and it checks weather conditions periodically to send alerts if the current or forecasted temperature falls outside the user's specified range.

## Instructions to Run the Project

To run the Temperature Alert System, follow these steps:

1. Clone the project repository to your local machine.

   ```bash
   git clone https://github.com/7-Phoenix-7/temperature-alert-system.git

2. Install Dependencies
  ```poetry install```

3. Setup congig.py File

   RapidAPI Key
    Visit RapidAPI.
    Sign up or log in.
    Search for the Forecast Weather API and subscribe.
    Once subscribed, copy your X-RapidAPI-Key

   Create a config.py file, in the src/agents folder
   ```API_KEY={YOUR_API_KEY}```

4. Run the main script
  To run the project and its agents:
    ```poetry run python main.py```
   


