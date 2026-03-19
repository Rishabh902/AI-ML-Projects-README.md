import certifi
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")

try:
    client = MongoClient(
        MONGO_URL,
        tls=True,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=5000,
    )
    client.admin.command("ping")
    print("Connected successfully!")
except Exception as e:
    print(f"Failed: {e}")


# from pymongo import MongoClient
# import certifi

# client = MongoClient("YOUR_URL", tlsCAFile=certifi.where())

# print(client.list_database_names())