from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["adaptive_engine"]

questions_col = db["questions"]
sessions_col = db["user_sessions"]