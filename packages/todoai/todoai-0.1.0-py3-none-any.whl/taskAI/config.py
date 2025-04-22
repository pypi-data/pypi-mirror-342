import os
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
model = None

def setup(key: str, model_name: str):
    """
    Sets up the API key and model name for the library.

    Args:
        key (str): The user's Gemini API key.
        model_name (str): The name of the Gemini model to use.
    """
    global api_key, model
    if not key:
        raise ValueError("API key is required. Please pass your Gemini API key to the setup function.")
    
    # Set the API key in the environment
    os.environ["GOOGLE_API_KEY"] = key
    api_key = os.environ["GOOGLE_API_KEY"]
    model = model_name