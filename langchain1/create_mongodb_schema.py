import json
import os
import datetime
import re
from pymongo import MongoClient
from bson import ObjectId
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# MongoDB Connection
client = MongoClient(
    'mongodb+srv://Test_User:testUser124@clustermdb.9ux7k.mongodb.net/'
    '?retryWrites=true&w=majority&appName=ClusterMDB'
)
db = client['website_analytics']

# Function to read the image analysis from the file
def read_llm_output():
    with open("element_analysis.txt", "r") as file:
        return file.read()

# Function to clean the response and extract valid JSON
def extract_json_from_response(response_text):
    try:
        # Find the first occurrence of '[' or '{'
        start = None
        for i, char in enumerate(response_text):
            if char == '[' or char == '{':
                start = i
                break
        if start is None:
            raise ValueError("No JSON object found in response.")

        # Find the last occurrence of ']' or '}'
        end = None
        for i in range(len(response_text) - 1, -1, -1):
            if response_text[i] == ']' or response_text[i] == '}':
                end = i + 1  # Include the closing bracket/brace
                break
        if end is None:
            raise ValueError("No JSON object found in response.")

        # Extract the JSON content
        json_content = response_text[start:end]

        # Debugging: Print the extracted JSON content
        print(f"Extracted JSON content for parsing:\n{json_content}")

        # Attempt to parse it
        return json.loads(json_content)
    except json.JSONDecodeError as e:
        print("Error parsing JSON content:", e)
        raise e

# Function to validate the response and ensure it is valid JSON
def validate_response(response):
    if isinstance(response, dict):
        try:
            cleaned_text = response['text']
            return extract_json_from_response(cleaned_text)
        except Exception as e:
            print(f"Error: The response does not contain valid JSON. {e}")
            raise e
    else:
        raise TypeError("The response is not in the expected dictionary format.")

# Function to use LangChain and OpenAI to parse the output into a MongoDB schema
def infer_schema_from_llm(image_analysis):
    # LangChain prompt template for generating the MongoDB schema from text
    prompt_template = PromptTemplate(
        input_variables=["image_analysis"],
        template="""
Based on the following detailed image analysis, generate a MongoDB schema.
- The schema should include the necessary collections and fields based on the analysis.
- Each collection should be represented as an object with the collection name as the key.
- Each collection object should contain a "fields" key, which is a list of field definitions.
- Each field definition should be an object with "name" and "type" keys.
- Return the schema in **valid JSON** format only. Make sure it can be parsed directly as JSON.
- No additional comments, explanations, or text. Only return valid JSON. Strictly follow this format.
Image Analysis:
{image_analysis}
        """
    )

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OpenAI API key not found in environment variable 'OPENAI_API_KEY'."
        )

    llm = ChatOpenAI(openai_api_key=api_key, model_name="gpt-4o-mini")

    # Create a chain using the new syntax
    chain = prompt_template | llm

    # Invoke the chain and get the response
    response = chain.invoke({"image_analysis": image_analysis})

    # Check the type of response
    print("Type of response:", type(response))
    print("Response:", response)

    # If response is an AIMessage, extract the content
    if hasattr(response, 'content'):
        response_text = response.content
    elif isinstance(response, str):
        response_text = response
    else:
        raise TypeError(f"Unexpected response type: {type(response)}")

    # Now pass the text to validate_response
    return validate_response({'text': response_text})

# Helper function to map the field type to a placeholder value
def handle_field_type(field_type):
    field_type_str = str(field_type).lower()
    if 'integer' in field_type_str:
        return 0
    elif 'float' in field_type_str or 'number' in field_type_str:
        return 0.0
    elif 'date' in field_type_str:
        return datetime.datetime.utcnow()
    elif 'string' in field_type_str:
        return ""
    elif 'percentage' in field_type_str:
        return 0.0  # Assuming percentage is a float
    elif 'array' in field_type_str or 'list' in field_type_str:
        return []
    elif 'object' in field_type_str:
        return {}
    elif 'objectid' in field_type_str:
        return ObjectId()
    elif 'bool' in field_type_str or 'boolean' in field_type_str:
        return False
    else:
        return None

