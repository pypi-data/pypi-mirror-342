from click.testing import CliRunner
from llm.cli import cli
import llm
from time import sleep
import pytest


@pytest.mark.parametrize("model_name", [
    "gemini-embedding-exp-03-07",
    "text-embedding-004",
    "embedding-001"  # Add more model variants as needed
])
def test_gemini_embed(model_name):
    model = llm.get_embedding_model(model_name)
    floats = model.embed("hello world")
    assert model._task_type == "SEMANTIC_SIMILARITY"
    assert all(isinstance(f, float) for f in floats)
    assert len(floats) == 3072
    sleep(1)

