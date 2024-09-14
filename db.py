# populate_data.py

from pymongo import MongoClient
from datetime import datetime
import random

# Establish connection to MongoDB
client = MongoClient('mongodb+srv://Test_User:testUser124@clustermdb.9ux7k.mongodb.net/?retryWrites=true&w=majority&appName=ClusterMDB')

# Connect to the database
db = client.web_analytics_dashboard

# Insert sample users data
users_collection = db.users
users_data = [
    {
        "user_id": f"user_{i}",
        "user_type": random.choice(["new", "returning"]),
        "age": random.randint(18, 65),
        "gender": random.choice(["male", "female"]),
        "location": random.choice(["USA", "Canada", "UK", "Germany", "France"]),
        "created_at": datetime.now()
    }
    for i in range(1, 201)  # Generate 200 users
]
users_collection.insert_many(users_data)
print(f"Inserted {len(users_data)} users.")

# Insert sample traffic_sources data
traffic_sources_collection = db.traffic_sources
traffic_sources_data = [
    {"source_id": 1, "source": "Direct", "percentage": 50},
    {"source_id": 2, "source": "Organic Search", "percentage": 18},
    {"source_id": 3, "source": "Social", "percentage": 15},
    {"source_id": 4, "source": "Paid Search", "percentage": 7},
    {"source_id": 5, "source": "Referral", "percentage": 5},
    {"source_id": 6, "source": "Email", "percentage": 5}
]
traffic_sources_collection.insert_many(traffic_sources_data)
print(f"Inserted {len(traffic_sources_data)} traffic sources.")

# Insert sample sessions data
sessions_collection = db.sessions
sessions_data = [
    {
        "session_id": f"session_{i}",
        "user_id": random.choice(users_data)["user_id"],
        "session_length": random.randint(10, 300),  # in seconds
        "page_views": random.randint(1, 10),
        "bounce": random.choice([True, False]),
        "traffic_source": random.choice(traffic_sources_data)["source"],
        "created_at": datetime.now()
    }
    for i in range(1, 1001)  # Generate 1000 sessions
]
sessions_collection.insert_many(sessions_data)
print(f"Inserted {len(sessions_data)} sessions.")

# Insert sample goals data
goals_collection = db.goals
goals_data = [
    {
        "goal_id": f"goal_{i}",
        "goal_name": random.choice(["Sign-up", "Purchase", "Form Submission"]),
        "completed": random.choice([True, False]),
        "value": random.uniform(10.0, 500.0) if random.choice([True, False]) else 0,
        "session_id": random.choice(sessions_data)["session_id"],
        "created_at": datetime.now()
    }
    for i in range(1, 301)  # Generate 300 goals
]
goals_collection.insert_many(goals_data)
print(f"Inserted {len(goals_data)} goals.")

