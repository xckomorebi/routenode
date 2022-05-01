from socket import *

from src.service import *

def dv_main(port, mode, dv, is_last, cost_change):
    listen_sock = socket(AF_INET, SOCK_DGRAM)
    listen_sock.bind(("", port))

    send_sock = socket(AF_INET, SOCK_DGRAM)

    # TODO
    if cost_change:
        pass

    routing_table = build_table(dv)
    first_send = True

    # TODO
    if is_last:
        # msg = encode_msg(port, "routing_table", routing_table)
        broadcast_table(send_sock, port, dv, routing_table)
        first_send = False

    while True:
        rcv_msg = decode_msg(listen_sock.recv(2048))
        type_ = rcv_msg.pop("type_")

        if type_ == "routing_table":
            changed = update_table(dv, routing_table, rcv_msg, port)
            if changed or first_send:
                broadcast_table(send_sock, port, dv, routing_table)
                first_send = False
            if changed:
                print_table(routing_table, port)

        elif type_ == "dv_update":
            pass
        