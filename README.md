RouteNode
===
__Name: Chen Xu__

__UNI: cx2255__

---

In this assignment, you will emulate the operation of network layer protocols in a small computer network. The program you write should behave like a single node in the network. You will start several nodes (instances of your program) so that they can send packets to each other as if there are links between them. Running as an independent node, your program should implement a simple version of a Distance-Vector routing protocol as well as a Link State routing protocol.


Usage:
===
```bash
$  ./routenode dv <r/p> <update-interval> <local-port> <neighbor1-port> <cost-1> <neighbor2-port> <cost-2> ... [last][cost-change]
```
Port number should be an integer between 1024 and 65535!

Mode:
===
## Distance-Vector Routing Algorithm

```python
# for node xxxx
dv = {
    <port_yyyy>: <distance>
}

# socket communication
msg_broadcast_table = {
    "type_": "routing_table"
    <port_xxxx>: {
        <port_yyyy>: {
            "prev": None,
            "distance": <distance>
        },
        <port_zzzz>: {
            "prev": <port_xxxx>,
            "distance": <distance>
        }
    }
}

msg_dv_update = {
    "type_": "dv_update",
    <port_xxxx>: {
        <port_yyyy>: <new_distance>
    }
}

```
## Link State Routing Protocol
each node keeps those tables in memeory
```python
seq_num = {
    <port_xxxx>: <no>
}

dv

lsa

nei_lsa
```


```python
msg = {
    "type_": "lsa",
    "from_": <port_xxxx>,
    "seq_num": 0,
    "data": 
}

```