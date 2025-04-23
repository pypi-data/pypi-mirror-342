
```

agent = MongoAgent(mongoURL=..., openAI_token=..., db_name=...)
ai_query = agent.execute(prompt="show last 3 entries in logs table")
print("\n🤖 AI Response:\n", ai_query)
result = agent.execute_from_ai_query(ai_query)
print(result)
```