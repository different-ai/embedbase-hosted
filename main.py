from embedbase import get_app

from embedbase.settings import get_settings
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

app = app.run()
