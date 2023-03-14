from embedbase.api import get_app

from embedbase.settings import get_settings

from middlewares.auth_api_key.auth_api_key import AuthApiKey

settings = get_settings()
app = get_app(settings)
app.add_middleware(AuthApiKey)