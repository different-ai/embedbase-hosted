from embedbase import get_app

from embedbase.settings import get_settings
from fastapi.middleware.cors import CORSMiddleware
import supabase
from middlewares.auth_api_key.auth_api_key import AuthApiKey

settings = get_settings()
app = (
    get_app(settings)
    .use(
        supabase.client.Client(
            settings.supabase_url,
            settings.supabase_key,
        )
    )
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
