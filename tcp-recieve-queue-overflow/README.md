
## TCP Receive Queue Overflow

We will set up two Nginx servers on separate nodes, each supported by services.  
Then, we'll simulate a flood of TCP connections on one node, observe the relevant  
metrics on the OCP console, and witness how the Nginx server becomes inaccessible  
on the flooded node, while the other server remains accessible.

### Prerequisite

* Openshift version 4.15 with Administrator permissions with at least 2 worker nodes.
* OC binary.
* Python.

### Setup

1. Label one worker node as "target" and the other as “unaffected”.
```
oc label node <WORKER_NODE_1> node=target
oc label node <WORKER_NODE_2> node=unaffected
```

2. Create namespaces "target" and “unaffected”:
```
oc create -f namespace1.yaml

oc create -f namespace2.yaml
```

4. Create Nginx deployments and services:
```
oc create -f ngnix-deployment1.yaml
oc create -f service1.yaml
oc create -f ngnix-deployment2.yaml
oc create -f service2.yaml
```

5. Apply the `cluster-monitoring-config` configmap:
```
oc create -f monitor-config.yaml
```

6. Place the `main.py` script inside the "target" node.

### Observe before the flood

1. Verify both servers is reachable:
```
curl http://NODE_IP:NODE_PORT
```

See response:
```
"<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>"
...

```

2. Query `node_tcp_connection_states` and observe the `rx_queued_bytes`  
metric in the Observe > metrics page in the OCP console. 

### Simulating the Traffic Flood

1. ssh into the target node and run the `main.py` server
to send traffic to itself:
```
python run main.py receiver
```
And in a different session:
```
python run main.py sender
```

### Aftermath Observations


1. Observe the value of `rx_queued_bytes` on the target node.
2. Attempt to curl the Nginx server on the target node; it should fail.
3. Attempt to curl the Nginx server on the unaffected node; it should succeed.
