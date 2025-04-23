import mongomock
from pathlib import Path
import json

# Create in-memory MongoDB mock
client = mongomock.MongoClient()
db = client["product_db"]

# Collections
products_collection = db["products"]
logs_collection = db["logs"]

DATA_PATH = Path("/app/meta") 
METADATA_FILE = DATA_PATH / "products.json"

def load_metadata_from_disk():
    if METADATA_FILE.exists():
        with open(METADATA_FILE, "r") as f:
            docs = json.load(f)
            for doc in docs:
                products_collection.insert_one(doc)