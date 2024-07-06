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

## Possible improvements
1. Split chat-bot service and doc-processing services. They have different logic, and consumes different resources and time.
2. Add status for doc-processing (in queue, processing, completed, failed...). This will help to monitor status via API-endpoint.
3. Add smart chunking for docs. For this case all chunks are already splitted by 'new line' into <150 tokens, but in general the text can be solid and huge.
4. Add document time-period, type of finance (i.e. COGS, Revenue etc) and probably dynamics (increase/decrease) to a separate columns, and vectorize it with company name as well.
5. For benchamarking add either web-search service, either document from benchmars agencies / API to these agencies.
6. Make parameters analysis for RAG system (select best threshold, amount of top_k chunks).
7. Analyse reranking for RAG system, i.e. 1st similarity search relying on entites like company name, period, type of finance etc and reranking directly by chunks.
