LOCAL_PORT="8000"
SERVICE="embedbase-hosted"
GCLOUD_PROJECT:=$(shell gcloud config list --format 'value(core.project)' 2>/dev/null || echo "none")
LATEST_IMAGE_URL=$(shell echo "gcr.io/${GCLOUD_PROJECT}/${SERVICE}:latest")
VERSION=$(shell sed -n 's/.*image:.*:\(.*\)/\1/p' service.prod.yaml)
IMAGE_URL=$(shell echo "gcr.io/${GCLOUD_PROJECT}/${SERVICE}:${VERSION}")
REGION="us-central1"


# notify current gcp project
$(info Current GCP project: ${GCLOUD_PROJECT})

install: ## [DEVELOPMENT] Install the API dependencies
	virtualenv env; \
	. env/bin/activate; \
	pip install -r requirements.txt; \
	pip install -r requirements-test.txt
	@echo "Done, run '\033[0;31msource env/bin/activate\033[0m' to activate the virtual environment"

run:
	python3 -m uvicorn main:app --reload --port ${LOCAL_PORT}

docker/run/dev: ## [Local development] Run the development docker image.
	docker-compose -f docker-compose.yaml up --build

docker/run/prod:
	docker-compose -f docker-compose-prod.yaml up

test: ## [Local development] Run tests with pytest.
	python3 -m pytest  -s ./middlewares/auth_api_key/test_api_key.py::test_clear
	@echo "Done testing"

build: ## [Local development] Build the docker image.
	@echo "Building docker image for urls ${LATEST_IMAGE_URL} and ${IMAGE_URL}"
	docker buildx build . --platform linux/amd64 -t ${LATEST_IMAGE_URL} -f ./Dockerfile
	docker buildx build . --platform linux/amd64 -t ${IMAGE_URL} -f ./Dockerfile

push: build ## [Local development] Push the docker image to GCP.
	docker push ${IMAGE_URL}
	docker push ${LATEST_IMAGE_URL}

deploy: push ## [Local development] Deploy the Cloud run service.
	@echo "Will deploy embedbase-hosted to ${REGION} on ${GCLOUD_PROJECT}"
	gcloud run services replace ./service.prod.yaml --region ${REGION}

deploy/dev: ## [Local development] Deploy the Cloud run service.
	docker buildx build . --platform linux/amd64 -t ${LATEST_IMAGE_URL}-dev -f ./Dockerfile
	docker push ${LATEST_IMAGE_URL}-dev
	gcloud run services replace ./service.dev.yaml --region ${REGION}

scripts/users:
	python3 scripts/main.py get_users

release: ## [Local development] Release a new version of the API.
	@echo "Releasing version ${VERSION}"; \
	read -p "Commit content:" COMMIT; \
	git add .; \
	echo "Committing '${VERSION}: $$COMMIT'"; \
	git commit -m "${VERSION}: $$COMMIT"; \
	git push origin main; \
	git tag ${VERSION}; \
	git push origin ${VERSION}
	@echo "Done, check https://github.com/different-ai/embedbase-hosted/actions"

.PHONY: help

help: # Run `make help` to get help on the make commands
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'