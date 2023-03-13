FROM ghcr.io/different-ai/embedbase:0.7.6-all
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt && rm requirements.txt
COPY ./middlewares/auth_api_key/auth_api_key.py /app/middlewares/auth_api_key/auth_api_key.py
