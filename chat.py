from os import environ
import random
from typing import Iterable, AsyncIterable
from openai.types.chat import ChatCompletionMessageParam
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider


agent = Agent(
    model=OpenAIChatModel(
        model_name=environ["LLM_MODEL"],
        provider=OpenAIProvider(
            base_url=environ["LLM_BASE_URL"],
            api_key=environ["LLM_API_KEY"],
        ),
    ),
    system_prompt="You are a concise communicator but also a metal head who loves ozzy osbourne"
)

@agent.tool_plain
def get_the_best_cheese() -> str:
    if random.random() < 0.5:
        return "Gruyere"
    else:
        return "Comte"

conversation_history: list[ModelMessage] = []

async def stream(messages: Iterable[ChatCompletionMessageParam] = []) -> AsyncIterable[str]:
    # TODO either refactor to pass in convo history from frontend, or
    # to save it in something like a database
    global conversation_history

    if not messages:
        yield "Hello! I'm a metal head AI who loves Ozzy Osbourne. How can I assist you today?"
        return

    *_, last_user_message = (m.get("content", "") for m in messages if m.get("role") == "user")

    async with agent.run_stream(last_user_message, message_history=conversation_history) as result:
        async for text in result.stream_text(delta=True):
            yield text

        conversation_history.extend(result.new_messages())
