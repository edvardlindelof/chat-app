# Chat App
FastAPI + React LLM chat app with conversation control fully delegated to backend

## Develop
```
npx concurrently "npm run build -- --watch" "uv run uvicorn app:app --host 0.0.0.0 --port 8000 --reload"
```
