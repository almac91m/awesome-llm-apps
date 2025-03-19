import os
import requests
import pytest
import httpx
import ssl
import certifi
import truststore, urllib

truststore.inject_into_ssl()

url = "https://www.google.com"

def test_httpx():
    """
    Tests that `httpx` is working as expected with `truststore.inject_into_ssl()`.
    """
    
    client = httpx.Client()
    response = client.get(url)
    assert response.status_code == 200, f"Request to {url} failed. Status code: {response.status_code}"

def test_urllib():
    """
    Tests that `utllib` is working as expected with `truststore.inject_into_ssl()`.
    """
    response = urllib.request.urlopen(url)
    assert response.status == 200, f"Request to {url} failed. Status code: {response.status}"

