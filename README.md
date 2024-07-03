# FinancialChatBot

1. Create **.env** file and add your OPENAI_API_KEY

2. To run chatbot API use ```docker-compose up --build```. The first run will create vectors from existing companies in folder (4 files with total ~4500 chunks). It will take about 30-40 minutes!

3. The example of queries are in the **Postman-example** folder. Initially it runs on localhost environment.

## EXAMPLES OF QUERY:
### Documents processing
- To add document with data to vectorstore (use .txt file with format as in src/company_reports!)
```
curl --location 'http://127.0.0.1:8001/api/add_docs' \
--form 'file=@"<.../.../file.txt>"'
```

- To get existing companies in DB
```
curl --location 'http://127.0.0.1:8001/api/companies'
```

- To remove company from vectorstore
```
curl --location 'http://127.0.0.1:8001/api/rm_docs' \
--header 'Content-Type: application/json' \
--data '{
    "company": "<company_name>"
}'
```

### LLM functionality
LLM takes 3 agruments: chat_id, message, company (optional).

- Example 1:
```
curl --location 'http://127.0.0.1:8001/api/message' \
--header 'Content-Type: application/json' \
--data '{
    "chat_id": "00000000-0000-0000-0000-000000000000",
    "message": "Hi! How is a going? When was the highest revenue of Asgard?"
}'
```

```
curl --location 'http://127.0.0.1:8001/api/message' \
--header 'Content-Type: application/json' \
--data '{
    "chat_id": "00000000-0000-0000-0000-000000000000",
    "message": "and lowest?"
}'
```

- Example 2:
```
curl --location 'http://127.0.0.1:8001/api/message' \
--header 'Content-Type: application/json' \
--data '{
    "chat_id": "00000000-0000-0000-0000-000000000000",
    "message": "How did the company'\''s revenue compare to the industry benchmark in last twelve months?",
    "company": "Niflheim"
}'
```

- Example 3:
```
curl --location 'http://127.0.0.1:8001/api/message' \
--header 'Content-Type: application/json' \
--data '{
    "chat_id": "00000000-0000-0000-0000-000000000000",
    "message": "Hi! How is a going? What do you think about Trump?"
}'
```

- Example 4:
```
curl --location 'http://127.0.0.1:8001/api/message' \
--header 'Content-Type: application/json' \
--data '{
    "chat_id": "00000000-0000-0000-0000-000000000000",
    "message": "What was the company'\''s COGS in last twelve months?",
    "company": "Midgard"
}'
```

- Example 5:
```
curl --location 'http://127.0.0.1:8001/api/message' \
--header 'Content-Type: application/json' \
--data '{
    "chat_id": "00000000-0000-0000-0000-000000000000",
    "message": "How did the company'\''s OPEX in Q4 2023 compare to Q3 2023??",
    "company": "Niflheim"
}'
```

- Example 6:
```
curl --location 'http://127.0.0.1:8001/api/message' \
--header 'Content-Type: application/json' \
--data '{
    "chat_id": "00000000-0000-0000-0000-000000000000",
    "message": "What was the total OPEX of the company in the 2nd half of the 2022-2023 years?",
    "company": "Niflheim"
}'
```
