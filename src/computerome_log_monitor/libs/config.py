import tomli
from argparse import Namespace


class Config:
    def __init__(self, args: Namespace) -> None:
        with open(args.config, "rb") as fh:
            conf_toml_dict = tomli.load(fh)
        self.auditor_emails = conf_toml_dict["auditors"]
        self.monitor_dirs = set(conf_toml_dict["monitor_dirs"])
        self.allow_uids = set(conf_toml_dict["allow_uids"])
        self.log_dir = conf_toml_dict["log_dir"]
        self.report_dir = conf_toml_dict["report_dir"]
        self.log_file_prefix = conf_toml_dict["log_file_prefix"]
        self.check_after = conf_toml_dict["check_after"]
        self.check_before = conf_toml_dict["check_before"]
        self.conf_path = args.config

        self.report_date = args.date
