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
    # TODO investigate frontend/backend data contracts,
    # start with https://fastapi.tiangolo.com/advanced/generate-clients/
    aisdk_formatted_messages = (await request.json())["messages"]
    openai_formatted_messages = [
        # TODO consider supporting other part types than "text"
        {
            "role": m["role"],
            "content": next(p["text"] for p in m["parts"] if p["type"] == "text"),
        }
        for m in aisdk_formatted_messages
    ]
    if (await request.json()).get("first"):  # TODO delegate control to chat.py
        openai_response_stream = stream([])
    else:
        openai_response_stream = stream(openai_formatted_messages)
    async def aisdk_formatted_response_stream():
        # TODO consider following the protocol more closely
        # https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocol?utm_source=chatgpt.com#data-stream-protocol
        yield f'data: {json.dumps({"type": "text-start", "id": "msg_123"})}\n\n'
        async for chunk in openai_response_stream:
            yield f'data: {json.dumps({"type": "text-delta", "id": "msg_123", "delta": chunk})}\n\n'

    return StreamingResponse(
        aisdk_formatted_response_stream(), headers={"x-vercel-ai-ui-message-stream": "v1"},
    )

app.mount("/", StaticFiles(directory="dist", html=True), name="static")
