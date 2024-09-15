import json
import os
import re
from pymongo import MongoClient
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# MongoDB Connection
client = MongoClient(
    'mongodb+srv://Test_User:testUser124@clustermdb.9ux7k.mongodb.net/'
    '?retryWrites=true&w=majority&appName=ClusterMDB'
)
db = client['website_analytics']

def get_collection_names():
    """Retrieve all collection names from the database."""
    return db.list_collection_names()

def get_collection_schema(collection_name):
    """
    Retrieve the schema of a collection.
    This function assumes that the first document in the collection is representative of the schema.
    """
    collection = db[collection_name]
    sample_document = collection.find_one()
    if not sample_document:
        return {}
    schema = {"fields": []}

    def extract_fields(document, parent_key=''):
        fields = []
        for key, value in document.items():
            if key == '_id':
                continue  # Skip the '_id' field
            field_name = f"{parent_key}.{key}" if parent_key else key
            field_type = type(value).__name__
            if isinstance(value, dict):
                fields.extend(extract_fields(value, field_name))
            elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                # Handle list of documents
                fields.extend(extract_fields(value[0], field_name))
            else:
                fields.append({"name": field_name, "type": field_type})
        return fields

    schema["fields"] = extract_fields(sample_document)
    return schema

def extract_json_from_response(response_text):
    """
    Extract valid JSON array from the response text by identifying the first valid JSON object or array.
    """
    json_match = re.search(r'(\[.*\])', response_text, re.DOTALL)
    if json_match:
        return json_match.group(1)
    return None

def generate_aggregation_pipeline(collection_name, collection_schema):
    prompt_template = PromptTemplate(
        input_variables=["collection_name", "collection_schema"],
        template="""
Based on the following MongoDB collection schema, generate an aggregation pipeline that provides useful insights into the data.
If any string fields contain date information (for example, fields with names like 'created_at', 'date', 'timestamp', etc.),
convert these string fields into MongoDB `Date` type using `$dateFromString` **only if they are not already of type `Date`**.
If a field is already of `Date` type, do not attempt to convert it again.

- Collection Name: {collection_name}
- Return the aggregation pipeline as a **valid JSON array** of pipeline stages.
- Do not include any additional text outside of the JSON array.

Collection Schema:
{collection_schema}
        """
    )

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found in environment variable 'OPENAI_API_KEY'.")

    llm = ChatOpenAI(openai_api_key=api_key, model_name="gpt-4")

    chain = prompt_template | llm

    collection_schema_json = json.dumps(collection_schema, indent=2)

    response = chain.invoke({
        "collection_name": collection_name,
        "collection_schema": collection_schema_json
    })

    response_text = response.content if hasattr(response, 'content') else response

    # Extract JSON array from the response text
    json_pipeline = extract_json_from_response(response_text)
    if not json_pipeline:
        print(f"Error: No valid JSON pipeline found in response for {collection_name}.")
        print("Response was:", response_text)
        return None

    # Parse the JSON pipeline
    try:
        pipeline = json.loads(json_pipeline)
    except json.JSONDecodeError as e:
        print(f"Error parsing aggregation pipeline for {collection_name}:", e)
        print("Response was:", json_pipeline)
        return None

    return pipeline

def run_aggregation_pipeline(collection_name, pipeline):
    collection = db[collection_name]
    results = collection.aggregate(pipeline)
    return list(results)

def main():
    collection_names = get_collection_names()

    for collection_name in collection_names:
        print(f"\nProcessing collection: {collection_name}")

        collection_schema = get_collection_schema(collection_name)
        if not collection_schema.get("fields"):
            print(f"No schema found for collection {collection_name}. Skipping.")
            continue

        print(f"Generating aggregation pipeline for {collection_name} based on model's judgment...")

        pipeline = generate_aggregation_pipeline(
            collection_name, collection_schema
        )

        if pipeline:
            print(f"Generated Aggregation Pipeline for {collection_name}:")
            print(json.dumps(pipeline, indent=2))

            try:
                results = run_aggregation_pipeline(collection_name, pipeline)
                print(f"Aggregation Results for {collection_name}:")
                for result in results:
                    print(result)
            except Exception as e:
                print(f"Error running aggregation pipeline for {collection_name}: {e}")
        else:
            print(f"Failed to generate aggregation pipeline for {collection_name}.")

if __name__ == "__main__":
    main()
