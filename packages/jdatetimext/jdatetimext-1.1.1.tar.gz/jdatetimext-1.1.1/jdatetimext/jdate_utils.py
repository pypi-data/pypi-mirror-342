import jdatetime
from datetime import date, datetime, timedelta
from dateutil.parser import parse
import logging

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'
_jmonths = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']


def j_start_j(date_type='day', date_value=datetime.now() ):
    '''
    It takes a datetime and date_type (day, week,...). Then it find the START date of the date_type.
    The calculation and output will be on JALAALI calendar.
    Example:
        date_type: 'year'
        date_value: 2024-11-25 10:08:50
        return: jdatetime.datetime(1403, 1, 1, 0, 0)
    :param date_type: string
    :param date_value: datetime
    :return: jdatetime
    '''
    quarter_list = [1, 4, 7, 10]
    # print(f"+++++ \n date_type: {date_type}, date_value: {date_value}")
    if type(date_value) == str:
        date_value = datetime_pattern(date_value)
        date_value_d = datetime.strptime(date_value, DATETIME_FORMAT) if date_value else False
    else:
        date_value_d = date_value

    if not date_value_d:
        return False

    jdate_value = jdatetime.datetime.fromgregorian(datetime=date_value_d)
    jdate_value_d = jdate_value
    j_year = jdate_value.year
    j_month = jdate_value.month
    j_day = jdate_value.day
    j_hour = jdate_value.hour
    j_minute = jdate_value.minute
    j_second = jdate_value.second
    if date_type == 'year':
        jdate_value_d = jdatetime.datetime(j_year, 1, 1, 0, 0)
    elif date_type == 'quarter':
        jdate_value_d = jdatetime.datetime(j_year, quarter_list[(j_month - 1) // 3], 1, 0, 0, 0)
    elif date_type == 'month':
        jdate_value_d = jdatetime.datetime(j_year, j_month, 1, 0, 0, 0)
    elif date_type == 'week':
        if jdate_value.weeknumber() != 1:
            jdate_value_d = jdatetime.datetime(j_year, j_month, j_day, 0, 0, 0) - timedelta(days=jdate_value.weekday())
        else:
            jdate_value_d = jdatetime.datetime(j_year, 1, 1, 0, 0)

    elif date_type == 'day':
        jdate_value_d = jdatetime.datetime(j_year, j_month, j_day, 0, 0, 0)
    elif date_type == 'hour':
        jdate_value_d = jdatetime.datetime(j_year, j_month, j_day, j_hour, 0, 0)
    elif date_type == 'minute':
        jdate_value_d = jdatetime.datetime(j_year, j_month, j_day, j_hour, j_minute, 0)
    elif date_type == 'second':
        jdate_value_d = jdatetime.datetime(j_year, j_month, j_day, j_hour, j_minute, j_second)
    elif date_type == '_':
        jdate_value_d = jdate_value

    return jdate_value_d

def j_start(date_type='day', date_value=datetime.now()):
    '''
    It takes a datetime and date_type (day, week,...). Then it find the START date of the date_type.
    The calculation is based on Jalaali calendar but the output will be GREGORIAN calendar
    Example:
        date_type: 'year'
        date_value: 2024-11-25 10:08:50
        return: datetime.datetime(2024, 3, 20, 0, 0)
    :param date_type: string
    :param date_value: datetime
    :return: datetime
    '''
    j_start_j_value = j_start_j(date_type, date_value)
    return j_start_j_value.togregorian() if j_start_j_value else False

def j_end_j(date_type='day', date_value=datetime.now() ):
    '''
    It takes a datetime and date_type (day, week,...). Then it find the END date of the date_type.
    The calculation and output will be on JALAALI calendar.
    Example:
        date_type: 'year'
        date_value: 2024-11-25 10:08:50
        return: jdatetime.datetime(1404, 1, 1, 0, 0)
    :param date_type: string
    :param date_value: datetime
    :return: jdatetime
    '''

    quarter_list = [1, 4, 7, 10]
    if type(date_value) == str:
        date_value = datetime_pattern(date_value)
        date_value_d = datetime.strptime(date_value, DATETIME_FORMAT) if date_value else False
    else:
        date_value_d = date_value

    if not date_value_d:
        return False

    jdate_value = jdatetime.datetime.fromgregorian(date=date_value_d)
    jdate_value_d = jdate_value
    j_year = jdate_value.year
    j_month = jdate_value.month
    j_day = jdate_value.day
    j_hour = jdate_value.hour
    j_minute = jdate_value.minute
    j_second = jdate_value.second
    if date_type == 'year':
        jdate_value_d = jdatetime.datetime(j_year + 1, 1, 1, 0, 0)
    elif date_type == 'quarter':
        j_month = quarter_list[(j_month - 1) // 3]
        if j_month < 9:
            j_month += 3
        else:
            j_month = 1
            j_year += 1
        jdate_value_d = jdatetime.datetime(j_year, j_month, 1, 0, 0, 0)
    elif date_type == 'month':
        first_day = jdatetime.datetime(j_year, j_month, 1, 0, 0, 0)
        next_month = first_day.replace(day=28) + timedelta(days=5)
        jdate_value_d = next_month.replace(day=1)
    elif date_type == 'week':
        if jdate_value_d.weeknumber() < 52:
            # TODO: The last week of a year can be share between two years. last day of the week is the last day of
            #   that year.
            #   if last day of this week has the same year record, its ok
            #   if not, find the last day of the year, then set the last day of the year as end of the week
            jdate_value_d = jdate_value_d + timedelta(days=7 - jdate_value_d.weekday())
        else:
            # TODO:
            #   find the last day of current week by finding the next week first day minus one.
            next_week_start = jdate_value_d + timedelta(days=7 - jdate_value_d.weekday())
            if next_week_start.year == j_year:
                jdate_value_d = jdate_value_d + timedelta(days=7 - jdate_value_d.weekday())
            else:
                jdate_value_d = jdatetime.datetime(j_year + 1, 1, 1, 0, 0)

    elif date_type == 'day':
        jdate_value_d = jdatetime.datetime(j_year, j_month, j_day, 0, 0, 0) + timedelta(days=1)
    elif date_type == 'hour':
        jdate_value_d = jdatetime.datetime(j_year, j_month, j_day, j_hour, 0, 0) + timedelta(hours=1)
    elif date_type == 'minute':
        jdate_value_d = jdatetime.datetime(j_year, j_month, j_day, j_hour, j_minute, 0) + timedelta(
            minutes=1)
    elif date_type == 'second':
        jdate_value_d = jdatetime.datetime(j_year, j_month, j_day, j_hour, j_minute, j_second) + timedelta(
            seconds=1)
    else:
        jdate_value_d = jdate_value

    return jdate_value_d

def j_end(date_type='day', date_value=datetime.now() ):
    '''
    It takes a datetime and date_type (day, week,...). Then it find the END date of the date_type.
    The calculation is based on Jalaali calendar but the output will be GREGORIAN calendar
    Example:
        date_type: 'year'
        date_value: 2024-11-25 10:08:50
        return: datetime.datetime(2025, 3, 21, 0, 0)
    :param date_type: string
    :param date_value: datetime
    :return: datetime
    '''
    j_end_j_value = j_end_j(date_type, date_value)
    return j_end_j_value.togregorian() if j_end_j_value else False

def j_start_end(date_type='day', date_value=datetime.now()):
    '''
    It takes a datetime and date_type (day, week,...). Then it find the START and END date of the date_type.
    The calculation is based on Jalaali calendar but the output will be GREGORIAN calendar
    Example:
        date_type: 'year'
        date_value: 2024-11-25 10:08:50
        return: (datetime.datetime(2024, 3, 20, 0, 0), datetime.datetime(2025, 3, 21, 0, 0))
    :param date_type: string
    :param date_value: datetime
    :return: (datetime, datetime)
    '''
    start_date = j_start(date_type, date_value)
    end_date = j_end(date_type, date_value)
    return (start_date, end_date)

def j_start_end_j(date_type='day', date_value=datetime.now()):
    '''
    It takes a datetime and date_type (day, week,...). Then it find the START and END date of the date_type.
    The calculation is based on Jalaali calendar but the output will be JDATETIME of JALAALI calendar
    Example:
        date_type: 'year'
        date_value: 2024-11-25 10:08:50
        return: (jdatetime.datetime(1403, 1, 1, 0, 0), jdatetime.datetime(1403, 12, 30, 23, 59, 59)) <1>

    <1>: Jalaali output is the last second ot end date. 1403-12-30 23:59:59

    :param date_type: string
    :param date_value: datetime
    :return: (datetime, datetime)
    '''
    start_date = j_start_j(date_type, date_value)
    end_date = j_end_j(date_type, date_value)
    end_date = j_end_j(date_type, date_value) - timedelta(seconds=1) if end_date else False
    return (start_date, end_date)

def j_start_end_js(date_type='day', date_value=datetime.now(), dt='datetime', format=DATETIME_FORMAT):
    '''
    It takes a datetime and date_type (day, week,...). Then it find the START and END date of the date_type.
    The calculation is based on Jalaali calendar but the output will be STRING of JALAALI calendar
    Example:
        date_type: 'year'
        date_value: 2024-11-25 10:08:50
        return: dt='date' -> ('1403-01-01', '1403-12-30') <1>
                dt=''     -> ('1403-01-01 00:00:00', '1403-12-30 23:59:59') <1>

        <1>: Jalaali output is the last second ot end date. 1403-12-30 23:59:59
    :param date_type: string
    :param date_value: datetime
    :param dt: string
    :return: (string, string)
    '''
    start_date = j_start_j(date_type, date_value)
    start_date = start_date.strftime(format) if start_date else False
    end_date = j_end_j(date_type, date_value)
    end_date = (end_date - timedelta(seconds=1)).strftime(format) if end_date else False

    return (start_date, end_date)

def jdatejs(date_value=datetime.now(), format=DATE_FORMAT):
    return j_start_end_js(date_type='day', date_value=date_value, dt='date', format=format)[0]

def jdatetimej(date_value=datetime.now()):
    return jdatetime.datetime.fromgregorian(datetime=date_value)

def jdatetimejs(date_value=datetime.now(), format=DATE_FORMAT):
    return jdatetime.datetime.fromgregorian(datetime=date_value).strftime(format)


def datetime_pattern(date_str):
    try:
        dt = parse(date_str, fuzzy=False)
        if dt:
            return dt.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        return False

def j_age(birth_date, end_date=date.today()):
    if isinstance(birth_date, date) and isinstance(end_date, date):
        return end_date.year - birth_date.year - (
                (end_date.month, end_date.day) < (birth_date.month, birth_date.day))
    else:
        logging.warning('[j_age] birth date and end date must be an instance of date')
        return 0

def j_date_period(date_type='month', duration=6, this_day=date.today(), lang='en_US', res='str'):
    """

    :param date_type: day, week, month, quarter, year
    :param duration:
    :param this_day: instance of date or datetime
    :param lang: en_US -> Gregorian , fa_IR -> Jalaali
    :param res: date -> datetime , str -> string
    :return:
    """
    data = []
    offset_days = 15
    if date_type == 'day':
        duration_days = 1
        offset_days = 0
    elif date_type == 'week':
        duration_days = 7
    elif date_type == 'month':
        duration_days = 30
    elif date_type == 'quarter':
        duration_days = 90
    elif date_type == 'year':
        duration_days = 365
    else:
        duration_days = 365

    if duration >= 0:
        start_date = j_start(date_type, this_day)
    else:
        # TODO: it might not be correct for months and leap years
        start_date = j_start(date_type, this_day + timedelta(days=duration * duration_days))
        duration = abs(duration) + 1

    for du in range(duration):
        next_start = j_start(date_type, start_date + timedelta(days=offset_days + duration_days * du))

        if res == 'date':
            data.append(next_start)
        elif lang == 'fa_IR':
            next_start = jdatejs(next_start)
            if date_type in ['day', 'week']:
                data.append(f"{next_start}")
            elif date_type in ['month',]:
                month_no = int(next_start[5:7])
                data.append(f"{next_start[:4]} {_jmonths[month_no - 1]}")
            elif date_type in ['quarter']:
                month_no =  next_start[5:7]
                if month_no == '01':
                    data.append(f"{next_start[:4]} بهار")
                if month_no == '03':
                    data.append(f"{next_start[:4]} تابستان")
                if month_no == '07':
                    data.append(f"{next_start[:4]} پاییز")
                if month_no == '10':
                    data.append(f"{next_start[:4]} زمستان")

            elif date_type == 'year':
                data.append(f"{next_start[:4]}")
        else:
            if date_type in ['day', 'week']:
                data.append(f"{next_start.year}-{next_start.month}-{next_start.day}")
            elif date_type in ['month', ]:
                data.append(f"{next_start.year}-{next_start.month}")
            elif date_type in ['quarter']:
                if next_start.month == 1:
                    data.append(f"{next_start.year} Q1")
                elif next_start.month == 4:
                    data.append(f"{next_start.year} Q2")
                elif next_start.month == 7:
                    data.append(f"{next_start.year} Q3")
                elif next_start.month == 10:
                    data.append(f"{next_start.year} Q4")
            elif date_type == 'year':
                data.append(f"{next_start.year}")
    return data