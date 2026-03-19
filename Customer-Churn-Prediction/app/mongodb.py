from pymongo import MongoClient
import certifi

MONGO_URL = "mongodb+srv://mauryarishabh9_db_user:Rishabh%4012345@cluster0.gwhv7cr.mongodb.net/?retryWrites=true&w=majority&tls=true"

client = MongoClient(MONGO_URL, tlsCAFile=certifi.where())

db = client["churn_db"]
collection = db["users"]

print("MongoDB Atlas connected")