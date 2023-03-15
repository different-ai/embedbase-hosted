FROM ghcr.io/different-ai/embedbase:0.7.7-all
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt && rm requirements.txt && \
    apt-get update && apt-get install -y git && apt-get clean
COPY ./middlewares/auth_api_key/auth_api_key.py /app/middlewares/auth_api_key/auth_api_key.py
COPY main.py main.py
CMD gunicorn -w 1 -k uvicorn.workers.UvicornWorker main:app -b 0.0.0.0:${PORT} --threads 8 --timeout 0 --log-level info