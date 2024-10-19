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
`
minikube start --driver=docker
`

Step 6: Verify Installation
Check the status of your Minikube cluster:

`minikube status`

You can also verify kubectl is configured to use Minikube:

`kubectl cluster-info`

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
