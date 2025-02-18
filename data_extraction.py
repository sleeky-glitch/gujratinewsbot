import os
import json
from pymongo import MongoClient

# Load your mongodb connection string from an environment variable
mongo_uri = os.environ.get("MONGO_URI")  # Set this in your environment securely
client = MongoClient(mongo_uri)

# Access the database and collections
db = client["news_data"]
collection_dd = db["dd_news_articles"]
collection_guj = db["gujrat_samachar_articles"]

# Fetch articles from both collections
articles_dd = list(collection_dd.find())
articles_guj = list(collection_guj.find())

# Combine articles and extract the 'content' field (or any other field needed)
all_articles = [doc.get("content", "") for doc in (articles_dd + articles_guj) if doc.get("content")]

# Optionally, write the dataset to a file for later use in training
with open("gujarati_articles.json", "w", encoding="utf-8") as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=4)
