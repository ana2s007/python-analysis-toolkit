import datetime
import time

def ymdhms_to_datetime(input_str, truncate_time = False):
    d = datetime.datetime.fromtimestamp(time.mktime(time.strptime(input_str,'%Y-%m-%d %H:%M:%S')))
    return d.replace(second=0, minute=0, hour=0) if truncate_time else d
    
def ymdhms_to_epoch(input_str):
    return int(time.mktime(ymdhms_to_datetime(time.strptime(input_str, '%Y-%m-%d %H:%M:%S'))))


