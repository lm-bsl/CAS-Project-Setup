from dotenv import load_dotenv
import os

# load environment variables from .env file
load_dotenv()  

# get the environment variables for Open AI
OPENAI_KEY = os.getenv("OPENAI_KEY")
OPENAI_MODEL = "gpt-3.5-turbo-16k"

# get the environment variables for Mistral
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_MODEL = "open-mixtral-8x22b"