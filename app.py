import json
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

from chat import stream


app = FastAPI()

@app.get("/api/hello")
async def hello():
    return {"message": "Hello World from FastAPI!"}

@app.post("/chat-no-stream")
async def chat_no_stream():
    return {"text": "hello from chat"}

@app.post("/api/chat")
async def chat(request: Request):
    deepchat_formatted_messages = (await request.json())["messages"]
    openai_formatted_messages = [
        {"role": "assistant" if m["role"] == "ai" else m["role"], "content": m["text"]}
        for m in deepchat_formatted_messages
    ]
    return StreamingResponse(
        (
            f"data: {json.dumps({'text': f'{chunk}'})}\n\n"
            for chunk in stream(openai_formatted_messages)
        ),
        # TODO understand if media_type and headers are needed
        # media_type="text/event-stream"),
        # headers={
        #     "Content-Type": "text/event-stream",
        #     "Cache-Control": "no-cache",
        #     "Connection": "keep-alive",
        #     "Access-Control-Allow-Origin": "*",
        # },
    )

app.mount("/", StaticFiles(directory="dist", html=True), name="static")
