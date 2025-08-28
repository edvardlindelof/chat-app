import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Literal

from chat import stream


class AISDKMessagePart(BaseModel):
   type: Literal["text"]  # TODO consider supporting other part types
   text: str

class AISDKMessage(BaseModel):
   role: Literal["user", "assistant", "system"]
   parts: list[AISDKMessagePart]

class AISDKRequest(BaseModel):
    id: str
    messages: list[AISDKMessage]
    trigger: str
    first: bool = False


app = FastAPI()


@app.post("/api/chat")
async def chat(aisdk_request: AISDKRequest):
    *_, last_user_message = (m.parts[0].text for m in aisdk_request.messages if m.role == "user")
    completion_stream = stream(last_user_message)

    async def aisdk_formatted_response_stream():
        # TODO consider following the protocol more closely
        # https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocol?utm_source=chatgpt.com#data-stream-protocol
        yield f'data: {json.dumps({"type": "text-start", "id": "msg_123"})}\n\n'
        async for chunk in completion_stream:
            yield f'data: {json.dumps({"type": "text-delta", "id": "msg_123", "delta": chunk})}\n\n'

    return StreamingResponse(
        aisdk_formatted_response_stream(), headers={"x-vercel-ai-ui-message-stream": "v1"},
    )

app.mount("/", StaticFiles(directory="dist", html=True), name="static")
