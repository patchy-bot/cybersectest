from pymongo import MongoClient

client = MongoClient()
db = client.shop

def seed_flag():
    # Insert unpublished flag document safely
    db.flags.replace_one(
        {'name': 'flag'},
        {'name': 'flag', 'value': 'SECRET_FLAG', 'published': False},
        upsert=True
    )
