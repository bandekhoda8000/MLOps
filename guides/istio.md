Download the compatible release
```
curl -L https://github.com/istio/istio/releases/download/1.24.3/istio-1.24.3-linux-amd64.tar.gz -o istio.tar.gz
```
Make sure file is not corrupted
```
sha256sum istio.tar.gz
```

Add istioctl to path:
```sh
export PATH=$PATH:/home/martin/istio-1.24.3/bin
# Then
source .bashrc
```

Install istio with demo profile (includes istio-ingress-gateway & egress)
```sh
istioctl install --set profile=demo -y
```

Install istio gateway
```bash
kubectl get crd gateways.gateway.networking.k8s.io &> /dev/null || \
{ kubectl kustomize "github.com/kubernetes-sigs/gateway-api/config/crd?ref=v1.2.0" | kubectl apply -f -; }
```

finally you have;
```
curl -L https://github.com/istio/istio/releases/download/1.24.3/istio-1.24.3-linux-amd64.tar.gz -o istio.tar.gz
export PATH=$PATH:/home/martin/istio-1.24.3/bin

```