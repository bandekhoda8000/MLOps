Running `server.yaml` story creates the file k3s
```sh
ansible-playbook -i inventory.ini server.yaml --limit workers
# then use the token of server node and run
ansible-playbook -i inventory.ini agent.yaml --limit workers

```