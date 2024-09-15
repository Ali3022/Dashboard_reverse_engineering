from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)


# Connect to MongoDB
client = MongoClient('mongodb+srv://Test_User:testUser124@clustermdb.9ux7k.mongodb.net/?retryWrites=true&w=majority&appName=ClusterMDB')
db = client['web_analytics_dashboard']

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the image analysis and dashboard API!"})

# Route to get visual analysis
@app.route('/visual-analysis', methods=['GET'])
def get_visual_analysis():
    try:
        with open("visual_analysis.txt", "r") as file:
            visual_analysis = file.read()
        return jsonify({"visual_analysis": visual_analysis})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to get element analysis
@app.route('/element-analysis', methods=['GET'])
def get_element_analysis():
    try:
        with open("element_analysis.txt", "r") as file:
            element_analysis = file.read()
        return jsonify({"element_analysis": element_analysis})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to query MongoDB and get aggregated dashboard data
@app.route('/dashboard', methods=['GET'])
def get_dashboard_data():
    try:
        dashboard_data = list(db['Dashboard'].find())
        for data in dashboard_data:
            data['_id'] = str(data['_id'])  # Convert ObjectId to string
        return jsonify({"dashboard_data": dashboard_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
