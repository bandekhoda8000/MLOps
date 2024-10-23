# Installing Minikube and kubectl on Ubuntu

## Prerequisites
•  Ubuntu 18.04 or later with Docker installed on
•  A user account with sudo privileges
•  Internet connection(you may need to use a VPN)



## Step 1: Update Your System
First, update your system to ensure all packages are up to date:
```sh
sudo apt-get update
```
Step 2: Install Required Packages
Install the necessary packages for Minikube:
```
sudo apt-get install -y curl apt-transport-https
```

Step 3: Install kubectl
Download and install the latest version of kubectl:
```sh
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

OR run 
```sh
sudo snap install kubectl
```
Step 4: Install Minikube
Download and install the latest version of Minikube:

```sh
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```
Step 5: Start Minikube
Start your Minikube cluster:
`minikube start --driver=docker`

Step 6: Verify Installation
Check the status of your Minikube cluster:

`minikube status`

You can also verify kubectl is configured to use Minikube:
`
kubectl cluster-info
`

You can set the `docker` command of the current terminal window to the daemon that is running within the minikube by:
`
eval $(minikube docker-env)
`


Add this to environment varialbes(in ~/.bashrc)
```sh
export NO_PROXY=192.168.49.2,localhost,127.0.0.0/8,::1
export KUBE_EDITOR=nano

```
192.168.49.2 is IP of the kubernetes service

Step 7: Use kubectl with Minikube
You can now use kubectl to interact with your Minikube cluster. For example, to list all pods:

kubectl get pods -A

Additional Tips
•  https://www.bing.com/search?form=SKPBOT&q=Minikube%20Dashboard: You can access the Kubernetes dashboard with:

`minikube dashboard`


Feel free to ask if you have any questions or need further assistance!
## Getting node status, IP, etc.
```kubectl get nodes -o wide```

## Installing Helm

```sh
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```
**Caveat**: If some namespace is already created previous to installation of Helm, you have to delete it because it cannot be managed by it further


## Login to docker hub account
`docker login`
After the login process run:
```SH
kubectl create secret generic regcred \
--from-file=.dockerconfigjson=$HOME/.docker/config.json \
--type=kubernetes.io/dockerconfigjson
```
## kubectl useful commands
Basic Commands

```sh
kubectl cluster-info
kubectl get all
kubectl get namespaces
```
- Setting the current default namespace
```sh
kubectl config set-context --current --namespace=<namespace>
```
- Working with Pods
```sh
kubectl get pods
kubectl describe pod <POD_NAME>

# restart the deployment
kubectl delete pod <POD_NAME>

# restart all the deployments in a namespace
kubectl delete pods --all -n <namespace>

```
Working with Deployments
```sh
kubectl get deployments  ## List Deployments

# Displays detailed information about a specific deployment, including its pods, events, and current state.
kubectl describe deployment <DEPLOYMENT_NAME>

# Changes the number of replicas for a deployment, allowing you to scale it up or down based on your needs. You can turn on or shut down the pods using this command
kubectl scale deployment <DEPLOYMENT_NAME> --replicas=<NUMBER_OF_REPLICAS>
```

- Working with Services
```sh
kubectl get services
kubectl describe service <SERVICE_NAME>
```
- ConfigMaps and Secrets
`kubectl get configmaps`
`kubectl describe configmap <CONFIGMAP_NAME>`

- kubectl get secrets
`kubectl describe secret <SECRET_NAME>`

- Logs and Debugging

```
kubectl logs <POD_NAME>
kubectl logs -f <POD_NAME>
kubectl exec -it <POD_NAME> -- <COMMAND>
```

- Managing Nodes
```
kubectl get nodes
kubectl describe node <NODE_NAME>
```

- Seeing events in a namespace in real-time
```
kubectl get events --watch -n cert-manager
```

## installing nuclio
```sh
helm install nuclio \
             --set registry.pushPullUrl=https://index.docker.io/v1/ \
             --namespace nuclio \
             nuclio/nuclio

```

### Making dashboard accessible outside of the pod of nuclio
```sh 
kubectl port-forward svc/nuclio-dashboard -n nuclio 8070:8070
```
## sample nuclio function with configuration
``` python
import os

# @nuclio.configure
#
# function.yaml:
#   apiVersion: "nuclio.io/v1"
#   kind: NuclioFunction
#   metadata:
#     name: my-new-function  # Changed the function name here
#     namespace: nuclio
#   spec:
#     env:
#     - name: MY_ENV_VALUE
#       value: my value
#     handler: my_function_with_config:my_entry_point
#     runtime: python:3.8-alpine  # Specify the Python runtime version
#     triggers:
#       http:
#         kind: http
#         attributes:
#           serviceType: NodePort
#       periodic:
#         attributes:
#           interval: 3s
#         class: ""
#         kind: cron

def my_entry_point(context, event):
    # use the logger, outputting the event body
    return "HELLO WORLD"

```

write it in a file named my_function_with_config then run:
```sh
sudo nuctl deploy \
            --path . \
            --registry $(minikube ip):5000 \
            --run-registry localhost:5000
```
You can test it by sending a post requst with empty body to get HELLO WORLD as response.
`curl -X POST http://localhost:<function-port> -d '{}'`

# KubeFlow

## Installing kustomize
```sh
curl -LO "https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize/v5.0.3/kustomize_v5.0.3_linux_amd64.tar.gz"
tar -xvf kustomize_v5.0.3_linux_amd64.tar.gz
chmod +x kustomize
sudo mv kustomize /usr/local/bin/
kustomize version
```


## Installing kfctl
```sh
PLATFORM=$(uname)
export PLATFORM
mkdir -p ~/Kubeflow/bin
export KUBEFLOW_TAG=1.2.0
KUBEFLOW_BASE="https://api.github.com/repos/kubeflow/kfctl/releases"
KFCTL_URL=$(curl -s ${KUBEFLOW_BASE} | grep http | grep "${KUBEFLOW_TAG}" | grep -i "${PLATFORM}" | cut -d : -f 2,3 | tr -d '\" ' )
## you can access kfctl now

MANIFEST_BRANCH=${MANIFEST_BRANCH:-v1.2-branch}
export MANIFEST_BRANCH
MANIFEST_VERSION=${MANIFEST_VERSION:-v1.2.0}
export MANIFEST_VERSION
KF_PROJECT_NAME=${KF_PROJECT_NAME:-hello-kf-${PLATFORM}}
export KF_PROJECT_NAME

mkdir "${KF_PROJECT_NAME}"
manifest_root=https://raw.githubusercontent.com/kubeflow/manifests
FILE_NAME=kfctl_k8s_istio.${MANIFEST_VERSION}.yaml
KFDEF=${manifest_root}${MANIFEST_BRANCH}/kfdef/${FILE_NAME}
```
Manifest is the yml configurations same as docker and k8s
The MANIFEST_BRANCH variable specifies which version of Kubeflow to get based off the GitHub branch where the Kubeflow version lies and the MANIFEST_VERSION variable specifies the version on the manifest files we have.```

Start KubeFlow dashboard with command
```sh
kubectl port-forward svc/istio-ingressgateway -n istio-system 8085:80
# default credentials:
# username: user@example.com
# password: 12341234
```

## install kind
```sh
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

## Install kubeflow ml-pipeline
https://blog.min.io/setting-up-a-development-machine-with-kubeflow-pipelines-2-0-and-minio/
Start the dashboard `kubectl port-forward svc/ml-pipeline-ui -n kubeflow 8080:80`
