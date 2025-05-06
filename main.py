import threading

from tiny_lsm.engine import Engine


def split_args(args):
    cli_args = args.split(" ")

    action, payload = cli_args

    key, value = payload.split("%")

    uppercase = action.upper()

    if uppercase not in ("PUT", "GET"):
        raise ValueError("Invalid commands, please use PUT or GET")

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
            action, key, value = split_args(cmd)
            print(action, key, value)
            if action == "PUT":
                engine.put(key, value)
                print(f"Added {key}, {value} successfully")

            if action == "GET":
                value = engine.get(key)
                print(value)

        # else: ignore empty


if __name__ == "__main__":
    main()
