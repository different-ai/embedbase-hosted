import os
from embedbase import get_app
from embedbase.settings import get_settings_from_file
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from middlewares.auth_api_key.auth_api_key import AuthApiKey
from embedbase.database.supabase_db import Supabase
from embedbase.embedding.openai import OpenAI

config_path = "config.yaml"
SECRET_PATH = "/secrets" if os.path.exists("/secrets") else ".."
# if can't find config.yaml in .. try . now (local dev)
if not os.path.exists(os.path.join(SECRET_PATH, config_path)):
    SECRET_PATH = "."

if not os.path.exists(os.path.join(SECRET_PATH, config_path)):
    # exit process with error
    print(f"ERROR: Missing {config_path} file")

settings = get_settings_from_file(os.path.join(SECRET_PATH, config_path))


db = Supabase(settings.supabase_url, settings.supabase_key)

async def create_dataset(dataset_id: str, owner: str) -> None:
    # Check if the pair user_id - dataset_id already exists in the table
    existing_dataset = (
        db.supabase.table("datasets")
        .select("id")
        .eq("name", dataset_id)
        .eq("owner", owner)
        .execute()
        .data
    )

    # If the pair doesn't exist, create a new row in the table
    if not existing_dataset:
        await db.supabase.table("datasets").insert(
            {"name": dataset_id, "owner": owner}
        ).execute()
    else:
        print(f"Dataset with id {dataset_id} and owner {owner} already exists.")


async def auto_create_dataset(request, call_next):
    """
    Create a dataset row in the database if it doesn't exist
    in the table datasets with the pair dataset_id . user_id
    """

    dataset_id = request.path_params.get("dataset_id")
    user_id = request.scope.get("uid")

    if dataset_id and user_id:
        await create_dataset(dataset_id, user_id)

    return await call_next(request)


app = (
    get_app(settings)
    .use_embedder(OpenAI(settings.openai_api_key, settings.openai_organization))
    .use_db(db)
    .use_middleware(AuthApiKey)
    .use_middleware(auto_create_dataset)
    .use_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
)

app = app.run()


@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An error occurred in the server."},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        },
    )
