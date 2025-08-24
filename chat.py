from os import environ
from typing import Iterable
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


client = OpenAI(
    base_url=environ["LLM_BASE_URL"],
    api_key=environ["LLM_API_KEY"],
)
model = environ["LLM_MODEL"]

def stream(messages: Iterable[ChatCompletionMessageParam] = []) -> Iterable[str]:
    if not messages:
        yield "Hello! I'm a metal head AI who loves Ozzy Osbourne. How can I assist you today?"
        return

    system_message = "You are a concise communicator but also a metal head who loves ozzy osbourne"
    response_chunks = client.chat.completions.create(
        model=model,
        stream=True,
        messages=[{"role": "system", "content": system_message}, *messages],
    )
    for chunk in response_chunks:
        yield chunk.choices[0].delta.content or ""
