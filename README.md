# LLM-Powered Intelligent Query–Retrieval API

## Architecture & Workflow

1. **Input Documents**: Accepts PDF blob URLs
2. **LLM Parser**: Extracts structured queries (GPT-4 integration ready)
3. **Embedding Search**: FAISS semantic retrieval (Pinecone pluggable)
4. **Clause Matching**: Semantic similarity + QA pipeline
5. **Logic Evaluation**: Business rules and answer finalization
6. **JSON Output**: Returns answers in requested structure

## API Documentation

**Base URL:**  
`http://localhost:8000/api/v1`

**Header:**  
`Authorization: Bearer 17a4d98258f8d7d8d27a6b78bbc43181314f83936eb11ca1a4e0d1d31e4f44ff`

**Endpoint:**  
`POST /hackrx/run`

### Request

```
{
  "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?...",
  "questions": [
    "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
    "...more questions..."
  ]
}
```

### Response

```
{
  "answers": [
    "A grace period of thirty days ...",
    "...more answers..."
  ]
}
```

## Deployment

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Run locally

```
uvicorn app.main:app --reload
```

Your API is now live at `http://localhost:8000/api/v1/hackrx/run`.

### 3. Production

- Use a process manager (gunicorn, pm2) and reverse proxy (nginx) for stability.
- For Docker:  
  - Example Dockerfile:
    ```Dockerfile
    FROM python:3.10
    WORKDIR /app
    COPY . .
    RUN pip install -r requirements.txt
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    ```
  - Build and run:  
    ```sh
    docker build -t llm-query-api .
    docker run -p 8000:8000 llm-query-api
    ```
- For cloud: Deploy on Azure Web Apps, AWS ECS, Google Cloud Run, etc.

### 4. Deploy on Railway

- Go to [Railway](https://railway.app/)
- Create New Project > Deploy from GitHub
- Add your repo
- Railway auto-detects Dockerfile and deploys
- Add `OPENAI_API_KEY` as an environment variable (Settings > Variables)
- Access at `https://your-app.up.railway.app/api/v1/hackrx/run`

### 5. Test

Use Postman, curl, or any HTTP client:

```
curl -X POST 'https://your-app.up.railway.app/api/v1/hackrx/run' \
     -H 'Authorization: Bearer 17a4d98258f8d7d8d27a6b78bbc43181314f83936eb11ca1a4e0d1d31e4f44ff' \
     -H 'Content-Type: application/json' \
     -d '{
           "documents": "https://example.com/policy.pdf",
           "questions": ["What is the coverage for flood damage?"]
         }'
```

## Extending

- Plug in Pinecone in `vector_db.py`
- Integrate GPT-4 in `llm_parser.py`
- Add PostgreSQL for audit/scoring
