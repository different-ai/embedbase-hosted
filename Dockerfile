FROM ghcr.io/different-ai/embedbase:0.8.8-all
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y git && apt-get clean && \
    pip install -r requirements.txt && rm requirements.txt
COPY ./middlewares/auth_api_key/auth_api_key.py /app/middlewares/auth_api_key/auth_api_key.py
COPY main.py main.py

ENTRYPOINT ["docker/docker-entrypoint.sh"]
CMD ["embedbase"]