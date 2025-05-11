# Monitoring


## Monitoring resources with top
Run this to start metrics-server
```
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.6.1/components.yaml
```
*NOTE*: It cannot see other namespaces!


Update or install your chart:
```sh
helm upgrade --install <release name> <helm-charts-folder> --values values.yaml
```

## Grafana, Prometheus

```sh
 helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
 helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring 
```

Check its status by running:
```sh
  kubectl --namespace monitoring get pods -l "release=monitoring"
```

Get Grafana 'admin' user password by running:
```sh
  # username: admin 
  kubectl --namespace monitoring get secrets monitoring-grafana -o jsonpath="{.data.admin-password}" | base64 -d ; echo
```

Access Grafana local instance:
```sh
  export POD_NAME=$(kubectl --namespace monitoring get pod -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=monitoring" -oname)
  kubectl --namespace monitoring port-forward $POD_NAME 3000

```

```yml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: monitoring-ingress
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: web
spec:
  rules:
  - http:
      paths:
      - path: /grafana
        pathType: Prefix
        backend:
          service:
            name: grafana
            port:
              number: 80

```
Visit https://github.com/prometheus-operator/kube-prometheus for instructions on how to create & configure Alertmanager and Prometheus instances using the Operator.

* After this go to `Menu > Dashboards > +New > add the dashboard with id: 315` with `Prometheus` as data source. 
