import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    MONGO_URI = os.getenv("MONGO_DATABASE", "mongodb://localhost:27017/test")
    DEBUG = True
