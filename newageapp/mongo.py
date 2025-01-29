from pymongo import MongoClient
from urllib.parse import quote_plus
"""
# Your MongoDB username and password
username = "wanjos"
password = "0903620Wanjos@#$"

# URL-encode the username and password
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)
"""
# Replace with your MongoDB connection string
CONNECTION_STRING = "mongodb+srv://wanjos:0903620Wanjos@newagedatabase.40ybp.mongodb.net/?retryWrites=true&w=majority&appName=newagedatabase"
# Connect to the MongoDB cluster
client = MongoClient(CONNECTION_STRING,ssl=False)

# Access the specific database and collection
db = client['newageadatabase']  # Database name
users_collection = db['users']  # Collection name
