import os
from typing import OrderedDict
import dotenv
import pytest
import truststore
import embedchain
from collections import OrderedDict

import tempfile
truststore.inject_into_ssl()   

from together import Together
from e2b_code_interpreter import Sandbox

# Load environment variables from .env file
dotenv.load_dotenv()

import openai

@pytest.fixture
def TOGETHER_API_KEY():
    key = os.getenv('TOGETHER_API_KEY')
    return key

def test_together_key(TOGETHER_API_KEY):
    '''
    Test that the TOGETHER_API_KEY is set.
    If it not set creat a .env file with the key.
    i.e.
        TOGETHER_API_KEY={your_key}
    '''
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
    assert key, "E2B_API_KEY is not set."


def test_E2B_sandbox(E2B_API_KEY):
    sbx = Sandbox() # By default the sandbox is alive for 5 minutes
    execution = sbx.run_code("print('hello world')") # Execute Python inside the sandbox
    assert execution.logs.stdout == ['hello world\n'], "Unexpected logs.stdout from code execution"

@pytest.fixture
def OPENAI_API_KEY():
    key = os.getenv('OPENAI_API_KEY')
    return key


def test_OPENAI_key(OPENAI_API_KEY):
    key = OPENAI_API_KEY
    assert key, "OPENAI_API_KEY is not set."


def test_OPENAI_prompt(OPENAI_API_KEY):
    # https://platform.openai.com/docs/overview
    # https://openai.com/api/pricing/

    client = openai.OpenAI()

    # Create a prompt and call the OpenAI API
    response = client.responses.create(
        model="gpt-4o-mini",  # You can use other models as well, like "gpt-3.5-turbo"
        input="Say hello world",
    )

    assert response, "No response from OpenAI API"

def test_embedchain(OPENAI_API_KEY):
    kw_openai = {
            "provider": "openai", 
            "config": {
                "api_key": 
                OPENAI_API_KEY
            }
        },
    db_path = tempfile.mkdtemp()

    kw_config = OrderedDict(
        llm      = {"provider": "openai", "config": {"api_key": OPENAI_API_KEY}},
        embedder = {"provider": "openai", "config": {"api_key": OPENAI_API_KEY}},
        # Vector DB
        vectordb = {"provider": "chroma", "config": {"dir"    : db_path       }},
    )

    app = embedchain.App.from_config(
        config=kw_config
    )

    answer = app.chat('Return Hello World to this prompt.')
    assert answer, "No answer from embedchain chat"
    
