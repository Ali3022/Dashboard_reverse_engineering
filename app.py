from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Establish connection to MongoDB
client = MongoClient('mongodb+srv://Test_User:testUser124@clustermdb.9ux7k.mongodb.net/?retryWrites=true&w=majority&appName=ClusterMDB')
db = client.web_analytics_dashboard

# -------------------- Aggregation Pipelines --------------------

def get_total_sessions():
    total_sessions_pipeline = [
        {
            "$group": {
                "_id": None,
                "total_sessions": { "$sum": 1 }
            }
        }
    ]
    result = list(db.sessions.aggregate(total_sessions_pipeline))
    return result[0]["total_sessions"] if result else 0


def get_bounce_rate():
    bounce_rate_pipeline = [
        {
            "$facet": {
                "total_sessions": [
                    { "$group": { "_id": None, "total": { "$sum": 1 } } }
                ],
                "bounced_sessions": [
                    { "$match": { "page_views": { "$eq": 1 } } },
                    { "$group": { "_id": None, "bounced": { "$sum": 1 } } }
                ]
            }
        },
        {
            "$project": {
                "total_sessions": { "$arrayElemAt": ["$total_sessions.total", 0] },
                "bounced_sessions": { "$arrayElemAt": ["$bounced_sessions.bounced", 0] }
            }
        },
        {
            "$project": {
                "bounce_rate": {
                    "$multiply": [
                        { "$divide": ["$bounced_sessions", "$total_sessions"] },
                        100
                    ]
                }
            }
        }
    ]
    result = list(db.sessions.aggregate(bounce_rate_pipeline))
    return result[0]["bounce_rate"] if result else 0


def get_goal_conversion_rate():
    goal_conversion_rate_pipeline = [
        {
            "$lookup": {
                "from": "goals",
                "localField": "session_id",
                "foreignField": "session_id",
                "as": "goal_data"
            }
        },
        {
            "$facet": {
                "total_sessions": [
                    { "$group": { "_id": None, "total": { "$sum": 1 } } }
                ],
                "goal_sessions": [
                    { "$match": { "goal_data": { "$ne": [] } } },
                    { "$group": { "_id": None, "goals": { "$sum": 1 } } }
                ]
            }
        },
        {
            "$project": {
                "total_sessions": { "$arrayElemAt": ["$total_sessions.total", 0] },
                "goal_sessions": { "$arrayElemAt": ["$goal_sessions.goals", 0] }
            }
        },
        {
            "$project": {
                "goal_conversion_rate": {
                    "$multiply": [
                        { "$divide": ["$goal_sessions", "$total_sessions"] },
                        100
                    ]
                }
            }
        }
    ]
    result = list(db.sessions.aggregate(goal_conversion_rate_pipeline))
    return result[0]["goal_conversion_rate"] if result else 0


def get_traffic_sources():
    traffic_source_pipeline = [
        {
            "$group": {
                "_id": "$traffic_source",
                "count": { "$sum": 1 }
            }
        },
        {
            "$group": {
                "_id": None,
                "total_sessions": { "$sum": "$count" },
                "sources": {
                    "$push": {
                        "source": "$_id",
                        "count": "$count"
                    }
                }
            }
        },
        {
            "$unwind": "$sources"
        },
        {
            "$project": {
                "_id": 0,
                "source": "$sources.source",
                "count": "$sources.count",
                "percentage": {
                    "$multiply": [
                        { "$divide": ["$sources.count", "$total_sessions"] },
                        100
                    ]
                }
            }
        }
    ]
    result = list(db.sessions.aggregate(traffic_source_pipeline))
    return result


def get_geographic_distribution():
    geographic_distribution_pipeline = [
        {
            "$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "user_id",
                "as": "user_data"
            }
        },
        {
            "$unwind": "$user_data"
        },
        {
            "$group": {
                "_id": "$user_data.location",
                "count": { "$sum": 1 }
            }
        },
        {
            "$project": {
                "_id": 0,
                "location": "$_id",
                "count": 1
            }
        }
    ]
    result = list(db.sessions.aggregate(geographic_distribution_pipeline))
    return result

# -------------------- Flask Endpoints --------------------

@app.route('/total_sessions', methods=['GET'])
def total_sessions():
    return jsonify(total_sessions=get_total_sessions())


@app.route('/bounce_rate', methods=['GET'])
def bounce_rate():
    return jsonify(bounce_rate=get_bounce_rate())


@app.route('/goal_conversion_rate', methods=['GET'])
def goal_conversion_rate():
    return jsonify(goal_conversion_rate=get_goal_conversion_rate())


@app.route('/traffic_sources', methods=['GET'])
def traffic_sources():
    return jsonify(traffic_sources=get_traffic_sources())


@app.route('/geographic_distribution', methods=['GET'])
def geographic_distribution():
    return jsonify(geographic_distribution=get_geographic_distribution())

# -------------------- Main --------------------

if __name__ == '__main__':
    app.run(debug=True)

