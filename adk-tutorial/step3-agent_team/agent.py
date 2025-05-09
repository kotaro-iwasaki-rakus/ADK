# @title Import necessary libraries
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm # For multi-model support
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types # For creating message Content/Parts

ROOT_AGENT_MODEL="gemini-1.5-flash-002"
SUB_AGENT_MODEL="gemini-1.5-flash-002"

# @title Define the get_weather Tools
def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city (e.g., "New York", "London", "Tokyo").

    Returns:
        dict: A dictionary containing the weather information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'report' key with weather details.
              If 'error', includes an 'error_message' key.
    """
    print(f"--- Tool: get_weather called for city: {city} ---")
    city_normalized = city.lower().replace(" ", "")

    # Mock weather data
    mock_weather_db = {
        "newyork": {"status": "success", "report": "The weather in New York is sunny with a temperature of 25°C."},
        "london": {"status": "success", "report": "It's cloudy in London with a temperature of 15°C."},
        "tokyo": {"status": "success", "report": "Tokyo is experiencing light rain and a temperature of 18°C."},
    }

    if city_normalized in mock_weather_db:
        return mock_weather_db[city_normalized]
    else:
        return {"status": "error", "error_message": f"Sorry, I don't have weather information for '{city}'."}

# @title Define Tools for Greeting and Farewell Agents
def say_hello(name: str = "there") -> str:
    """Provides a simple greeting, optionally addressing the user by name.

    Args:
        name (str, optional): The name of the person to greet. Defaults to "there".

    Returns:
        str: A friendly greeting message.
    """
    print(f"--- Tool: say_hello called with name: {name} ---")
    return f"Hello, {name}!"

def say_goodbye() -> str:
    """Provides a simple farewell message to conclude the conversation."""
    print(f"--- Tool: say_goodbye called ---")
    return "Goodbye! Have a great day."

# @title Define Greeting and Farewell Sub-Agents
# --- Greeting Agent ---
greeting_agent = Agent(
    model=SUB_AGENT_MODEL,
    name="greeting_agent",
    instruction="""
        You are the Greeting Agent. Your ONLY task is to provide a friendly greeting to the user.
        Use the 'say_hello' tool to generate the greeting.
        If the user provides their name, make sure to pass it to the tool.
        Do not engage in any other conversation or tasks.
    """,
    description="Handles simple greetings and hellos using the 'say_hello' tool.",
    tools=[say_hello],
)

# --- Farewell Agent ---
farewell_agent = Agent(
    model=SUB_AGENT_MODEL,
    name="farewell_agent",
    instruction="""
        You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message.
        Use the 'say_goodbye' tool when the user indicates they are leaving or ending the conversation
        (e.g., using words like 'bye', 'goodbye', 'thanks bye', 'see you').
        Do not perform any other actions.
    """,
    description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.",
    tools=[say_goodbye],
)

# @title Define the Weather Agent
root_agent = Agent(
    name="weather_agent_v2",
    model=ROOT_AGENT_MODEL, 
    description="The main coordinator agent. Handles weather requests and delegates greetings/farewells to specialists.",
    instruction="""
        You are the main Weather Agent coordinating a team. Your primary responsibility is to provide weather information.
        Use the 'get_weather' tool ONLY for specific weather requests (e.g., 'weather in London').
        You have specialized sub-agents:
        1. 'greeting_agent': Handles simple greetings like 'Hi', 'Hello'. Delegate to it for these.
        2. 'farewell_agent': Handles simple farewells like 'Bye', 'See you'. Delegate to it for these.
        Analyze the user's query. If it's a greeting, delegate to 'greeting_agent'. If it's a farewell, delegate to 'farewell_agent'.
        If it's a weather request, handle it yourself using 'get_weather'.
        For anything else, respond appropriately or state you cannot handle it.
    """,
    tools=[get_weather],
    sub_agents=[greeting_agent, farewell_agent]
)
