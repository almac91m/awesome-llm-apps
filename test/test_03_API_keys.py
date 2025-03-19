import os
import dotenv
import pytest
import truststore
from together import Together
from e2b_code_interpreter import Sandbox

# Load environment variables from .env file
dotenv.load_dotenv()
truststore.inject_into_ssl()   

@pytest.fixture
def TOGETHER_API_KEY():
    key = os.getenv('TOGETHER_API_KEY')
    return key

def test_together_key(TOGETHER_API_KEY):
    key = TOGETHER_API_KEY
    assert key, "TOGETHER_API_KEY is not set."

def test_together_request(TOGETHER_API_KEY):
    key = TOGETHER_API_KEY
    client = Together(api_key=key)

    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=[
            {
                "role": "user", 
                "content": "What are the top 3 things to do in New York?"
            }
        ],
    )
    assert response, "No response from Together AI"
    assert response.choices, "No choices in the response"
    assert response.choices[0].message.content, "No content in the response message"



@pytest.fixture
def E2B_API_KEY():
    key = os.getenv('E2B_API_KEY')
    return key


def test_E2B_key(E2B_API_KEY):
    key = E2B_API_KEY
    assert key, "TOGETHER_API_KEY is not set."


def test_E2B_sandbox(E2B_API_KEY):
    sbx = Sandbox() # By default the sandbox is alive for 5 minutes
    execution = sbx.run_code("print('hello world')") # Execute Python inside the sandbox
    assert execution.logs.stdout == ['hello world\n'], "Unexpected logs.stdout from code execution"


