from pymongo import MongoClient

def create_database():
    # Connect to MongoDB (Replace 'localhost' and '27017' with your MongoDB URL if needed)
    client = MongoClient('mongodb+srv://Test_User:testUser124@clustermdb.9ux7k.mongodb.net/?retryWrites=true&w=majority&appName=ClusterMDB')
    # Create or connect to the database
    db = client['web_analytics_dashboard']

    # Drop existing collections if they exist to start fresh
    db.sessions_data.drop()
    db.traffic_sources.drop()
    db.geo_locations.drop()
    db.goal_data.drop()

    # Create collections and define schema (No strict schema enforcement in MongoDB)
    
    # Sessions Data
    db.create_collection('sessions_data')
    
    # Traffic Sources
    db.create_collection('traffic_sources')
    
    # Geo Locations
    db.create_collection('geo_locations')
    
    # Goal Data
    db.create_collection('goal_data')
    
    print("Database and collections created successfully!")

if __name__ == "__main__":
    create_database()

