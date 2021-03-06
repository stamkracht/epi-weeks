# -*- encoding: utf-8 -*-
from datetime import date, timedelta
from typing import Tuple, Iterator


class Week:
    """A Week object represents a week in epidemiological week calendar
    using CDC or WHO calculation method.
    """

    def __init__(self, year, week, method="cdc", validate=True):
        # type: (int, int, str, bool) -> None
        """
        :param year: epidemiological year
        :type year: int
        :param week: epidemiological week
        :type week: int
        :param method: calculation method, which may be ``cdc`` for MMWR weeks
            or ``who`` for ISO weeks (default is ``cdc``)
        :type method: str
        :param validate: check if values of year, week and method are valid
            or not (default is ``True``), and you may change it to ``False``
            only when these values are already validated.
        :type validate: bool
        """

        if validate:
            self._year = _check_year(year)
            self._method = _check_method(method)
            self._week = _check_week(self._year, week, self._method)
        else:
            self._year = year
            self._week = week
            self._method = method

    def __repr__(self):
        # type: () -> str
        class_name = self.__class__.__name__
        return "{}({}, {}, {})".format(class_name, self._year, self._week, self._method)

    def __str__(self):
        # type: () -> str
        return self.isoformat()

    def __eq__(self, other):
        # type: (object) -> bool
        if not isinstance(other, Week):
            raise TypeError("second operand must be 'Week' object")
        return self.weektuple() == other.weektuple()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        # type: (object) -> bool
        if not isinstance(other, Week):
            raise TypeError("second operand must be 'Week' object")
        return self.weektuple() > other.weektuple()

    def __ge__(self, other):
        # type: (object) -> bool
        if not isinstance(other, Week):
            raise TypeError("second operand must be 'Week' object")
        return self.weektuple() >= other.weektuple()

    def __lt__(self, other):
        # type: (object) -> bool
        if not isinstance(other, Week):
            raise TypeError("second operand must be 'Week' object")
        return self.weektuple() < other.weektuple()

    def __le__(self, other):
        # type: (object) -> bool
        if not isinstance(other, Week):
            raise TypeError("second operand must be 'Week' object")
        return self.weektuple() <= other.weektuple()

    def __add__(self, other):
        # type: (int) -> "Week"
        if not isinstance(other, int):
            raise TypeError("second operand must be 'int'")
        new_date = self.startdate() + timedelta(weeks=other)
        return Week.fromdate(new_date, self._method)

    def __sub__(self, other):
        # type: (int) -> "Week"
        if not isinstance(other, int):
            raise TypeError("second operand must be 'int'")
        return self + (-other)

    def __contains__(self, other):
        # type (date) -> bool
        if not isinstance(other, date):
            raise TypeError("tested operand must be 'date' object")
        return other in self.iterdates()

    def __hash__(self):
        return hash((self.year, self.week, self.method))

    @classmethod
    def fromdate(cls, date_obj, method="cdc"):
        # type : (date, str) -> Week
        """Construct Week object from a Gregorian date (year, month and day).

        :param date: Gregorian date
        :param method: calculation method, which may be ``cdc`` for MMWR weeks
            or ``who`` for ISO weeks (default is ``cdc``)
        :type method: str
        """
        year, month, day = date_obj.year, date_obj.month, date_obj.day
        method = _check_method(method)
        date_ordinal = date(year, month, day).toordinal()
        year_start_ordinal = _year_start(year, method)
        week = (date_ordinal - year_start_ordinal) // 7
        if week < 0:
            year -= 1
            year_start_ordinal = _year_start(year, method)
            week = (date_ordinal - year_start_ordinal) // 7
        elif week >= 52:
            year_start_ordinal = _year_start(year + 1, method)
            if date_ordinal >= year_start_ordinal:
                year += 1
                week = 0
        week += 1
        return cls(year, week, method, validate=False)

    @classmethod
    def thisweek(cls, method="cdc"):
        # type: (str) -> "Week"
        """Construct Week object from current Gregorian date.

        :param method: calculation method, which may be ``cdc`` for MMWR weeks
            or ``who`` for ISO weeks (default is ``cdc``)
        :type method: str
        """

        return cls.fromdate(date.today(), method)

    @property
    def year(self):
        # type: () -> int
        """Return year as an integer"""
        return self._year

    @property
    def week(self):
        # type: () -> int
        """Return week number as an integer"""
        return self._week

    @property
    def method(self):
        # type: () -> str
        """Return calculation method as a string"""
        return self._method

    def weektuple(self):
        # type: () ->  Tuple[int, int]
        """Return week as a tuple of (year, week)."""
        return self._year, self._week

    def isoformat(self):
        # type: () -> str
        """Return a string representing the week in compact form of ISO format
        ‘YYYYWww’.
        """
        return "{:04}W{:02}".format(self._year, self._week)

    def startdate(self):
        # type: () -> date
        """Return date for first day of week."""
        year_start_ordinal = _year_start(self._year, self._method)
        week_start_ordinal = year_start_ordinal + ((self._week - 1) * 7)
        startdate = date.fromordinal(week_start_ordinal)
        return startdate

    def enddate(self):
        # type: () -> date
        """Return date for last day of week."""
        enddate = self.startdate() + timedelta(days=6)
        return enddate

    def iterdates(self):
        # type: () -> Iterator[date]
        """Return an iterator that yield datetime.date objects for all days of
        week."""

        startdate = self.startdate()
        for day in range(0, 7):
            yield startdate + timedelta(days=day)

    def monday(self):
        d = _method_adjustment(self._method)
        return self.startdate() + timedelta(days=d)

    def tuesday(self):
        d = 1 + _method_adjustment(self._method)
        return self.startdate() + timedelta(days=d)

    def wednesday(self):
        d = 2 + _method_adjustment(self._method)
        return self.startdate() + timedelta(days=d)

    def thursday(self):
        d = 3 + _method_adjustment(self._method)
        return self.startdate() + timedelta(days=d)

    def friday(self):
        d = 4 + _method_adjustment(self._method)
        return self.startdate() + timedelta(days=d)

    def saturday(self):
        d = 5 + _method_adjustment(self._method)
        return self.startdate() + timedelta(days=d)

    def sunday(self):
        d = 0 if _method_adjustment(self._method) else 6
        return self.startdate() + timedelta(days=d)


