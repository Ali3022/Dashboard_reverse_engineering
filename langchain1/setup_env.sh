#!/bin/bash

# Run the Python script to analyze the image and generate the MongoDB schema
python3 image_analysis_with_langchain.py

echo "image analysis done, moving to creating mongodb_schema!"

python3 create_mongodb_schema.py

echo "Image analysis completed, and MongoDB schema created successfully."

python3 create_aggregate_pipeline.py

echo "aggregate pipelines created successfully."
