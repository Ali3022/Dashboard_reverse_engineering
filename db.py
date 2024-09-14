from pymongo import MongoClient
from datetime import datetime

def populate_data():
    # Connect to MongoDB (Replace 'localhost' and '27017' with your MongoDB URL if needed)
    client = MongoClient('mongodb+srv://Test_User:testUser124@clustermdb.9ux7k.mongodb.net/?retryWrites=true&w=majority&appName=ClusterMDB')   
    # Connect to the database
    db = client['web_analytics_dashboard']
    
    # Expanded data for sessions, users, and bounce rate (sessions_data collection)
    sessions_data = [
        {"date": datetime(2023, 11, 1), "total_sessions": 1500, "users": 1300, "bounce_rate": 47},
        {"date": datetime(2023, 11, 2), "total_sessions": 1600, "users": 1350, "bounce_rate": 46},
        {"date": datetime(2023, 11, 3), "total_sessions": 1700, "users": 1400, "bounce_rate": 45},
        {"date": datetime(2023, 11, 4), "total_sessions": 1550, "users": 1320, "bounce_rate": 48},
        {"date": datetime(2023, 11, 5), "total_sessions": 1650, "users": 1380, "bounce_rate": 44},
        {"date": datetime(2023, 11, 6), "total_sessions": 1800, "users": 1500, "bounce_rate": 43},
        {"date": datetime(2023, 11, 7), "total_sessions": 1900, "users": 1550, "bounce_rate": 42},
        {"date": datetime(2023, 11, 8), "total_sessions": 2100, "users": 1600, "bounce_rate": 41},
        {"date": datetime(2023, 11, 9), "total_sessions": 2200, "users": 1700, "bounce_rate": 40},
        {"date": datetime(2023, 11, 10), "total_sessions": 2300, "users": 1750, "bounce_rate": 39},
        # Add as many dates as required for better test cases
    ]
    
    # Insert data into the 'sessions_data' collection
    db.sessions_data.insert_many(sessions_data)
    
    # Expanded data for traffic sources (traffic_sources collection)
    traffic_sources = [
        {"source_name": "Direct", "percentage": 50},
        {"source_name": "Organic Search", "percentage": 30},
        {"source_name": "Email", "percentage": 5},
        {"source_name": "Referral", "percentage": 5},
        {"source_name": "Paid Search", "percentage": 7},
        {"source_name": "Social", "percentage": 3},
    ]
    
    # Insert data into the 'traffic_sources' collection
    db.traffic_sources.insert_many(traffic_sources)
    
    # Expanded geo-location data (geo_locations collection)
    geo_locations = [
        {"country": "USA", "latitude": 37.0902, "longitude": -95.7129},
        {"country": "Canada", "latitude": 56.1304, "longitude": -106.3468},
        {"country": "UK", "latitude": 51.5074, "longitude": -0.1278},
        {"country": "Germany", "latitude": 51.1657, "longitude": 10.4515},
        {"country": "France", "latitude": 46.6034, "longitude": 1.8883},
        {"country": "Australia", "latitude": -25.2744, "longitude": 133.7751},
        {"country": "India", "latitude": 20.5937, "longitude": 78.9629},
        {"country": "Brazil", "latitude": -14.2350, "longitude": -51.9253},
        {"country": "South Africa", "latitude": -30.5595, "longitude": 22.9375},
        {"country": "Japan", "latitude": 36.2048, "longitude": 138.2529},
        {"country": "Russia", "latitude": 61.5240, "longitude": 105.3188},
        {"country": "China", "latitude": 35.8617, "longitude": 104.1954},
        {"country": "Mexico", "latitude": 23.6345, "longitude": -102.5528},
        {"country": "Italy", "latitude": 41.8719, "longitude": 12.5674},
        {"country": "Netherlands", "latitude": 52.1326, "longitude": 5.2913},
        {"country": "Spain", "latitude": 40.4637, "longitude": -3.7492},
        {"country": "South Korea", "latitude": 35.9078, "longitude": 127.7669},
        {"country": "New Zealand", "latitude": -40.9006, "longitude": 174.8860},
        {"country": "Sweden", "latitude": 60.1282, "longitude": 18.6435},
        {"country": "Norway", "latitude": 60.4720, "longitude": 8.4689},
        {"country": "Argentina", "latitude": -38.4161, "longitude": -63.6167},
        {"country": "Saudi Arabia", "latitude": 23.8859, "longitude": 45.0792},
        {"country": "UAE", "latitude": 23.4241, "longitude": 53.8478},
    ]
    
    # Insert data into the 'geo_locations' collection
    db.geo_locations.insert_many(geo_locations)
    
    # Expanded data for goal metrics (goal_data collection)
    goal_data = [
        {"date": datetime(2023, 11, 1), "goal_completion": 109, "goal_value": 352, "conversion_rate": 3.7},
        {"date": datetime(2023, 11, 2), "goal_completion": 120, "goal_value": 400, "conversion_rate": 3.9},
        {"date": datetime(2023, 11, 3), "goal_completion": 100, "goal_value": 320, "conversion_rate": 3.5},
        {"date": datetime(2023, 11, 4), "goal_completion": 115, "goal_value": 360, "conversion_rate": 3.8},
        {"date": datetime(2023, 11, 5), "goal_completion": 130, "goal_value": 420, "conversion_rate": 4.0},
        {"date": datetime(2023, 11, 6), "goal_completion": 140, "goal_value": 450, "conversion_rate": 4.1},
        {"date": datetime(2023, 11, 7), "goal_completion": 135, "goal_value": 440, "conversion_rate": 4.0},
        {"date": datetime(2023, 11, 8), "goal_completion": 150, "goal_value": 480, "conversion_rate": 4.3},
        {"date": datetime(2023, 11, 9), "goal_completion": 160, "goal_value": 500, "conversion_rate": 4.5},
        {"date": datetime(2023, 11, 10), "goal_completion": 155, "goal_value": 490, "conversion_rate": 4.4},
        # Add more dates as required for better test cases
    ]
    
    # Insert data into the 'goal_data' collection
    db.goal_data.insert_many(goal_data)
    
    print("Detailed sample data populated successfully!")

if __name__ == "__main__":
    populate_data()

