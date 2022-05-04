import os
import json
import time
import heapq
import random

DEBUG = os.getenv("PA2_DEBUG", 0)


def build_lsa(port, dv):
    """
    convert distance vector from command line input
    to local lsa for the node itself
    """
    result = dict()
    for k, v in dv.items():
        p = port
        if p > k:
            p, k = k, p
        if str(p) in result:
            result[str(p)].update({str(k): v})
        else:
            result[str(p)] = {str(k): v}

    return result


def update_dv(update_interval,
              send_sock,
              neis_set,
              port,
              lsa,
              seq_num):
    """
    broadcast lsa table of the node to
    all neighbors once every update_interval

    Parameters
    ---
    update_interval : int
        from command line argument

    send_sock : socket.socket

    neis_set : set
        a set of all neighbors for this node

    port : int

    lsa : dict
        local lsa table

    seq_num : dict
        {
            <port_xxx>: seq_num
        }
    """
    print_topology(port, lsa)
    while True:
        msg = mk_packet(port, "lsa", lsa, seq_num)
        broadcast_msg(send_sock, neis_set, msg)
        time.sleep(update_interval + random.uniform(0, 1))


def send_dv_update(sock, port, seq_num, cost_change, lsa, nei_lsa, nei_seq, neis_set):
    k = str(port)
    v = next(iter(cost_change))
    d = cost_change[v]

    msg = mk_packet(port, "update_dv", cost_change, seq_num)
    sock.sendto(msg, ("", v))
    print(f"[{time.time():.3f}] Node {v} cost updated to {d}\n")

    if int(k) > v:
        k, v = v, k

    lsa[str(k)][str(v)] = d

    seq_num[str(port)] += 1
    update_lsa(nei_lsa, nei_seq, lsa, seq_num)

    msg = mk_packet(port, "lsa", lsa, seq_num)
    broadcast_msg(sock, neis_set, msg)


def mk_packet(port, type_, data, seq_num):
    msg = dict(port=str(port),
               type_=type_,
               data=data,
               seq_num=seq_num)

    return json.dumps(msg).encode()


def decode(raw_msg):
    return json.loads(raw_msg.decode())


def broadcast_msg(send_sock, neis_set, msg):
    data = decode(msg)
    # port = data.get("port")
    # print(data.get("seq_num"))
    k, v = list(data.get("seq_num").items())[0]
    for node in neis_set:
        send_sock.sendto(msg, ("", node))
        print(
            f"[{time.time():.3f}] LSA of Node {k} with",
            f"sequence number {v} sent to Node {node}\n"
            )


def update_lsa(nei_lsa, nei_seq, node_lsa, node_seq):
    nei_seq.update(node_seq)
    for k in node_lsa:
        if k in nei_lsa:
            nei_lsa[k].update(node_lsa[k])
        else:
            nei_lsa[k] = node_lsa[k]


def print_topology(port, lsa):
    msg = f"[{time.time():.3f}] Node {port} Network topology\n"
    nodes = list(lsa.keys())
    nodes.sort()

    for node in lsa:
        neis = list(lsa[node].keys())
        neis.sort()
        for nei in neis:
            msg += f"- ({lsa[node][nei]}) from Node {node} to Node {nei}\n"

    print(msg)


def expand_node(node, nei_lsa):
    """
    get the distance for one node
    """
    result = nei_lsa.get(node, {})
    result2 = {k: d for k, v in nei_lsa.items()
               for n, d in v.items() if n == node}

    result.update(result2)
    return result


def compute_routing_table(port, nei_lsa, routing_table):
    routing_table.clear()
    h = []
    heapq.heappush(h, (0, str(port), None))

    while h:
        cur_dist, node, prev = heapq.heappop(h)
        if not node in routing_table:
            if prev == str(port):
                prev = None
            routing_table.update({node: (cur_dist, prev)})
            for next_node, dist in expand_node(node, nei_lsa).items():
                heapq.heappush(h, (dist + cur_dist, next_node, node))

    routing_table.pop(str(port))


def print_table(port, nei_lsa, routing_table):
    compute_routing_table(port, nei_lsa, routing_table)

    msg = f"[{time.time():.3f}] Node {port} Routing Table\n"

    for node, (dist, prev) in routing_table.items():
        if prev:
            msg += f"- ({dist}) -> Node {node} ; Next hop -> Node {prev}\n"
        else:
            msg += f"- ({dist}) -> Node {node}\n"

    print(msg)


def node_set(nei_lsa):
    """
    Return
    ---
    result : set
        return a set of all nodes that appears
        in lsa table of all neighbors
    """
    result = set(nei_lsa.keys())
    for k, v in nei_lsa.items():
        result.update(set(v.keys()))

    return result
