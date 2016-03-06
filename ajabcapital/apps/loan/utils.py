from decimal import Decimal as D

from django.utils import timezone

import logging

def time_units_to_turple(digit, unit):
    #returns a tuple such us: (days, hours, minutes, seconds)
    HOUR = "LP_001"
    DAY = "LP_002"
    WEEK = "LP_003"
    MONTH = "LP_004"
    YEAR = "LP_005"

    STANDARD_DAYS_OF_A_YEAR = (((365 * 4) + 1) / D('48.0'))

    if digit > 0:
        if unit.code == HOUR:
            return (0, digit, 0, 0)
        elif unit.code == DAY:
            return (digit, 0, 0, 0)
        elif unit.code == WEEK:
            return ((digit * 7), 0, 0, 0)
        elif unit.code == MONTH:
            return ((digit * 30.5), 0, 0, 0)
        elif unit.code == YEAR:
            return ((digit * STANDARD_DAYS_OF_A_YEAR), 0, 0, 0)

def get_time_diff(later_date, past_date):
    time_diff   = later_date - past_date
    #stringify the difference and you will get something like:
    #We are interested in something like this: '2605 days, 5:50:59.571425'. 
    time_diff   = str()
    split_tuple = time_diff.split(' days, ')

    if len(split_tuple) == 2:
        (days, time) = split_tuple
    
    (hours, minutes, seconds) = time.split(":")
    (hours, minutes, seconds) = (int(days), int(hours), int(minutes), float(seconds))

    return (days, hours, minutes, seconds)
