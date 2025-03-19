import os
import requests
import pytest
import httpx
import ssl
import certifi
import truststore, urllib

url = "https://www.google.com"

def test_example():
    """
    A simple test to check that the pytest is working as expected.
    """
    assert True
    
def test_requests():
    """
    Tests that the requests is working as expected.
    """
    response = requests.get(url)
    assert response.status_code == 200, f"Request to {url} failed. Status code: {response.status_code}"

@pytest.mark.xfail # This test is expected to fail
def test_httpx_fail():
    """
    Tests that httpx is working as expected.
    """
    client = httpx.Client()
    response = client.get(url)
    assert response.status_code == 200, f"Request to {url} failed. Status code: {response.status_code}"

@pytest.mark.xfail # This test is expected to fail
def test_urllib_fail():
    """
    Tests that urllib is working as expected.
    """
    response = urllib.request.urlopen(url)
    assert response.status == 200, f"Request to {url} failed. Status code: {response.status}"

def test_httpx_ctx():
    """
    Tests that httpx is working as expected with the truststore.
    """
    ctx = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    client = httpx.Client(verify=ctx)
    response = client.get(url)
    assert response.status_code == 200, f"Request to {url} failed. Status code: {response.status_code}"

def test_urllib_ctx():
    """
    Tests that urllib is working as expected with the truststore.
    """
    ctx = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    # Create a custom opener with the SSL context
    opener = urllib.request.build_opener(
        urllib.request.HTTPSHandler(context=ctx)
    )
    response = opener.open(url)
    assert response.status == 200, f"Request to {url} failed. Status code: {response.status}"

