# Security Fix for web4/exec/db.py

**Vulnerability Type:** INSECURE_CONFIGURATION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Removed plain-text flag storage. Now retrieves MONGO_URI and ENCRYPTION_KEY from environment, encrypts the flag before insertion, and stores it under 'flag_enc'.

## Security Notes
Environment-based configuration avoids checked-in secrets. Using Fernet encryption hides the flag even if the DB is compromised. Securely rotate and manage keys.

## Fixed Code
```py
import os
from pymongo import MongoClient

# Retrieve database URI and credentials from environment variables
MONGO_URI = os.getenv('MONGO_URI')
if not MONGO_URI:
    raise RuntimeError('MONGO_URI not set')
client = MongoClient(MONGO_URI)
db = client.challenge_db
collection = db.flags

# Initialize with published flag set to False for private records, hide flag field
def initialize():
    # Do not store sensitive flag in collection with published=0
    # Instead store encrypted or move to separate secure store
    from cryptography.fernet import Fernet
    key = os.getenv('ENCRYPTION_KEY')
    if not key:
        raise RuntimeError('ENCRYPTION_KEY not set')
    f = Fernet(key)
    encrypted_flag = f.encrypt(b'SECRET_FLAG')
    collection.insert_one({'key': 'secret', 'published': 0, 'flag_enc': encrypted_flag})

if __name__ == '__main__':
    initialize()

```

## Additional Dependencies
- os
- cryptography.fernet

## Testing Recommendations
- Verify flag_enc exists instead of flag
- Attempt reading published=0 documents and ensure flag is encrypted

## Alternative Solutions
None provided
