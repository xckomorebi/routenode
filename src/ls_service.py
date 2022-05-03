import json
import time
import heapq


def build_lsa(port, dv):
    """
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


# TODO
def update_dv(update_interval,
              send_sock,
              neis_set,
              port,
              lsa,
              seq_num):
    print_topology(port, lsa)
    while True:
        msg = mk_packet(port, "lsa", lsa, seq_num)
        broadcast_msg(send_sock, neis_set, msg)
        time.sleep(update_interval)


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
    port = data.get("port")
    # print(data.get("seq_num"))
    k, v = list(data.get("seq_num").items())[0]
    for node in neis_set:
        send_sock.sendto(msg, ("", node))
        print(
            f"[{time.time():.3f}] LSA of Node {k} with sequence number {v} sent to Node {node}\n")


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
    result = nei_lsa.get(node, {})
    result2 = {k: d for k, v in nei_lsa.items()
               for n, d in v.items() if n == node}

    result.update(result2)
    return result


def print_table(port, nei_lsa):
    # all_nodes = node_set(nei_lsa) - {str(port)}
    visited = {}

    h = []
    heapq.heappush(h, (0, str(port), None))

    while h:
        cur_dist, node, prev = heapq.heappop(h)
        if not node in visited:
            if prev == str(port):
                prev = None
            visited.update({node: (cur_dist, prev)})
            for next_node, dist in expand_node(node, nei_lsa).items():
                heapq.heappush(h, (dist + cur_dist, next_node, node))

    msg = f"[{time.time():.3f}] Node {port} Routing Table\n"
    visited.pop(str(port))

    for node, (dist, prev) in visited.items():
        if prev:
            msg += f"- ({dist}) -> Node {node} ; Next hop -> Node {prev}\n"
        else:
            msg += f"- ({dist}) -> Node {node}\n"

    print(msg)


def node_set(nei_lsa):
    result = set(nei_lsa.keys())
    for k, v in nei_lsa.items():
        result.update(set(v.keys()))

    return result
