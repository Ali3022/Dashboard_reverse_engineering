#!/bin/bash

# Run the Python script to analyze the image and generate the MongoDB schema
python3 image_analysis_with_langchain.py

echo "Image analysis done, moving to creating mongodb schema!"

python3 create_mongodb_schema.py

echo "Image analysis completed, and MongoDB schema created successfully."

python3 create_aggregate_pipeline.py

echo "Aggregate pipelines created successfully."

# Start the Flask API in the background using nohup to keep it running after the script ends
nohup python3 flask_api.py > flask_api.log 2>&1 &

echo "Flask API server started and running in the background."

python3 generate_dash_generator.py

echo "Dash generator created!"

python3 revised_dynamic_detailed_dash_app.py
