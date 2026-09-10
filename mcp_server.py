import sys
import json
from client import RaftLogSnapshot

raft = RaftLogSnapshot()

def handle_call(name, arguments):
    if name == "append":
        idx = raft.append_entry(arguments.get("term", 1), tuple(arguments["cmd"]))
        return {"index": idx, "state": raft.state_machine}
    elif name == "snapshot":
        return raft.take_snapshot(arguments["up_to_index"])
    return {"error": f"Unknown tool: {name}"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_call(req.get("name"), req.get("arguments", {}))
            print(json.dumps({"id": req.get("id"), "result": res}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
