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

## Link State Routing Protocol

Tech details
===

### msg format
```python
dv = {

}



msg = {
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

msg2 = {
    "type_": "dv_update",
    <port_xxxx>: {
        <port_yyyy>: <new_distance>
    }
}
```