class Year:
    """A Year object represents a year in epidemiological week calendar
    using US CDC or WHO calculation method.
    """

    def __init__(self, year, method="cdc"):
        # type: (int, str) -> None
        """
        :param year: epidemiological year
        :type year: int
        :param method: calculation method, which may be ``cdc`` for MMWR weeks
            or ``who`` for ISO weeks (default is ``cdc``)
        :type method: str
        """

        self._year = _check_year(year)
        self._method = _check_method(method)

    def __repr__(self):
        # type: () -> str
        class_name = self.__class__.__name__
        return "{}({}, {})".format(class_name, self._year, self._method)

    def __str__(self):
        # type: () -> str
        return "{:04}".format(self._year)

    @property
    def year(self):
        # type: () -> int
        """Return year as an integer"""
        return self._year

    @property
    def method(self):
        # type: () -> str
        """Return calculation method as a string"""
        return self._method

    @property
    def totalweeks(self):
        # type: () -> int
        """Return number of weeks in year as an integer"""
        return _year_total_weeks(self._year, self._method)

    def startdate(self):
        # type: () -> date
        """Return date for first day of first week of year."""
        year_start_ordinal = _year_start(self._year, self._method)
        return date.fromordinal(year_start_ordinal)

    def enddate(self):
        # type: () -> date
        """Return date for last day of last week of year."""
        year_end_ordinal = _year_start(self._year + 1, self._method) - 1
        return date.fromordinal(year_end_ordinal)

    def iterweeks(self):
        # type: ()  -> Iterator[Week]
        """Return an iterator that yield Week objects for all weeks of year."""
        for week in range(1, self.totalweeks + 1):
            yield Week(self._year, week, self._method, validate=False)


def _check_year(year):
    # type: (int) -> int
    """Check type and value of year."""
    if not isinstance(year, int):
        raise TypeError("year must be an integer")
    if not 1 <= year <= 9999:
        raise ValueError("year must be in 1..9999")
    return year


def _check_week(year, week, method):
    # type: (int, int, str) -> int
    """Check type and value of week."""
    if not isinstance(week, int):
        raise TypeError("week must be an integer")
    weeks = _year_total_weeks(year, method)
    if not 1 <= week <= weeks:
        raise ValueError("week must be in 1..{} for year".format(weeks))
    return week


def _check_method(method):
    # type: (str) -> str
    """Check type and value of calculation method."""
    if not isinstance(method, str):
        raise TypeError("method must be a string")
    method = method.lower()
    methods = ["cdc", "who"]
    if method not in methods:
        raise ValueError("method must be '{}' or '{}'".format(*methods))
    return method


def _method_adjustment(method):
    # type: (str) -> int
    """Return needed adjustment based on first day of week using given
    calculation method.
    """
    first_day = ("Mon", "Sun")
    if method.lower() == "cdc":
        return first_day.index("Sun")
    return first_day.index("Mon")


def _year_start(year, method):
    # type: (int, str) -> int
    """Return proleptic Gregorian ordinal for first day of first week for
    given year using given calculation method.
    """

    adjustment = _method_adjustment(method)
    mid_weekday = 3 - adjustment  # Sun is 6 .. Mon is 0
    jan1 = date(year, 1, 1)
    jan1_ordinal = jan1.toordinal()
    jan1_weekday = jan1.weekday()
    week1_start_ordinal = jan1_ordinal - jan1_weekday - adjustment
    if jan1_weekday > mid_weekday:
        week1_start_ordinal += 7
    return week1_start_ordinal


def _year_total_weeks(year, method):
    # type: (int, str) -> int
    """Return number of weeks in year for given year using given calculation
    method.
    """
    year_start_ordinal = _year_start(year, method)
    next_year_start_ordinal = _year_start(year + 1, method)
    weeks = (next_year_start_ordinal - year_start_ordinal) // 7
    return weeks
