""" 
Generate stochastic data.
"""

import calendar
from datetime import datetime


def from_pattern(dates: list[datetime], 
                 daily_pattern=None, monthly_pattern=None, annual_pattern=None):
    """Generate a list of daily values from either a daily, monthly, or annual pattern.

    The behaviour depends on what type of pattern is supplied. 
    - Annual pattern => 
        - annual totals are disaggregated to daily by dividing by 365 or 366 as
          appropriate.
    - Monthly pattern => 
        - if 1 value is provided, it is used for every month and disaggregated
          to daily by dividing by the days in the month;
        - if 12 values are provided, each month has its own total and which is
          disaggregated to daily by dividing by the days in the month.
    - Daily pattern => 
        - if 1 value is provided, it is used for every day;
        - if 7 values are provided, they are taken to represent a week and are
          repeated accordingly;
        - if 366 values are provided, they will be taken to represent days in
          the calendar year and the last value ignored in non-leap-years.

    Annual patterns are preferred to monthly are preferred to daily. 
    Default behaviour is to fill with `1`.

    Parameters
    ----------
    dates : list of datetime
    daily_pattern : list of float, optional
        Defaults to [1].
    monthly_pattern : list of float, optional
        Defaults to [].
    annual_pattern : list of float, optional
        Defaults to [].

    Raises
    ------
    ValueError
        Invalid number of arguments provided for pattern

    Returns
    -------
    list of float
        Disaggregated pattern as daily values.
    """
    # Guard
    if len(dates) == 0:
        return []

    # Default args
    if daily_pattern is None:
        daily_pattern = [1]
    if monthly_pattern is None:
        monthly_pattern = []
    if annual_pattern is None:
        annual_pattern = []

    # Generate data
    if len(annual_pattern) > 0:
        # Annual totals disaggregated to daily
        pattern_len = len(annual_pattern)
        year0 = dates[0].year
        return [annual_pattern[(d.year - year0) % pattern_len]/(366 if calendar.isleap(d.year) else 365) for d in dates]
    elif len(monthly_pattern) > 1:
        # Monthly pattern disaggregated to daily
        if (len(monthly_pattern) == 1):
            return [monthly_pattern[0]/calendar.monthrange(d.year, d.month)[1] for d in dates]
        if (len(monthly_pattern) == 12):
            # Pattern assumed to start in January
            return [monthly_pattern[d.month - 1]/calendar.monthrange(d.year, d.month)[1] for d in dates]
        else:
            raise ValueError("Monthly pattern must have 1 or 12 values.")
    else:
        # Daily pattern
        if len(daily_pattern) == 1:
            value = daily_pattern[0]
            return [value for _ in range(len(dates))]
        elif len(daily_pattern) == 7:
            # Pattern assumed to start on Monday
            return [daily_pattern[d.weekday()] for d in dates]
        elif len(daily_pattern) == 366:
            # Pattern assumed to start on Jan 1 (non-leapyears will skip the last value)
            return [daily_pattern[d.timetuple().tm_yday - 1] for d in dates]
        else:
            raise ValueError("Daily pattern must have 1, 7 or 366 values.")
