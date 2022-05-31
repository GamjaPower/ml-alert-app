from datetime import datetime
import time

def convert_ts(timestamp):
    date_format = "%Y-%m-%dT%H:%M:%S"
    return datetime.utcfromtimestamp(timestamp).strftime(date_format)

def convert_strtime(strtime):
    # return time.mktime(datetime.strptime(strtime, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple())
    return time.mktime(datetime.strptime(strtime, "%Y-%m-%dT%H:%M:%S.%f%z").timetuple())

