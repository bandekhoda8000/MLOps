# Proxy for Docker and K3s
## Steps:
### Connect to the proxy
1. Connect to the proxy host
```bash
ssh -D 1080 -q -C -N root@<host ip>
```
This will create a socks5 proxy on port 1080 of your machine.
* Check it out with:
```sh
curl --proxy socks5h://127.0.0.1:1080 http://ipinfo.io/ip
# should return your proxy server IP
```
### Set up a privoxy server locally

2. Docker does not support socks5 proxy so we have to create another type of proxy in front of our socks5 to make this work for docker using `privoxy`:
```sh
sudo apt install privoxy -y
```
- Then run `sudo nano /etc/privoxy/config` and add this:
```sh
forward-socks5t / 127.0.0.1:1080 .
```
Then run 
```sh
sudo systemctl restart privoxy
```
Then you have a proxy on `127.0.0.1:8118` which in turn forwards the traffic to port `1080`

* Check if it is working:
```sh
netstat -tuln | grep 8118
# tcp        0      0 127.0.0.1:8118          0.0.0.0:*               LISTEN     
# tcp6       0      0 ::1:8118                :::*                    LISTEN 

curl -x http://127.0.0.1:8118 http://ipinfo.io/ip
# your proxy server IP
```
### Setting Envs

2. Set these envs
```
export HTTP_PROXY=http://127.0.0.1:8118
export HTTPS_PROXY=http://127.0.0.1:8118
export NO_PROXY=localhost,127.0.0.1,.cluster.local
```


3. Make file for changing Docker service config partially:

    ```sh
    sudo mkdir -p /etc/systemd/system/docker.service.d
    sudo nano /etc/systemd/system/docker.service.d/http-proxy.conf
    ```

Add these to http-proxy.conf:
```
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:8118"
Environment="HTTPS_PROXY=http://127.0.0.1:8118"
Environment="NO_PROXY=localhost,127.0.0.1,.cluster.local"
```


### Resatrt
4. Restart services:
```sh
sudo systemctl daemon-reload
sudo systemctl restart docker k3s
```

5. Try pulling an image and monitor traffic of your proxies
```sh
sudo tcpdump -i any port 8118 -nn
``` 
