from datetime import datetime


def get_timestamp():
    return datetime.now().strftime("[%H:%M]")
    # ("%Y-%m-%d %H:%M:%S")
