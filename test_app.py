
from app import generate_answer


def test_generate_answer_function_exists():
    """Check that the answer-generation function is available."""
    assert callable(generate_answer)
