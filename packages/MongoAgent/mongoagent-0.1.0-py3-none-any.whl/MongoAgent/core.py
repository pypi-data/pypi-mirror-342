import os
import json
from pymongo import MongoClient
from openai import OpenAI
from dotenv import load_dotenv
from bson.json_util import dumps  # Add this at the top of your script




load_dotenv()

class MongoAgent:
    def __init__(self, mongoURL=None, openAI_token=None, db_name=None):
        """
        Initialize MongoAgent with MongoDB and OpenAI API clients.
        """
        self.mongoURL = mongoURL or "mongodb://admin:TonY%24ta7k@192.168.101.4:27017/"
        self.openAI_token = openAI_token or os.getenv("OPENAI_API_KEY")
        self.client = MongoClient(self.mongoURL)
        self.AIclient = OpenAI(api_key=self.openAI_token)
        self.db_name = db_name

    def close_connection(self):
        """Close the MongoDB connection."""
        self.client.close()

    def list_databases(self):
        """Return a list of all available database names."""
        return self.client.list_database_names()

    def list_collections(self, db_name):
        """List all collections in a given database."""
        return self.client[db_name].list_collection_names()

    def getMetaData(self, db_name):
        """
        Return collection-wise schema (based on first sample document).
        """
        db = self.client[db_name]
        metadata = {}

        for col_name in db.list_collection_names():
            sample_doc = db[col_name].find_one()
            metadata[col_name] = list(sample_doc.keys()) if sample_doc else []

        return metadata

    def get_documentation(self, db_name, collection_name):
        """
        Return sample document and inferred schema for documentation.
        """
        collection = self.client[db_name][collection_name]
        sample = collection.find_one()
        schema = list(sample.keys()) if sample else []
        return {
            "sample_document": sample,
            "schema_fields": schema,
            "total_documents": collection.estimated_document_count()
        }

    def chat(self, prompt=None, metadata=None):
        """
        Use OpenAI to generate MongoDB query based on metadata and prompt.
        """
        system_prompt = (
            "You are an AI assistant for MongoDB query generation. "
            "Respond only with a JSON object having keys:\n\n"
            "db_name, collection_name, operation, query (optional), data (optional), update (optional), many (optional)\n\n"
            f"Metadata:\n{metadata}"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Generate mongo query for: {prompt}"}
        ]

        try:
            response = self.AIclient.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print("Chat Generation Error:", e)
            return None

    def execute(self, prompt):
        """
        High-level method to generate MongoDB query using AI from a user prompt.
        """
        db_name = self.db_name
        schema_info = self.getMetaData(db_name)
        collection_info = [{"collection": col, "fields": fields} for col, fields in schema_info.items()]
        metadata = f"DATABASE: {db_name}\nCollections and Fields: {collection_info}"

        return self.chat(prompt=prompt, metadata=metadata)

    def execute_mongo_query(
        self, db_name, collection_name, operation,
        query=None, data=None, update=None, many=False, verbose=False):
        """
        Perform supported MongoDB operations.
        """
        try:
            db = self.client[db_name]
            col = db[collection_name] if collection_name else None

            if operation == "createCollection":
                db.create_collection(collection_name)
                return f"✅ Collection '{collection_name}' created in '{db_name}'"

            elif operation == "dropCollection":
                db.drop_collection(collection_name)
                return f"🗑️ Collection '{collection_name}' dropped from '{db_name}'"

            elif operation == "find":
                result = list(col.find(query or {}))
                if verbose:
                    print(f"[FIND] {len(result)} document(s) found.")
                return result

            elif operation == "insert":
                if many:
                    return col.insert_many(data).inserted_ids
                else:
                    return col.insert_one(data).inserted_id

            elif operation == "update":
                return col.update_many(query, update).raw_result if many else col.update_one(query, update).raw_result

            elif operation == "delete":
                return col.delete_many(query).raw_result if many else col.delete_one(query).raw_result

            else:
                raise ValueError(f"Unsupported operation: {operation}")

        except Exception as e:
            print("MongoDB Error:", e)
            return None

    def execute_from_ai_query(self, ai_query: str):
        """
        Convert AI-generated JSON string into executable Mongo query.
        """
        try:
            parsed = json.loads(ai_query)
            return self.execute_mongo_query(
                db_name=parsed.get("db_name"),
                collection_name=parsed.get("collection_name"),
                operation=parsed.get("operation"),
                query=parsed.get("query"),
                data=parsed.get("data"),
                update=parsed.get("update"),
                many=parsed.get("many", False)
            )
        except json.JSONDecodeError as je:
            print("❌ JSON Parse Error:", je)
        except Exception as e:
            print("❌ Execution Error:", e)
        return None
