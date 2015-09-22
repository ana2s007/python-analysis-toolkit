import datetime
import time
import pytz
from datetime import timedelta

_THE_EPOCH = datetime.datetime.utcfromtimestamp(0)

"""
Misc
"""



"""
To datetime
"""


def ymdhms_to_datetime(input_str, truncate_time = False):
    d = datetime.datetime.fromtimestamp(time.mktime(time.strptime(input_str,'%Y-%m-%d %H:%M:%S')))
    return d.replace(second=0, minute=0, hour=0) if truncate_time else d
    
def epoch_to_datetime(input_epoch, truncate_time = False):
    d = datetime.datetime.utcfromtimestamp(input_epoch)
    return d.replace(second=0, minute=0, hour=0) if truncate_time else d

def datetime_timezone_dst_to_utc_datetime(dt, tz="US/Eastern"):
    local_dt = pytz.timezone(tz).localize(dt) #account for etc and UTC by localizing then converting to utc
    return local_dt.astimezone(pytz.utc).replace(tzinfo=None)

def datetime_in_utc_to_epoch(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return int(delta.total_seconds())
                                         
"""
To epoch int
"""
def ymdhms_to_epoch(input_str):
    return int(time.mktime(ymdhms_to_datetime(time.strptime(input_str, '%Y-%m-%d %H:%M:%S'))))

def ymdhms_timezone_dst_to_epoch(input_str,  tz="US/Eastern"):
    return datetime_in_utc_to_epoch(datetime_timezone_dst_to_utc_datetime(ymdhms_to_datetime(input_str)))
