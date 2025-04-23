import mongomock
from pathlib import Path
import json
from datetime import datetime
from bson import ObjectId

# Create in-memory MongoDB mock
client = mongomock.MongoClient()
db = client["product_db"]

# Collections
products_collection = db["products"]
logs_collection = db["logs"]

DATA_PATH = Path("/app/meta") 
METADATA_FILE = DATA_PATH / "products.json"
LOG_FILE = DATA_PATH / "logs.json"

def load_metadata_from_disk():
    if METADATA_FILE.exists():
        with open(METADATA_FILE, "r") as f:
            docs = json.load(f)
            for doc in docs:
                products_collection.insert_one(doc)

def save_logs_to_disk():
    """Persist current logs to disk (optional for shutdown hook or testing)."""
    logs = list(logs_collection.find())
    for log in logs:
        log["_id"] = str(log["_id"])  # make serializable
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2, default=str)

def load_logs_from_disk():
    """Load previously saved logs from disk."""
    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
            for log in logs:
                logs_collection.insert_one(log)
    else:
        LOG_FILE.touch()  # create empty file
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

def log_event(level, message, meta=None):
    """Insert a log event into the logs_collection."""
    log_entry = {
        "_id": str(ObjectId()),
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "message": message,
        "meta": meta or {}
    }
    logs_collection.insert_one(log_entry)