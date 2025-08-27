import pytest
from os import environ
from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.models import GPTModel
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

from chat import stream


pytest_plugins = ("pytest_asyncio",)


factual_faithulness = GEval(
    name="Factual faithfulness",
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.RETRIEVAL_CONTEXT],
    evaluation_steps=[
        "Extract claims from the actual output.",
        "Verify each claim against statements in retrieved contextual information.",
        "Identify any contradictions between claims in the output and claims in the contextual information.",
        "Heavily penalize hallucinations.",
        "Provide reasons for the faithfulness score."
    ],
    threshold=0.5,
    model=GPTModel(
        model="gpt-4o-mini",
        base_url=environ["LLM_BASE_URL"],
        _openai_api_key=environ["LLM_API_KEY"],
    ),
)

@pytest.mark.asyncio
async def test_beurre_monte_knowledge():
    """Chatbot should understand that beurre monté is the silky thing."""
    chat_input = "What do you think of beurre monte??"
    chat_output = ''.join([chunk async for chunk in stream([{"role": "user", "content": chat_input}])])
    assert_test(
        LLMTestCase(
            input=chat_input,
            actual_output=chat_output,
            retrieval_context=[
                "beurre monté is a silky sauce made by gently emulsifying butter and water",
            ]
        ),
        [factual_faithulness]
    )
