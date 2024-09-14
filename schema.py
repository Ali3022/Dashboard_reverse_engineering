import pymongo
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb+srv://Test_User:testUser124@clustermdb.9ux7k.mongodb.net/?retryWrites=true&w=majority&appName=ClusterMDB')

# Create or connect to the database
db = client['web_analytics_db']

# Create collections
users_collection = db['users']
sessions_collection = db['sessions']
traffic_sources_collection = db['traffic_sources']
goals_collection = db['goals']

# Ensure indexes for optimized queries (you can add more indexes as needed)
users_collection.create_index([('user_id', pymongo.ASCENDING)], unique=True)
sessions_collection.create_index([('session_id', pymongo.ASCENDING)], unique=True)
traffic_sources_collection.create_index([('source', pymongo.ASCENDING)])
goals_collection.create_index([('goal_id', pymongo.ASCENDING)], unique=True)

# Print confirmation
print("Database schema has been created with collections for users, sessions, traffic sources, and goals.")

client.close()

