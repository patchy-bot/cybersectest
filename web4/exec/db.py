# web4/exec/db.py
from pymongo import MongoClient
import os

# Database seeding script
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
client = MongoClient(MONGO_URI)
# Use a dedicated 'flags' collection with restricted access
db = client.challenge_db

# Insert flag into a protected collection that is excluded from user queries
if __name__ == '__main__':
    flags = db.get_collection('flags')
    # Upsert to avoid duplicates
    flags.update_one({'name': 'hidden_flag'}, {'$set': {'value': 'FLAG{secret}'}}, upsert=True)
    print('Flag inserted securely')
