import pytest



def test_embedchain():
    try:
        import embedchain
    except ImportError:
        pytest.fail("embedchain is not installed in the virtual environment.")

def test_openai():
    try:
        import openai
    except ImportError:
        pytest.fail("embedchain is not installed in the virtual environment.")

