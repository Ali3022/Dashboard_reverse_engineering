from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB (Adjust 'localhost' and '27017' with your MongoDB URL)
client = MongoClient('mongodb+srv://Test_User:testUser124@clustermdb.9ux7k.mongodb.net/?retryWrites=true&w=majority&appName=ClusterMDB')
db = client['web_analytics_dashboard']

### 1. Total Sessions, Users, and Bounce Rate Aggregation
def aggregate_total_sessions_and_users(start_date, end_date):
    pipeline = [
        {
            "$match": {
                "date": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            }
        },
        {
            "$group": {
                "_id": None,
                "total_sessions": {"$sum": "$total_sessions"},
                "total_users": {"$sum": "$users"},
                "avg_bounce_rate": {"$avg": "$bounce_rate"}
            }
        }
    ]
    
    result = list(db.sessions_data.aggregate(pipeline))
    return result

### 2. Percentage Change from Previous Period
def aggregate_previous_period_metrics(start_date, end_date, previous_start_date, previous_end_date):
    # Get current period data
    current_period = aggregate_total_sessions_and_users(start_date, end_date)
    previous_period = aggregate_total_sessions_and_users(previous_start_date, previous_end_date)

    if current_period and previous_period:
        total_sessions_change = ((current_period[0]["total_sessions"] - previous_period[0]["total_sessions"]) / previous_period[0]["total_sessions"]) * 100
        total_users_change = ((current_period[0]["total_users"] - previous_period[0]["total_users"]) / previous_period[0]["total_users"]) * 100
        bounce_rate_change = ((current_period[0]["avg_bounce_rate"] - previous_period[0]["avg_bounce_rate"]) / previous_period[0]["avg_bounce_rate"]) * 100

        return {
            "total_sessions_change": total_sessions_change,
            "total_users_change": total_users_change,
            "bounce_rate_change": bounce_rate_change
        }

    return {}

### 3. Traffic Sources Aggregation
def aggregate_traffic_sources():
    pipeline = [
        {
            "$group": {
                "_id": "$source_name",
                "percentage": {"$avg": "$percentage"}
            }
        }
    ]
    
    result = list(db.traffic_sources.aggregate(pipeline))
    return result

### 4. Goal Data Aggregation
def aggregate_goal_data(start_date, end_date):
    pipeline = [
        {
            "$match": {
                "date": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            }
        },
        {
            "$group": {
                "_id": None,
                "total_goal_completion": {"$sum": "$goal_completion"},
                "total_goal_value": {"$sum": "$goal_value"},
                "avg_conversion_rate": {"$avg": "$conversion_rate"}
            }
        }
    ]
    
    result = list(db.goal_data.aggregate(pipeline))
    return result

# Sample calls to test the functions
if __name__ == "__main__":
    # Date ranges
    start_date = datetime(2023, 11, 1)
    end_date = datetime(2023, 11, 10)
    previous_start_date = datetime(2023, 10, 21)
    previous_end_date = datetime(2023, 10, 31)

    # Aggregate total sessions and users for the current period
    total_sessions_users = aggregate_total_sessions_and_users(start_date, end_date)
    print("Total Sessions & Users: ", total_sessions_users)
    
    # Aggregate previous period comparison
    previous_period_metrics = aggregate_previous_period_metrics(start_date, end_date, previous_start_date, previous_end_date)
    print("Previous Period Metrics: ", previous_period_metrics)
    
    # Aggregate traffic sources
    traffic_sources = aggregate_traffic_sources()
    print("Traffic Sources: ", traffic_sources)
    
    # Aggregate goal data
    goal_data = aggregate_goal_data(start_date, end_date)
    print("Goal Data: ", goal_data)

