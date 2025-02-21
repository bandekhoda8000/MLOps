## Installing Helm

```sh
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```
**Caveat**: If some namespace is already created previous to installation of Helm, you have to delete it because it cannot be managed by it further

Then you have to add repositories and update them to be able to use charts.

## Add a repo
```sh
helm repo add bitnami https://charts.bitnami.com/bitnami
# check if added
helm repo list 
# update repos
helm repo update
```


## Namespacing
There shuold be a namespace per microservice-environment like `datalake-production` or `datalake-stage`

## Deploying a sample PostgreSQL pod
1. Creating the secrets in the *namespace*:
- env file:
```sh
POSTGRES_USER=datalakeuser
POSTGRES_PASSWORD=datalakepassword
```

- Having an env file, create the secrets by command:
```sh
source .env && kubectl create secret generic postgresql-secrets \
  --from-literal=POSTGRES_USER=$POSTGRES_USER \
  --from-literal=POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
  --namespace datalake
```

2. Create values file:
```yaml
auth:
  username: ""  # Leave blank since we're using an existing secret
  password: ""  # Leave blank since we're using an existing secret
  existingSecret: "postgresql-secrets"  # Reference the Kubernetes Secret
```

```
helm install datalake-postgres bitnami/postgresql --namespace datalake
```

# Creating Helm templates
Helm uses go template language to create reusable manifests
### init a repo:
```
```

### linting the template
```
helm lint chart-folder
```

If you ran into parsing error during lint stage run: 
```helm template <template-name> <charts-folder> --debug```
this will show the rendered version of that template