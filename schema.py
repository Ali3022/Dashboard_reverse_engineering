# MongoDB schema creation (using PyMongo)

from pymongo import MongoClient
from datetime import datetime, timedelta

client = MongoClient('mongodb+srv://Test_User:testUser124@clustermdb.9ux7k.mongodb.net/?retryWrites=true&w=majority&appName=ClusterMDB')
db = client['website_analytics']

# Define schema for sessions, page views, and traffic concentration

# Collection: sessions
db.sessions.drop()  # Drop the collection if it already exists to start fresh
sessions = db.sessions

# Document schema
session_data = {
    'date': datetime.utcnow(),  # Timestamp for the session data
    'sessions': 5139,
    'page_views': 22495,
    'users': 4520,
    'website_visits': 20582
}

# Insert multiple documents with different timestamps for time series
for i in range(30):
    session_data['date'] = datetime.utcnow() - timedelta(days=i)
    session_data['sessions'] += i * 10  # Incrementing for sample purposes
    session_data['page_views'] += i * 50
    session_data['users'] += i * 5
    session_data['website_visits'] += i * 20
    sessions.insert_one(session_data)

print("Sample data for sessions inserted.")

