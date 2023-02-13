import os
from typing import Tuple
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")

_IGNORED_PATHS = [
    "openapi.json",
    "redoc",
    "docs",
]

def middleware(app: FastAPI):
    @app.middleware("http")
    async def endpoint(request: Request, call_next) -> Tuple[str, str]:
        """
        Only allow calls on search endpoint
        """
        if request.scope["type"] != "http":  # pragma: no cover
            return await call_next(request)

        path_segments = request.scope["path"].split("/")
        if path_segments[-1] != "search":
            return JSONResponse(
                status_code=400,
                content={"message": "Only search endpoint is allowed"},
            )

        # in development mode, allow redoc, openapi etc
        if ENVIRONMENT == "development" and any(
            path in request.scope["path"] for path in _IGNORED_PATHS
        ):
            return await call_next(request)

        response = await call_next(request)
        return response