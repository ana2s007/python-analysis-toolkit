from datetime import datetime
import time
import pytz
from datetime import timedelta

"""
To datetime
"""

def ymdhms_to_datetime(input_str, truncate_time = False):
    d = datetime.strptime(input_str, '%Y-%m-%d %H:%M:%S')
    return d.replace(second=0, minute=0, hour=0) if truncate_time else d
    
def epoch_to_datetime(input_epoch, truncate_time = False):
    d = datetime.utcfromtimestamp(input_epoch)
    return d.replace(second=0, minute=0, hour=0) if truncate_time else d

def datetime_timezone_dst_to_utc_datetime(dt, interpret_as_tz="US/Eastern", kill_utc_tz = True):
    tz = pytz.timezone(interpret_as_tz)
    local_dt = tz.normalize(tz.localize(dt, is_dst=None)) #raise an error on ambigous times, force caller to handle
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt.replace(tzinfo=None) if kill_utc_tz else utc_dt

def datetime_in_utc_to_epoch(dt):
    return (dt - datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
                                         
"""
To epoch int
"""
def ymdhms_to_epoch(input_str):
    return int(time.mktime(ymdhms_to_datetime(time.strptime(input_str, '%Y-%m-%d %H:%M:%S'))))

def ymdhms_timezone_dst_to_epoch(input_str,  tz="US/Eastern"):
    return datetime_in_utc_to_epoch(datetime_timezone_dst_to_utc_datetime(ymdhms_to_datetime(input_str), kill_utc_tz = False))
