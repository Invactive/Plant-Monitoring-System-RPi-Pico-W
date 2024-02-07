class TimeFormat:
    TUPLE = 0
    SQL_FORMAT = 1


def getCurrentTime(format: TimeFormat, UTC_OFFSET=1):
    '''
    format specifies return value:
        TimeFormat.TUPLE for tuple format
        TimeFormat.SQL_FORMAT for SQL format
    '''
    import time
    if format == TimeFormat.TUPLE:
        return time.gmtime(time.time() + UTC_OFFSET * 3600)
    elif format == TimeFormat.SQL_FORMAT:
        return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            *time.gmtime(time.time() + UTC_OFFSET * 3600)[:6])
    else:
        print("Wrong format.")
