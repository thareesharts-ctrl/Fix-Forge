from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load .env file with absolute path relative to database.py
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path)

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = AsyncIOMotorClient(MONGO_URI)

db = client[DATABASE_NAME]
