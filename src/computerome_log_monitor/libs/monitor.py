from libs.parser.log import Log
import datetime
from libs.config import Config


def get_daily_log(conf: Config) -> Log:
    if conf.report_date is None:
        day = datetime.datetime.date(datetime.datetime.now())
        conf.report_date = day
    else:
        day = conf.report_date

    day_log_file_path = f"{conf.log_dir}/{conf.log_file_prefix}{day}"

    return Log(day_log_file_path)
