from libs.config import Config
from libs.parser.log import Log
import subprocess

SUBJECT = "SOFI security incident - Data accessed"

SUBJECT_MISSING = "SOFI security incident - Missing logs"

SUBJECT_TEST = "SOFI security incident - Test"
MESSAGE_TEST = (
    "Dear auditor,\n"
    "\n"
    "This email was send to make sure the email service is working as "
    "expected.\n"
    "No furhter action is needed.\n"
)


def send_mail_to_auditors(conf: Config, unaouth: dict) -> None:
    message = create_unaouth_message(conf, unaouth)
    emails = " ".join(conf.auditor_emails)
    cmd = f"echo '{message}' | mail -s '{SUBJECT}' {emails}"

    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.SubprocessError:
        unsent_filepath = (
            f"{conf.report_dir}/unsent_security_incident_{conf.report_date}"
        )
        with open(unsent_filepath, "w") as fh:
            fh.write(create_unaouth_message(conf, unaouth))


def create_unaouth_message(conf: Config, unaouth: dict) -> str:
    message = (
        "Dear auditor,\n"
        "\n"
        f"{len(unaouth)} user(s) have accessed sensitive files.\n"
        "Below follows a list of users each with a sublist, that indicates "
        "which files the user in question has accessed.\n"
        "Please verify that the listed user(s) have legitimate interest in "
        "each of the listed files.\n"
        "\n"
    )

    for uid, log_entry in unaouth.items():
        message += "\n--------------------------------------------------\n"
        message += f"USER: {log_entry.name} USER ID: {uid}\n"
        for access in log_entry.accessed:
            message += f"\t{access}\n"
        message += "\n--------------------------------------------------\n"

    return message


def send_missing_log_mail(conf: Config, log: Log) -> None:
    emails = " ".join(conf.auditor_emails)
    message = (
        "Dear auditor,\n"
        "\n"
        "A log file is missing.\n"
        f"It was expected to be found at: {log.log_path}\n"
        "\n"
        "Possible issues:\n"
        "\t* Computerome no longer creates new logs. Contact Computerome.\n"
        "\t* Location of log directory has changed. Change the 'log_dir' \n"
        f"\t  setting in the configuration file: \n\t  {conf.conf_path}\n"
        "\t  to the new log directory.\n"
        "\n"
        "IMPORTANT: Remember to check the missing log file, when it has been "
        "found, either manually or by running 'computerome_log_monitor' with "
        "the date option."
    )
    cmd = f"echo '{message}' | mail -v -s '{SUBJECT_MISSING}' -r rkmo {emails}"
    subprocess.run(cmd, shell=True, check=True)


def send_test_mail(conf: Config) -> None:
    emails = " ".join(conf.auditor_emails)
    cmd = f"echo '{MESSAGE_TEST}' | mail -s '{SUBJECT_TEST}' {emails}"
    subprocess.run(cmd, shell=True, check=True)
