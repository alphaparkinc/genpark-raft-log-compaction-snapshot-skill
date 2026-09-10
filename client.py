class RaftLogSnapshot:
    """
    Raft Log Compaction & Snapshotting Engine.
    Discards applied log entries up to last_included_index.
    """
    def __init__(self):
        self.log = []
        self.last_included_index = 0
        self.last_included_term = 0
        self.state_machine = {}

    def append_entry(self, term, cmd):
        idx = self.last_included_index + len(self.log) + 1
        self.log.append((idx, term, cmd))
        k, v = cmd
        self.state_machine[k] = v
        return idx

    def take_snapshot(self, up_to_index):
        cut = -1
        for i, (idx, term, cmd) in enumerate(self.log):
            if idx == up_to_index:
                cut = i
                self.last_included_index = idx
                self.last_included_term = term
                break
        if cut != -1:
            self.log = self.log[cut + 1:]
            return {
                "last_index": self.last_included_index,
                "last_term": self.last_included_term,
                "snapshot_data": dict(self.state_machine)
            }
        return None
