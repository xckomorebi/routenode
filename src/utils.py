import sys
from typing import List


PORT_MIN = 1024
PORT_MAX = 65535


def exit_msg(msg):
    print(msg)
    sys.exit(1)


def check_algo(algo):
    if not algo in ["dv", "ls"]:
        exit_msg("Algorithm should be dv(distance vector) or ls(link state)")
    return algo


def check_mode(mode):
    if not mode in ["r", "p"]:
        exit_msg("Mode should be r(regular) or p(poison)")
    return mode


def check_neis(neighbors):
    """
    convert command line arguments to dv, is_last, cost_change

    Parameters
    ---
    neighors : list[str]
        arguments passed from command line

    Returns
    ---
    dv : dict
        distance vector

    is_last : bool
        whether this node is the last node

    cost_change : dict
        whether the cost of node with highest port will
        change after 30 seconds
    """
    dv = {}
    is_last = False
    cost_change = {}

    while neighbors:
        k = neighbors.pop(0)
        if k != "last":
            v = neighbors.pop(0)
            k = check_port(k)
            try:
                v = int(v)
            except ValueError:
                exit_msg("distance should be an integer")
            dv[k] = v
        else:
            is_last = True
            if neighbors:
                v = neighbors.pop(0)
                try:
                    v = int(v)
                except ValueError:
                    exit_msg("cost_change should be an integer")
                k = max(dv)
                cost_change[k] = v

            if neighbors:
                exit_msg("there should be no more arguments after <cost_change>")

    return dv, is_last, cost_change


def check_port(port):
    msg = "Port number should be an integer between 1024 and 65535!"
    try:
        port = int(port)
    except ValueError:
        exit_msg(msg)
    if not PORT_MIN <= port <= PORT_MAX:
        exit_msg(msg)

    return port


# only for testing
if __name__ == "__main__":
    nei = ["1111", "2", "3333", "12", "2222", "4", "last", "4123"]
    print(check_neis(nei))

