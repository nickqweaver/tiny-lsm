import threading
from typing import Optional, Tuple

from tiny_lsm.engine import Engine


def split_args(args) -> Tuple[str, str, Optional[str]]:
    cli_args = args.split(" ")

    action, payload = cli_args

    kv = payload.split("%")

    key = kv[0]

    value = None
    try:
        value = kv[1]
    except IndexError:
        value = None

    uppercase = action.upper()

    if uppercase not in ("PUT", "GET", "DELETE"):
        raise ValueError("Invalid commands, please use PUT, GET or DELETE")

    return (uppercase, key, value)


def main():
    print("Database Console - PUT, GET, DELETE (k, v) to modify database")

    engine = Engine()

    while True:
        cmd = input("> ").strip()
        if cmd == "quit":
            print("Shutting down...")
            engine.flush()
            print("Terminated")
            break
        elif cmd == "help":
            print("Available commands: help, quit, ...")
        elif cmd:
            # Here, parse and execute your command
            print(f"Received: {cmd}")
            tokens = cmd.split()

            key = tokens[1]
            # Multi line value
            value = " ".join(tokens[2:])
            action, key, value = split_args(cmd)
            if action == "PUT":
                engine.put(key, value)
                print(f"Added {key}, {value} successfully")

            if action == "GET":
                value = engine.get(key)
                print(f"GET {key} -> {value}")

            if action == "DELETE":
                print("Deleting item")
        # else: ignore empty


if __name__ == "__main__":
    main()
