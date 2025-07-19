# Security Fix for web4/exec/db.py

**Vulnerability Type:** INFORMATION_DISCLOSURE  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Separated public and internal flags into different collections. Internal flags are never exposed by public APIs. The API layer must only query `public_flags`.

## Security Notes
Keep SECRET_FLAG in environment, not in code. Enforce least privilege MongoDB credentials so API cannot read internal_flags.

## Fixed Code
```py
from pymongo import MongoClient
import os

client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017'))
db = client.flagsdb

# Collections: public_flags, internal_flags
def setup_flags():
    # Insert only public flags into public_flags collection
    db.public_flags.delete_many({})
    db.public_flags.insert_many([
        {'id':1, 'flag':'CTF{public1}'},
        # other public flags
    ])

    # Internal flags stored separately, not exposed via API
    db.internal_flags.delete_many({})
    db.internal_flags.insert_one(
        {'id':2, 'flag':os.getenv('SECRET_FLAG')}
    )

# API must explicitly read from public_flags only
def get_public_flags():
    return list(db.public_flags.find({}, {'_id':0}))

if __name__ == '__main__':
    setup_flags()
```

## Additional Dependencies
- os

## Testing Recommendations
- Attempt to query internal_flags via API

## Alternative Solutions
None provided
