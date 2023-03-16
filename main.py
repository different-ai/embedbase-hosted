from embedbase import get_app

from embedbase.settings import get_settings
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from middlewares.auth_api_key.auth_api_key import AuthApiKey
from embedbase.supabase_db import Supabase

settings = get_settings()

app = (
    get_app(settings)
    .use(Supabase(settings.supabase_url, settings.supabase_key))
    .use(AuthApiKey)
    .use(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
)


@app.fastapi_app.get("/auth-health")
def health(_: Request):
    """
    Return the status of the API
    """
    app.logger.info("Auth Health check successful")

    return JSONResponse(status_code=200, content={})


app = app.run()
