FROM ghcr.io/another-ai/embedbase:latest
# COPY ./middlewares/endpoint/endpoint.py /app/middlewares/endpoint.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt && rm requirements.txt
COPY ./middlewares/auth_api_key/auth_api_key.py /app/middlewares/auth_api_key.py
