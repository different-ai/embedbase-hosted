FROM ghcr.io/another-ai/embedbase:latest
# COPY ./middlewares/endpoint/endpoint.py /app/middlewares/endpoint.py
COPY ./middlewares/auth_api_key/auth_api_key.py /app/middlewares/auth_api_key.py
