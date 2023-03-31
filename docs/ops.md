# ops

- [Adding new secret version](https://console.cloud.google.com/security/secret-manager/secret/EMBEDBASE_HOSTED/versions?project=embedbase). You should then update service.*.yaml with the new version number and deploy again.


## How to release

Bump version image in service.prod.yaml and SENTRY_RELEASE environment variable in service.prod.yaml.

Then run:

```bash
make release
```
