from client import RaftLogSnapshot

def main():
    print("=== Testing Raft Log Compaction & Snapshotting ===")
    raft = RaftLogSnapshot()
    raft.append_entry(1, ("user:1", "active"))
    raft.append_entry(1, ("user:2", "pending"))
    raft.append_entry(2, ("user:3", "verified"))

    print(f"Log size before snapshot: {len(raft.log)} entries.")
    snap = raft.take_snapshot(up_to_index=2)
    print("Snapshot created:", snap)
    assert snap["last_index"] == 2
    assert len(raft.log) == 1
    assert raft.log[0][0] == 3
    print("Remaining uncompacted log entries:", raft.log)
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
