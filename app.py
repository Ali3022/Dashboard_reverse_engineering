from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb+srv://Test_User:testUser124@clustermdb.9ux7k.mongodb.net/?retryWrites=true&w=majority&appName=ClusterMDB')
db = client['web_analytics_db']
sessions_collection = db['sessions']
goals_collection = db['goals']
traffic_sources_collection = db['traffic_sources']

# Aggregation Pipeline: Total Sessions
def get_total_sessions_pipeline():
    pipeline = [
        {
            '$group': {
                '_id': None,
                'total_sessions': { '$sum': 1 }  # Count all sessions
            }
        }
    ]
    result = list(sessions_collection.aggregate(pipeline))
    return result[0]['total_sessions'] if result else 0

# Aggregation Pipeline: Average Bounce Rate
def get_bounce_rate_pipeline():
    pipeline = [
        {
            '$group': {
                '_id': None,
                'avg_bounce_rate': { '$avg': '$bounce_rate' }
            }
        }
    ]
    result = list(sessions_collection.aggregate(pipeline))
    return result[0]['avg_bounce_rate'] if result else 0

# Aggregation Pipeline: Traffic Sources
def get_traffic_sources_pipeline():
    pipeline = [
        {
            '$group': {
                '_id': '$traffic_source',
                'session_count': { '$sum': 1 }
            }
        }
    ]
    result = list(sessions_collection.aggregate(pipeline))
    return [{'source': r['_id'], 'sessions': r['session_count']} for r in result]

# Aggregation Pipeline: Goal Conversion Rate
def get_goal_conversion_rate_pipeline():
    pipeline = [
        {
            '$group': {
                '_id': None,
                'goal_conversion_rate': { '$avg': '$conversion_rate' }
            }
        }
    ]
    result = list(goals_collection.aggregate(pipeline))
    return result[0]['goal_conversion_rate'] if result else 0

# Aggregation Pipeline: Goal Completion Count
def get_goal_completion_pipeline():
    pipeline = [
        {
            '$group': {
                '_id': None,
                'total_goals': { '$sum': 1 }
            }
        }
    ]
    result = list(goals_collection.aggregate(pipeline))
    return result[0]['total_goals'] if result else 0


# Flask API Endpoints

# Route: Get Total Sessions
@app.route('/api/total_sessions', methods=['GET'])
def get_total_sessions():
    total_sessions = get_total_sessions_pipeline()
    return jsonify({'total_sessions': total_sessions})

# Route: Get Average Bounce Rate
@app.route('/api/bounce_rate', methods=['GET'])
def get_bounce_rate():
    avg_bounce_rate = get_bounce_rate_pipeline()
    return jsonify({'avg_bounce_rate': avg_bounce_rate})

# Route: Get Traffic Sources Breakdown
@app.route('/api/traffic_sources', methods=['GET'])
def get_traffic_sources():
    traffic_sources = get_traffic_sources_pipeline()
    return jsonify({'traffic_sources': traffic_sources})

# Route: Get Goal Conversion Rate
@app.route('/api/goal_conversion_rate', methods=['GET'])
def get_goal_conversion_rate():
    goal_conversion_rate = get_goal_conversion_rate_pipeline()
    return jsonify({'goal_conversion_rate': goal_conversion_rate})

# Route: Get Goal Completion Count
@app.route('/api/goal_completion', methods=['GET'])
def get_goal_completion():
    goal_completion = get_goal_completion_pipeline()
    return jsonify({'goal_completion': goal_completion})


if __name__ == '__main__':
    app.run(debug=True)

