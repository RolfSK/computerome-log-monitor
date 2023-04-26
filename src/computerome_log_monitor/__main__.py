#!/usr/bin/env python3
import sys
import os.path
import datetime
from argparse import ArgumentParser
from __init__ import __version__
from libs.config import Config
from libs.monitor import get_daily_log
from libs.mailer import create_unaouth_message


CONF_FILENAME = "conf.toml"


def main():
    version = __version__

    app_dir = os.path.dirname(os.path.realpath(__file__))
    conf_default = f"{app_dir}/{CONF_FILENAME}"

    parser = ArgumentParser(allow_abbrev=False)
    parser.add_argument(
        "-c",
        "--config",
        help=f"Path to config file. Default: {conf_default}",
        default=conf_default,
        metavar="PATH",
    )
    parser.add_argument(
        "-d",
        "--date",
        help=(
            "Not yet implemented! TODO."
            "Get a full access report from a specific date. Specify date in "
            "the format YYYY-MM-DD"
        ),
        default=None,
        metavar="DATE",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__,
        help="Show program's version number and exit",
    )

    args = parser.parse_args()

    conf = Config(args)

    if datetime.datetime.now().time() < conf.check_after and conf.report_date is None:
        print(f"Not after {conf.check_after}")
        return
    elif (
        datetime.datetime.now().time() > conf.check_before and conf.report_date is None
    ):
        print(f"Not before {conf.check_before}")
        return

    log = get_daily_log(conf)
    unauthorized_access = log.collect_unauthorized_entries(conf)

    if unauthorized_access:
        print(create_unaouth_message(conf, unauthorized_access))


if __name__ == "__main__":
    sys.exit(main())
