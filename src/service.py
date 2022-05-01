import copy
import json
import time

DEBUG = True


def build_table(dv):
    """
    build first routing table from distance vector
    """
    result = {str(k): {"prev": None, "distance": v} for k, v in dv.items()}
    return result


def update_table(dv, routing_table, nei_table, rcv_table, port) -> bool:
    """
    Return
    ---
    changed : bool
        whether routing table is changed after receiving table
        from adjacent node
    """
    old_table = copy.copy(routing_table)
    nei_table.update(rcv_table)
    routing_table.clear()

    routing_table.update(build_table(dv))
    for node in nei_table:
        node_distance = dv[int(node)]
        node_table = copy.copy(nei_table[node])
        node_table.pop(str(port), None)

        for dest in node_table:
            distance = node_table[dest]["distance"] + node_distance
            if dest not in routing_table:
                routing_table[dest] = {
                    "prev": node,
                    "distance": distance
                }
            else:
                if distance < routing_table[dest]["distance"]:
                    routing_table[dest] = {
                        "prev": node,
                        "distance": distance
                    }

    return old_table != routing_table


def broadcast_table(sock, port, dv, routing_table):
    msg = encode_msg(port, "routing_table", routing_table)
    for node in dv:
        sock.sendto(msg, ("", node))


def send_dv_update(sock, port, cost_change):
    interval = 5 if DEBUG else 30
    time.sleep(interval)
    msg = encode_msg(port, "dv_update", cost_change)
    node = next(iter(cost_change))
    value = cost_change[node]

    sock.sendto(msg, ("", next(iter(cost_change))))
    print(f"[{time.time():.3f}] Node {node} cost updated to {value}\n")


def encode_msg(port, type_, data):
    """
    encode data to json msg

    Parameters
    ---
    port : int
        local port

    type_ : str
        "cost_change" or "routing_table"

    data : dict
        distance vector or routing table 

    Return
    ---
    msg : Byte string
    """
    msg = {
        "type_": type_,
        port: data
    }

    return json.dumps(msg).encode()


def decode_msg(msg):
    return json.loads(msg.decode())


def print_table(routing_table, port):
    """
    Format
    ---
    ```
    [1353035852.173] Node 1111 Routing Table
    - (1) -> Node 2222
    - (3) -> Node 3333; Next hop -> Node 2222
    - (8) -> Node 4444; Next hop -> Node 2222
    ```
    """

    print(f"[{time.time():.3f}] Node {port} Routing Table")
    for node in routing_table:
        dist = routing_table[node]["distance"]
        prev = routing_table[node]["prev"]
        if prev:
            print(f"- ({dist}) -> Node {node}; Next hop -> Node {prev}")
        else:
            print(f"- ({dist}) -> Node {node}")
    print()
