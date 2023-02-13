import os
import pytest
import requests

def test_clear():
    response = requests.get(
        "http://localhost:8000/v1/dev/clear",
        timeout=10,
    )
    assert response.status_code == 400
