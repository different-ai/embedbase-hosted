

## Usage

```bash
API_KEY="foobar"
VAULT_ID="myvault"

curl -X POST \
  https://embedbase-hosted-c6txy76x2q-uc.a.run.app/v1/${VAULT_ID}/search \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer ${API_KEY}" \
  -d '{
  "query": "Something about a red planet"
}'
```

```bash
curl -X POST \
  https://embedbase-hosted-c6txy76x2q-uc.a.run.app/v1/dev \
  -H 'Content-Type: application/json' \
  -d '{
  "documents": [
    {
      "data": "Elon is sipping a tea on Mars"
    }
  ]
}'
```

>{"message":"Only search endpoint is allowed"}



## Infra

```yaml
# config.yaml
# ...
middlewares:
  # - middlewares.endpoint
  - middlewares.auth_api_key
# ...
```

```bash
SECRET_NAME="FIREBASE_ADMIN_SERVICE_ACCOUNT"
gcloud secrets create ${SECRET_NAME} --replication-policy=automatic
gcloud secrets versions add ${SECRET_NAME} --data-file=svc.prod.json
```

```bash
SECRET_NAME="EMBEDBASE_HOSTED"
gcloud secrets create ${SECRET_NAME} --replication-policy=automatic
gcloud secrets versions add ${SECRET_NAME} --data-file=config.yaml
```

```bash
gcloud run services set-iam-policy embedbase-hosted ./policy.yaml --region us-central1
```


```bash
PROJECT_ID=$(gcloud config get-value project)

# create a service account for the cloud run runtime
gcloud iam service-accounts create ${PROJECT_ID}-cloud-run \
  --display-name "Cloud Run"

# get the service account email
RUNTIME_SVC="${PROJECT_ID}-cloud-run@${PROJECT_ID}.iam.gserviceaccount.com"

# give the service account access to the secret
gcloud secrets add-iam-policy-binding ${SECRET_NAME} \
  --member serviceAccount:${RUNTIME_SVC} \
  --role roles/secretmanager.secretAccessor

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member serviceAccount:${RUNTIME_SVC} \
  --role roles/secretmanager.secretAccessor

```

### Automatic deployment through GitHub Actions

```bash

# create service account for pushing containers to gcr
# and deploying to cloud run
gcloud iam service-accounts create cloud-run-deployer \
  --display-name "Cloud Run deployer"

# Grant the appropriate Cloud Run role
# to the service account to provide repository access
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member serviceAccount:cloud-run-deployer@${PROJECT_ID}.iam.gserviceaccount.com \
  --role roles/run.admin

# Grant the appropriate Cloud Storage role
# to the service account to provide registry access
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member serviceAccount:cloud-run-deployer@${PROJECT_ID}.iam.gserviceaccount.com \
  --role roles/storage.admin

# Service Account User
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member serviceAccount:cloud-run-deployer@${PROJECT_ID}.iam.gserviceaccount.com \
  --role roles/iam.serviceAccountUser

# get svc key
KEY_PATH="${PROJECT_ID}.cloud-run-deployer.svc.prod.json"
gcloud iam service-accounts keys create ${KEY_PATH} \
  --iam-account=cloud-run-deployer@${PROJECT_ID}.iam.gserviceaccount.com
cat ${KEY_PATH}
# copy the key to GitHub secrets as `GCP_SA_KEY_PROD`
rm -rf ${KEY_PATH}
```

## Extra ops

- [Adding new secret version](https://console.cloud.google.com/security/secret-manager/secret/EMBEDBASE_HOSTED/versions?project=embedbase)
