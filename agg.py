from pymongo import MongoClient

# Establish connection to MongoDB
client = MongoClient('mongodb+srv://Test_User:testUser124@clustermdb.9ux7k.mongodb.net/?retryWrites=true&w=majority&appName=ClusterMDB')
db = client.web_analytics_dashboard

# -------------------- Aggregation Pipelines --------------------

# 1. Total Sessions
total_sessions_pipeline = [
    {
        "$group": {
            "_id": None,
            "total_sessions": { "$sum": 1 }
        }
    }
]

# 2. Bounce Rate
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

# 3. Goal Conversion Rate
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

# 4. Traffic Source Distribution
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

# 5. Geographic Distribution
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

# -------------------- Execute Aggregations and Print Results --------------------

# 1. Total Sessions
total_sessions_result = list(db.sessions.aggregate(total_sessions_pipeline))
if total_sessions_result:
    print("Total Sessions:", total_sessions_result[0]["total_sessions"])

# 2. Bounce Rate
bounce_rate_result = list(db.sessions.aggregate(bounce_rate_pipeline))
if bounce_rate_result:
    print("Bounce Rate: {:.2f}%".format(bounce_rate_result[0]["bounce_rate"]))

# 3. Goal Conversion Rate
goal_conversion_rate_result = list(db.sessions.aggregate(goal_conversion_rate_pipeline))
if goal_conversion_rate_result:
    print("Goal Conversion Rate: {:.2f}%".format(goal_conversion_rate_result[0]["goal_conversion_rate"]))

# 4. Traffic Source Distribution
traffic_source_result = list(db.sessions.aggregate(traffic_source_pipeline))
print("Traffic Source Distribution:")
for source in traffic_source_result:
    print(f"Source: {source['source']} - Count: {source['count']} - Percentage: {source['percentage']:.2f}%")

# 5. Geographic Distribution
geographic_distribution_result = list(db.sessions.aggregate(geographic_distribution_pipeline))
print("Geographic Distribution:")
for location in geographic_distribution_result:
    print(f"Location: {location['location']} - Count: {location['count']}")

