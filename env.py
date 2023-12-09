import dotenv
import os

dotenv.load_dotenv()

def load_or_throw(env_name: str) -> str:
    value = os.getenv(env_name)
    if value is None:
        raise ValueError(f"Environment variable {env_name} is not set")
    return value

OPENAI_API_KEY=load_or_throw('OPENAI_API_KEY')
