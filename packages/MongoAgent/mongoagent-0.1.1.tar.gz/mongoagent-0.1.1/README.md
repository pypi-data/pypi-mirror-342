# MongoAgent 🧠🔍

**MongoAgent** is an AI-powered assistant that helps generate and execute MongoDB queries using OpenAI. It supports intelligent querying, CRUD operations, collection/documentation exploration, and metadata generation.

## ✨ Features

- Connect to MongoDB
- Auto-generate queries using OpenAI (GPT-3.5)
- CRUD operations on collections and documents
- Smart prompt handling for listing collections
- Auto-inferred schema from sample documents
- Optional verbose logging for debugging
- Extendable for aggregation and custom operations

## How to install

```
pip install MongoAgent
```
## How to use?
```
from  MongoAgent import MongoAgent

agent = MongoAgent(mongoURL=..., openAI_token=..., db_name=...)
ai_query = agent.execute(prompt="show last 3 entries in logs table")
print("\n🤖 AI Response:\n", ai_query)
result = agent.execute_from_ai_query(ai_query)
print(result)
```