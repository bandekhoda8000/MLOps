# Gateway
Make sure you have traefik installed

Then you can add your rules with your services in your custom manifest:

```sh
apiVersion: traefik.containo.us/v1alpha1
kind: IngressRoute
metadata:
  name: datalake-ingress
  namespace: datalake
spec:
  entryPoints:
    - web  # traefik entrypoint
  routes:
    - match: PathPrefix(`/api/datalake/`)
      kind: Rule
      services:
        - name: datalake # name of the target svc
          port: 8000

```
