to veryfy iptables run `iptables -L -n`
install 
```sh
sudo apt install iptables-persistent -y
systemctl enable netfilter-persistent
```

set rules of ipotables (as root)
```sh
iptables -I INPUT -p tcp --dport 2379:2380 -j ACCEPT
iptables -I INPUT -p tcp --dport 6443 -j ACCEPT
iptables -I INPUT -p udp --dport 8472 -j ACCEPT
iptables -I INPUT -p tcp --dport 10250 -j ACCEPT
iptables -I INPUT -p udp --dport 51820 -j ACCEPT
iptables -I INPUT -p udp --dport 51821 -j ACCEPT
iptables -I INPUT -p tcp --dport 5001 -j ACCEPT
iptables -I INPUT -p tcp --dport 6443 -j ACCEPT
sudo netfilter-persistent save

```
restart with
```
systemctl enable nftables
systemctl restart nftables
```
verify the rules with
```sh
iptables -L INPUT -n --line-numbers
# or
nft list ruleset
```

NOTE: if there is no directory for it create one: `mkdir -p /etc/iptables` then run:
```sh
ip4tables-save > /etc/iptables/rules.v4
ip6tables-save > /etc/iptables/rules.v6
```


# K3s
#### Install with embedded SQLite
```sh
curl -sfL https://get.k3s.io | sh
```

### Install with etcd
```sh
curl -sfL https://get.k3s.io | sh -s - server --cluster-init
# add external server node 
curl -sfL https://get.k3s.io | sh -s - server --server https://<server-ip>:6443
```


### Install with external data soruce and docker as runtime:
``` sh
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--datastore-endpoint='postgres://arka:arka@127.0.0.1:5432/k3s' --write-kubeconfig-mode=644 --token=<token_from_previous_setup> --docker" sh - 
# try the permission like 600
```

### kubectl
Add to `~/.bashrc`:  `export KUBECONFIG=/etc/rancher/k3s/k3s.yaml`

Then run:
```sh
mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $USER:$USER ~/.kube/config
```
Make kubectl is working by sudo: `sudo kubectl get pods`

If `kubectl` did not work with `sudo` run: 
```sh
sudo mkdir -p /root/.kube
sudo cp /etc/rancher/k3s/k3s.yaml /root/.kube/config
```


## GPU in K3s
see https://docs.k3s.io/advanced#alternative-container-runtime-support


## Agent nodes
1. Set the IPtables on the VM
2. Get the token from server node: `sudo cat /var/lib/rancher/k3s/server/node-token`
3. Run on agent VM (with docker runtime):
```sh
curl -sfL https://get.k3s.io | K3S_URL="https://<SERVER_IP>:6443" K3S_TOKEN="<TOKEN>" sh -s - --docker
```

---
#### Uninstall with:
```
/usr/local/bin/k3s-uninstall.sh
```

## Registry Mirrors
You must change these files for mirroring the repositories(in *agent nodes* as well!):
```sh
sudo nano /etc/docker/daemon.json
```
```json                                
{
  "registry-mirrors":  ["https://docker.iranserver.com", "https://ghcr.io", "https://registry.gitlab.com"], 
}
```
Add the mirrors to k3
```sh
# sudo nano /etc/rancher/k3s/registries.yaml
# create the file if does not exist. 
mirrors:
  "*":
    endpoint:
      - https://docker.iranserver.com
      - https://ghcr.io
      - https://registry.gitlab.com
```

Then restart the services:
```sh
sudo systemctl daemon-reload
sudo systemctl restart docker k3
```

You must also enable the mirroring in *agent nodes* as well!
```
mirrors:
  docker.io:
```

# After installation
- Install this to make port-forwarding work
```
sudo apt update && sudo apt install socat -y
```


- add this to bashrc : `export KUBE_EDITOR=nano`


## Traefik

```sh 
sudo nano /var/lib/rancher/k3s/server/manifests/traefik-config.yaml
```
Then add this:
```yaml
apiVersion: helm.cattle.io/v1
kind: HelmChartConfig
metadata:
  name: traefik
  namespace: kube-system
spec:
  valuesContent: |-
    logs:
      general:
        level: DEBUG
      access:
        enabled: true
        format: json
        filepath: /var/log/traefik/access.log  # Specify the path explicitly
```
Then restart the traefik pod
You can see the pods in the file and/or stdout or the pod