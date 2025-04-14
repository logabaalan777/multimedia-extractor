from pymongo import MongoClient, errors
from datetime import datetime
from typing import List, Optional
from models import ExtractedTextResponse

class Database:
    def __init__(self, uri: str = "mongodb://localhost:27017", db_name: str = "media_db"):
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            self.collection = self.db["extracted_texts"]
            print("MongoDB connection established successfully.")
        except errors.ConnectionError as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

    def insert_data(self, source: str, text: str, language: Optional[str] = None):
        try:
            print(f"Inserting data: source={source}, text={text}")
            result = self.collection.insert_one({
                "source": source,
                "text": text,
                "language": language,
                "timestamp": datetime.now()
            })
            print(f"Document inserted with id {result.inserted_id}")
        except errors.PyMongoError as e:
            print(f"Error inserting data: {e}")
            raise

    def get_all_data(self, language: Optional[str] = None, source: Optional[str] = None) -> List[ExtractedTextResponse]:
        query = {}
        if language:
            query["language"] = language
        if source:
            query["source"] = source
        
        try:
            results = self.collection.find(query).sort("timestamp", -1)
            return [
                ExtractedTextResponse(
                    source=r["source"],
                    text=r["text"],
                    language=r.get("language", ""),
                    timestamp=str(r["timestamp"])
                ) for r in results
            ]
        except errors.PyMongoError as e:
            print(f"Error retrieving data: {e}")
            raise

db = Database()

insert_data = db.insert_data
get_all_data = db.get_all_data