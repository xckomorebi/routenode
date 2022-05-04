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
Port number should be an integer between 1024 and 65535

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
    <port_xxxx>: <number>
}

# for one node, xxxx is always smaller than yyyy and zzzz
lsa = {
    <port_xxxx>: {
        <port_yyyy>: <distance1>,
        <port_zzzz>: <distance2>
    }
}

# conbination of all known lsa table
nei_lsa = {
    <port_xxxx>: {
        <port_yyyy>: <distance1>,
        <port_zzzz>: <distance2>
    },
    <port_yyyy>: {
        <port_zzzz> <distance3>
    }
}
```


```python
msg = {
    "port": <port_xxxx>
    "type_": "lsa" or "update_dv",
    "seq_num": {
        <port_xxxx>: <num>
    },
    "data": <dict>
}
```
the `port` in msg is actually the node which send the or forward the message, the original sender information is
included in `seq_num`
