from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_KEY: str
    API_IP: str
    API_PORT: int
    CHANNEL_ID: int

    class Config:
        env_file = ".env"


settings = Settings()


# Customize these values as needed for your application:

# Command to trigger the bot to log out
logout_command = "!logout"

# Message sent by the bot when logging out
logout_message = "Logging Out..."

# System prompt sent to the Ollama model to define its behavior
system_prompt = "You are a helpful assistant."

# The name of the model used by the Ollama API
model = "dolphin-mistral:latest"
