import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "llama3.1")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
APP_PORT = int(os.getenv("APP_PORT", "8000"))
ALLOW_COMMANDS = os.getenv("ALLOW_COMMANDS", "true").lower() == "true"
