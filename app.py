from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb+srv://Test_User:testUser124@clustermdb.9ux7k.mongodb.net/?retryWrites=true&w=majority&appName=ClusterMDB')
db = client['web_analytics_dashboard']

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
    
    if result:
        return result[0]
    else:
        return {"total_sessions": 0, "total_users": 0, "avg_bounce_rate": 0}

# Sessions and Users endpoint
@app.route('/api/sessions_users', methods=['GET'])
def get_sessions_users():
    start_date = request.args.get('start_date', '2023-11-01')
    end_date = request.args.get('end_date', '2023-11-10')
    
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    result = aggregate_total_sessions_and_users(start_date, end_date)
    return jsonify(result), 200

# Traffic Sources endpoint
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
    return result if result else []

@app.route('/api/traffic_sources', methods=['GET'])
def get_traffic_sources():
    result = aggregate_traffic_sources()
    return jsonify(result), 200

# Goal Data endpoint
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
    return result[0] if result else {"total_goal_completion": 0, "total_goal_value": 0, "avg_conversion_rate": 0}

@app.route('/api/goals', methods=['GET'])
def get_goal_data():
    start_date = request.args.get('start_date', '2023-11-01')
    end_date = request.args.get('end_date', '2023-11-10')
    
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    result = aggregate_goal_data(start_date, end_date)
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)

