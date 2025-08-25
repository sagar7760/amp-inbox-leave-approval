from pymongo import MongoClient
from pymongo.collection import Collection
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client.get_default_database()

users_collection: Collection = db["users"]
leaves_collection: Collection = db["leave_requests"]
