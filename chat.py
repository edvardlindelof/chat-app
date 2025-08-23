from typing import Iterable
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama',  # required but unused
)

def stream(messages: Iterable[ChatCompletionMessageParam] = []) -> Iterable[str]:
    if not messages:
        yield "Hello! I'm a metal head AI who loves Ozzy Osbourne. How can I assist you today?"
        return
    system_message = "You are a concise communicator but also a metal head who loves ozzy osbourne"
    response_chunks = client.chat.completions.create(
        model="llama3.2:3b",
        stream=True,
        messages=[{"role": "system", "content": system_message}, *messages],
    )
    for chunk in response_chunks:
        yield chunk.choices[0].delta.content or ""
