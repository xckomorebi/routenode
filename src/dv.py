import time
from socket import *
from threading import Thread

from src.service import *


def dv_main(port, mode, dv, is_last, cost_change):
    listen_sock = socket(AF_INET, SOCK_DGRAM)
    listen_sock.bind(("", port))

    send_sock = socket(AF_INET, SOCK_DGRAM)

    # TODO
    if cost_change:
        Thread(target=send_dv_update, args=(send_sock, port, cost_change)).start()

    nei_table = dict()
    routing_table = build_table(dv)
    first_send = True

    if is_last:
        broadcast_table(send_sock, port, dv, routing_table, None)
        first_send = False

    while True:
        raw_msg = listen_sock.recv(2048) 
        rcv_msg = decode_msg(raw_msg)
        type_ = rcv_msg.pop("type_")
        poisoned = None

        if type_ == "routing_table":
            changed, poisoned = update_table(dv, routing_table, nei_table, rcv_msg, port, mode)
            if changed or first_send:
                broadcast_table(send_sock, port, dv, routing_table, poisoned)
                first_send = False
            # if changed:
                print_table(routing_table, port)

        elif type_ == "dv_update":
            sender = next(iter(rcv_msg))
            receiver = next(iter(rcv_msg[sender]))
            dist = rcv_msg[sender][receiver]

            if str(port) == sender:
                dv[int(receiver)] = dist
                print(f"[{time.time():.3f}] Link value message received at Node {receiver} from Node {sender}\n")
            else:
                dv[int(sender)] = dist
                print(f"[{time.time():.3f}] Link value message sent from Node {sender} to Node {receiver}\n")
                send_sock.sendto(raw_msg, ("", int(sender)))

            changed, poisoned = update_table(dv, routing_table, nei_table, {}, port, mode)
            if changed:
                broadcast_table(send_sock, port, dv, routing_table, poisoned)
                print_table(routing_table, port)
