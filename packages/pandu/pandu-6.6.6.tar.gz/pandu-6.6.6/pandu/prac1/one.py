from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["testdb"]
collection = db["testcollection"]

# # Create
collection.insert_one({"name": "Alice", "age": 25})

# # Read
print(collection.find_one({"name": "Alice"}))

# Update
collection.update_one({"name": "Alice"}, {"$set": {"age": 26}})

# Delete
collection.delete_one({"name": "Alice"})

print(client.list_database_names())



