from libs.config import Config
import subprocess
import re


class Log:
    def __init__(self, log_path: str) -> None:
        self.entries = {}
        self.log_path = log_path
        try:
            with open(log_path, "r") as fh:
                for line in fh:
                    line = line.rstrip()
                    if not line:
                        continue
                    columns = line.split("|")
                    uid = columns[1]
                    action = columns[6]
                    target_type = columns[9]
                    success = columns[7]
                    target = columns[-1]

                    entry = self.entries.get(uid, {})
                    entry_target = entry.get(target, [])
                    entry_target.append((action, target_type, success))
                    entry[target] = entry_target
                    self.entries[uid] = entry
        except FileNotFoundError:
            print("! Log not found!")

    def collect_unauthorized_entries(self, conf: Config) -> dict:
        unauthorized_entries = {}

        for uid, targets in self.entries.items():
            # Ignore all authorized ids
            if uid in conf.allow_uids:
                continue
            for target in targets:
                for monitored_dir in conf.monitor_dirs:
                    if target.startswith(monitored_dir):
                        entry = unauthorized_entries.get(uid, LogEntry(uid))
                        entry.accessed.add(target)
                        unauthorized_entries[uid] = entry

        return unauthorized_entries

    @staticmethod
    def get_username(uid: str) -> str:
        try:
            id_process = subprocess.run(
                ["id", uid], capture_output=True, check=True)
            id_name_str = id_process.stdout.decode("utf-8").split(" ")[0]
            name_match = re.match(r"uid=\d+\((.+)\)", id_name_str)
            if name_match:
                name = name_match.group(1)
            else:
                print(f"Didn't match: {id_name_str}")
                name = uid
        except subprocess.SubprocessError as e:
            raise e
            print("subprocess exception")
            name = uid
        return name


class LogEntry:
    def __init__(self, uid: str) -> None:
        self.uid = uid
        self.accessed = set()
        self.name = Log.get_username(uid)