# Function to create the MongoDB schema from the inferred structure
def create_mongodb_schema(schema):
    # Check if 'collections' is in the schema
    if 'collections' in schema:
        collections = schema['collections']
    else:
        collections = schema  # Assume schema is already a dict of collections

    if isinstance(collections, dict):
        # Handle collections as a dictionary
        for collection_name, collection_data in collections.items():
            fields = collection_data.get('fields', [])
            print(f"Creating collection: {collection_name}")
            collection_obj = db[collection_name]

            document = {}
            for field in fields:
                field_name = field.get('name')
                field_type = field.get('type', 'string')
                if not field_name:
                    continue  # Skip if field name is missing

                # Handle nested fields if field_name contains dots
                current = document
                if '.' in field_name:
                    parts = field_name.split('.')
                    for part in parts[:-1]:
                        if part not in current:
                            current[part] = {}
                        current = current[part]
                    final_field_name = parts[-1]
                    current[final_field_name] = handle_field_type(field_type)
                else:
                    current[field_name] = handle_field_type(field_type)

            try:
                result = collection_obj.insert_one(document)
                print(
                    f"Inserted document into {collection_name} with ID: "
                    f"{result.inserted_id}"
                )
            except Exception as e:
                print(f"Error inserting document into {collection_name}: {e}")
    else:
        raise ValueError("Invalid format for 'collections' in schema.")

# Function to populate realistic data for each collection using LLM
def populate_realistic_data(schema, num_documents=5):
    realistic_data = {}
    collections = schema.get('collections', schema)

    if isinstance(collections, dict):
        # Handle collections as a dictionary
        for collection_name, collection_schema in collections.items():
            print(f"Generating data for collection: {collection_name}")
            prompt_template = PromptTemplate(
                input_variables=["collection_name", "collection_schema", "num_documents"],
                template="""
Based on the following MongoDB collection schema, generate realistic and detailed sample data.
- Collection Name: {collection_name}
- Generate at least {num_documents} entries.
- **IMPORTANT:** Only output the JSON array of documents. Do not include any additional text, explanations, or formatting.
Collection Schema:
{collection_schema}
                """
            )

            api_key = os.getenv("OPENAI_API_KEY")
            llm = ChatOpenAI(openai_api_key=api_key, model_name="gpt-4")

            chain = prompt_template | llm

            collection_schema_json = json.dumps(collection_schema)

            # Invoke the chain and get the response
            response = chain.invoke({
                "collection_name": collection_name,
                "collection_schema": collection_schema_json,
                "num_documents": num_documents
            })

            # Check the type of response
            print(f"Type of response for {collection_name}:", type(response))
            print(f"Response for {collection_name}:", response)

            # If response is an AIMessage, extract the content
            if hasattr(response, 'content'):
                response_text = response.content
            elif isinstance(response, str):
                response_text = response
            else:
                raise TypeError(f"Unexpected response type for {collection_name}: {type(response)}")

            # Print the raw LLM response for debugging
            print(f"LLM Response for {collection_name}:\n{response_text}")

            # Print the repr of the response_text for debugging
            print(f"LLM Response for {collection_name} (repr):\n{repr(response_text)}")

            # Validate and parse the JSON array
            try:
                documents = extract_json_from_response(response_text)
                if not isinstance(documents, list):
                    raise ValueError("Extracted JSON is not a list of documents.")
                realistic_data[collection_name] = documents
            except Exception as e:
                print(f"Error parsing JSON for collection {collection_name}: {e}")
                continue
    else:
        raise ValueError("Invalid format for 'collections' in schema.")

    return realistic_data

# Function to insert the generated realistic data into MongoDB
def insert_realistic_data(data):
    if isinstance(data, dict):
        for collection_name, documents in data.items():
            collection = db[collection_name]
            try:
                # Ensure documents is a list
                if isinstance(documents, list) and len(documents) > 0:
                    result = collection.insert_many(documents)
                    print(
                        f"Inserted {len(result.inserted_ids)} documents into "
                        f"{collection_name}."
                    )
                else:
                    print(
                        f"Skipping {collection_name}: documents must be a "
                        "non-empty list."
                    )
            except Exception as e:
                print(f"Error inserting documents into {collection_name}: {e}")
    else:
        print("Error: Expected data to be a dictionary of collections and documents.")

# Main Execution
if __name__ == "__main__":
    print("Image analysis done, moving to creating mongodb_schema!")
    # Step 1: Read the image analysis from file
    image_analysis = read_llm_output()

    # Step 2: Use LangChain and OpenAI to infer the MongoDB schema
    print("Inferring schema from LLM...")
    schema = infer_schema_from_llm(image_analysis)

    print("Parsed JSON Schema:")
    print(json.dumps(schema, indent=2))

    # Step 3: Create MongoDB collections based on the inferred schema
    create_mongodb_schema(schema)

    # Step 4: Generate and populate realistic data based on the schema
    print("Generating realistic data...")
    realistic_data = populate_realistic_data(schema, num_documents=5)

    print("Realistic Data Generated:")
    print(json.dumps(realistic_data, indent=2))

    # Step 5: Insert the realistic data into MongoDB
    insert_realistic_data(realistic_data)

    print("MongoDB schema and realistic data have been populated successfully.")
