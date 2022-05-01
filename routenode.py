import os
import argparse
from src.dv import dv_main
from src.ls import ls_main

from src.utils import *


def get_args():
    parser = argparse.ArgumentParser(
        description="""Emulation of the operation of network,
        layer protocols in a small computer network""")

    parser.add_argument("algorithm",
                        metavar="ALGO",
                        nargs=1,
                        help="dv: distance vector, ls: link state")

    parser.add_argument("mode",
                        metavar="MODE",
                        nargs=1,
                        help="r: regular, p: poison"
                        )

    parser.add_argument("update_interval",
                        metavar="INTERVAL",
                        nargs=1,
                        type=int,
                        help="an be any value")

    parser.add_argument("local_port",
                        metavar="LOCAL_PORT",
                        nargs=1,
                        type=int)
    parser.add_argument("neighbors",
                        metavar="NEIG",
                        nargs="+")

    args = parser.parse_args()

    return args


def main():
    args = get_args()
    algo = check_algo(args.algorithm[0])
    port = check_port(args.local_port[0])
    mode = check_mode(args.mode[0])
    rest = check_neis(args.neighbors)

    try:
        update_interval = int(args.update_interval[0])
    except ValueError:
        exit_msg("update_interval should be an integer!")

    if algo == "dv":
        dv_main(port, mode, *rest)
    else:
        ls_main(port, mode, update_interval, *rest)

if __name__ == "__main__":
    main()
