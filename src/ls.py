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
    # print(dv)

    lsa = build_lsa(port, dv)
    nei_lsa = copy.deepcopy(lsa)

    seq_num = {str(port): 0}
    nei_seq = copy.copy(seq_num)

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

    if is_last:
        msg = mk_packet(port, "lsa", lsa, seq_num)
        broadcast_msg(send_sock, neis_set, msg)
        thread.start()
        started = True

    while True:
        raw_msg, addr = listen_sock.recvfrom(2048)
        prev_node = str(addr[1])
        rcv_msg = decode(raw_msg)

        type_ = rcv_msg.pop("type_")
        updated = False

        if type_ == "lsa":
            node_lsa = rcv_msg.get("data")
            node = rcv_msg.get("port")
            node_seq = rcv_msg.get("seq_num")

            if node_seq[node] > nei_seq.get(node, -1):
                nei_seq[node] = rcv_msg.get("seq_num")[node]
                # TODO
                # print(f"[{time.time():.3f}] LSA of node {node} with",
                #       f"sequence number {nei_seq[node]} received from Node {port}\n")
                update_lsa(nei_lsa, nei_seq, node_lsa, node_seq)
                broadcast_msg(send_sock, neis_set - set(prev_node), raw_msg)
                updated = True
            else:
                msg = f"""[{time.time():.3f}] DUPLICATE LSA packet Received, AND DROPPED:
- LSA of node {node}
- Sequence number {nei_seq[node]}
- Received from {port}\n"""

                # print(msg)

            if not started:
                thread.start()
                started = True

        elif type_ == "update_dv":
            pass

        if rcv_from_all_neis and updated:
            print_table(port, nei_lsa)

        if set(nei_seq) == node_set(nei_lsa):
            if not rcv_from_all_neis:
                print_table(port, nei_lsa)
                rcv_from_all_neis = True
