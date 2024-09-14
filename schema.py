# create_schema.py

from pymongo import MongoClient, ASCENDING

# Establish connection to MongoDB
client = MongoClient('mongodb+srv://Test_User:testUser124@clustermdb.9ux7k.mongodb.net/?retryWrites=true&w=majority&appName=ClusterMDB')
# Create or connect to the database
db = client.web_analytics_dashboard

# Drop collections if they exist (for clean setup)
db.users.drop()
db.sessions.drop()
db.traffic_sources.drop()
db.goals.drop()
db.metrics.drop()

# Create users collection with a unique index on user_id
users_collection = db.users
users_collection.create_index([("user_id", ASCENDING)], unique=True)

# Create traffic_sources collection
traffic_sources_collection = db.traffic_sources
traffic_sources_collection.create_index([("source_id", ASCENDING)], unique=True)

# Create sessions collection with an index on session_id
sessions_collection = db.sessions
sessions_collection.create_index([("session_id", ASCENDING)], unique=True)

# Create goals collection with an index on goal_id
goals_collection = db.goals
goals_collection.create_index([("goal_id", ASCENDING)], unique=True)

# Create metrics collection
metrics_collection = db.metrics
metrics_collection.create_index([("metric_id", ASCENDING)], unique=True)

print("MongoDB schema has been created successfully.")

