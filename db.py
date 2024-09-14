import pymongo
from pymongo import MongoClient
import random
import datetime

# Connect to MongoDB
client = MongoClient('mongodb+srv://Test_User:testUser124@clustermdb.9ux7k.mongodb.net/?retryWrites=true&w=majority&appName=ClusterMDB')

# Connect to the database and collections
db = client['web_analytics_db']
users_collection = db['users']
sessions_collection = db['sessions']
traffic_sources_collection = db['traffic_sources']
goals_collection = db['goals']

# Helper function to generate random user data
def generate_user(user_id):
    return {
        'user_id': user_id,
        'name': f'User{user_id}',
        'email': f'user{user_id}@example.com',
        'location': random.choice(['USA', 'Canada', 'UK', 'Germany', 'Australia']),
        'join_date': datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 365))
    }

# Helper function to generate session data
def generate_session(session_id, user_id):
    start_time = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 30))
    end_time = start_time + datetime.timedelta(minutes=random.randint(1, 60))
    return {
        'session_id': session_id,
        'user_id': user_id,
        'start_time': start_time,
        'end_time': end_time,
        'bounce_rate': random.randint(30, 80),
        'traffic_source': random.choice(['Direct', 'Organic Search', 'Social', 'Paid Search', 'Referral', 'Email']),
        'goal_id': random.randint(1, 10)
    }

# Helper function to generate goal data
def generate_goal(goal_id, session_id):
    return {
        'goal_id': goal_id,
        'session_id': session_id,
        'goal_type': random.choice(['Purchase', 'Sign-up', 'Subscription']),
        'goal_value': random.randint(50, 500),
        'conversion_rate': round(random.uniform(1.0, 5.0), 1)
    }

# Helper function to generate traffic source data
def generate_traffic_source(source):
    return {
        'source': source,
        'sessions': random.randint(1000, 10000),
        'conversions': random.randint(100, 1000),
        'bounce_rate': random.randint(30, 70)
    }

# Insert sample users
print("Inserting sample users...")
for i in range(1, 51):  # 50 sample users
    users_collection.insert_one(generate_user(i))

# Insert sample sessions
print("Inserting sample sessions...")
for i in range(1, 151):  # 150 sample sessions
    sessions_collection.insert_one(generate_session(i, random.randint(1, 50)))  # link to random user

# Insert sample goals
print("Inserting sample goals...")
for i in range(1, 11):  # 10 sample goals
    goals_collection.insert_one(generate_goal(i, random.randint(1, 150)))  # link to random session

# Insert sample traffic sources
print("Inserting sample traffic sources...")
traffic_sources = ['Direct', 'Organic Search', 'Social', 'Paid Search', 'Referral', 'Email']
for source in traffic_sources:
    traffic_sources_collection.insert_one(generate_traffic_source(source))

# Print confirmation
print("Sample data inserted into users, sessions, goals, and traffic sources collections.")

client.close()

