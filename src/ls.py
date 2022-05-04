import os
import copy
from socket import *
from threading import Thread

from src.ls_service import *


def ls_main(port, mode, update_interval, dv, is_last, cost_change):
    if mode == "p":
        print("Link state algorithm only runs in regular mode!")
        os._exit(1)

    neis_set = set(dv.keys())

    lsa = build_lsa(port, dv)
    nei_lsa = copy.deepcopy(lsa)

    seq_num = {str(port): 0}
    nei_seq = copy.deepcopy(seq_num)

    rcv_from_all_neis = False

    send_sock = socket(AF_INET, SOCK_DGRAM)
    listen_sock = socket(AF_INET, SOCK_DGRAM)

    listen_sock.bind(("", port))

    thread = Thread(target=update_dv,
                    args=(update_interval,
                          send_sock,
                          neis_set,
                          port,
                          lsa,
                          seq_num))

    started = False

    if cost_change:
        thread2 = Thread(target=send_dv_update,
                         args=(send_sock,
                               port,
                               seq_num,
                               cost_change,
                               lsa,
                               nei_lsa,
                               nei_seq,
                               neis_set))
        thread2.start()

    if is_last:
        # msg = mk_packet(port, "lsa", lsa, seq_num)
        # broadcast_msg(send_sock, neis_set, msg)
        thread.start()
        started = True

    while True:
        raw_msg = listen_sock.recv(2048)
        rcv_msg = decode(raw_msg)

        type_ = rcv_msg.pop("type_")
        updated = False

        if type_ == "lsa":
            node_lsa = rcv_msg.get("data")
            prev_node = rcv_msg.get("port")
            node_seq = rcv_msg.get("seq_num")
            node = next(iter(node_seq.keys()))

            if node_seq[node] > nei_seq.get(node, -1):
                nei_seq[node] = rcv_msg.get("seq_num")[node]
                print(f"[{time.time():.3f}] LSA of node {node} with",
                      f"sequence number {nei_seq[node]} received from Node {port}\n")
                update_lsa(nei_lsa, nei_seq, node_lsa, node_seq)
                fwd_msg = mk_packet(port, "lsa", node_lsa, node_seq)
                broadcast_msg(send_sock, neis_set - {int(prev_node)}, fwd_msg)
                updated = True
            else:
                msg = f"""[{time.time():.3f}] DUPLICATE LSA packet Received, AND DROPPED:
- LSA of node {node}
- Sequence number {nei_seq[node]}
- Received from {port}\n"""
                print(msg)

            if not started:
                thread.start()
                started = True

        elif type_ == "update_dv":
            new_cost = rcv_msg.get("data")
            node = next(iter(rcv_msg.get("seq_num").keys()))

            k = str(port)
            v = node
            d = new_cost[k]
            if int(k) > int(v):
                k, v = v, k
            lsa[str(k)][str(v)] = d
            print(f"[{time.time():.3f}] Node {v} cost updated to {d}\n")
            print_topology(port, lsa)
            update_lsa(nei_lsa, nei_seq, lsa, {})
            print_table(port, nei_lsa)

            seq_num[str(port)] += 1
            msg = mk_packet(port, "lsa", lsa, seq_num)
            broadcast_msg(send_sock, neis_set, msg)

        if rcv_from_all_neis and updated:
            print_table(port, nei_lsa)

        if set(nei_seq) == node_set(nei_lsa):
            if not rcv_from_all_neis:
                print_table(port, nei_lsa)
                rcv_from_all_neis = True
