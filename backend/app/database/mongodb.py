import os

from dotenv import load_dotenv
from pymongo import MongoClient


# Load environment variables from .env
load_dotenv()


# Get MongoDB connection details
MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "synthetic_speech_detection"
)


# Create MongoDB client
client = MongoClient(MONGODB_URL)


# Connect to our database
database = client[DATABASE_NAME]