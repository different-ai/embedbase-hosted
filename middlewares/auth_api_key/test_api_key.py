import os
from .auth_api_key import AuthApiKey
import pytest
import requests
from fastapi import FastAPI, Request

def test_user_cannot_write_to_another_vault():
    pass # TODO
    # response = requests.get(
    #     "http://localhost:8000/v1/dev/clear",
    #     timeout=10,
    # )
    # assert response.status_code == 400

@pytest.mark.asyncio
async def test_health_is_allowed():
    m = AuthApiKey()
    r = Request(scope={"path": "health"})
    async def c():
        return "foo"
    result = await m.dispatch(r, c)
    print(result)