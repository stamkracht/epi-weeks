from datetime import date, timedelta, datetime
from typing import Tuple, Iterator


class Week:
    """A Week object represents a week in epidemiological week calendar."""

    __slots__ = "_year", "_week", "_system"

    def __init__(
        self, year: int, week: int, system: str = "cdc", validate: bool = True
    ) -> None:
        """
        :param year: Epidemiological year
        :type year: int
        :param week: Epidemiological week
        :type week: int
        :param system: Week numbering system, which may be ``cdc`` where the
            week starts on Sunday or ``iso`` where the week starts on Monday
            (default is ``cdc``)
        :type system: str
        :param validate: Whether to validate year, week and system or not
            (default is ``True``)
        :type validate: bool
        """

        if validate:
            _check_year(year)
            _check_system(system)
            _check_week(year, week, system)

        self._year = year
        self._week = week
        self._system = system.upper()

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}({self._year}, {self._week}, {self._system})"

    def __str__(self) -> str:
        return {"CDC": self.cdcformat, "ISO": self.isoformat, "WND": self.wndformat}[
            self._system
        ]()

    def __hash__(self) -> int:
        return hash((self._year, self._week, self._system))

    def __eq__(self, other: "Week") -> bool:
        return self._compare(other) == 0

    def __gt__(self, other: "Week") -> bool:
        return self._compare(other) > 0

    def __ge__(self, other: "Week") -> bool:
        return self._compare(other) >= 0

    def __lt__(self, other: "Week") -> bool:
        return self._compare(other) < 0

    def __le__(self, other: "Week") -> bool:
        return self._compare(other) <= 0

    def _compare(self, other: "Week") -> int:
        """Compare two Week objects after checking if they are comparable."""
        class_name = self.__class__.__name__
        other_name = type(other).__name__
        if not isinstance(other, self.__class__):
            raise TypeError(f"can't compare '{class_name}' to '{other_name}'")
        if self._system != other._system:
            raise TypeError(
                f"can't compare '{class_name}' objects with different "
                f"numbering systems"
            )
        x = self.weektuple()
        y = other.weektuple()
        return 0 if x == y else 1 if x > y else -1

    def __add__(self, other: int) -> "Week":
        if not isinstance(other, int):
            raise TypeError("second operand must be 'int'")
        new_date = self.startdate() + timedelta(weeks=other)
        return self.__class__.fromdate(new_date, self._system)

    def __sub__(self, other: int) -> "Week":
        if not isinstance(other, int):
            raise TypeError("second operand must be 'int'")
        return self.__add__(-other)

    def __contains__(self, other: date) -> bool:
        if not isinstance(other, date):
            raise TypeError("tested operand must be 'datetime.date' object")
        return other in self.iterdates()

    @classmethod
    def fromdate(cls, date_object: date, system: str = "cdc") -> "Week":
        """Construct Week object from a date.

        :param date_object: Gregorian date object
        :type date_object: datetime.date
        :param system: Week numbering system, which may be ``cdc`` where the
            week starts on Sunday or ``iso`` where the week starts on Monday
            (default is ``cdc``)
        :type system: str
        """
        if isinstance(date_object, datetime):
            date_object = date_object.date()
        if date_object >= date(2019, 11, 14):
            system = "wnd"
        _check_system(system)
        year = date_object.year
        date_ordinal = date_object.toordinal()
        year_start_ordinal = _year_start(year, system)
        week = (date_ordinal - year_start_ordinal) // 7
        if week < 0:
            year -= 1
            year_start_ordinal = _year_start(year, system)
            week = (date_ordinal - year_start_ordinal) // 7
        elif week >= 52:
            year_start_ordinal = _year_start(year + 1, system)
            if date_ordinal >= year_start_ordinal:
                year += 1
                week = 0
        week += 1
        return cls(year, week, system, validate=False)

    @classmethod
    def fromstring(
        cls, week_string: str, system: str = "cdc", validate: bool = True
    ) -> "Week":
        """Construct Week object from a formatted string.

        :param week_string: Week string formatted as ‘YYYYww’, ‘YYYYWww’,
            or ‘YYYY-Www’ for example ‘201908’, ‘2019W08’, or ‘2019-W08’.
            If the string ends with weekday as in ISO formats, weekday will
            be ignored.
        :type week_string: str
        :param system: Week numbering system, which may be ``cdc`` where the
            week starts on Sunday or ``iso`` where the week starts on Monday
            (default is ``cdc``)
        :type system: str
        :param validate: Whether to validate year, week and system or not
            (default is ``True``)
        :type validate: bool
        """

        week_string = week_string.replace("-", "").replace("W", "")
        year = int(week_string[:4])
        week = int(week_string[4:6])
        return cls(year, week, system, validate)

    @classmethod
    def thisweek(cls, system: str = "cdc") -> "Week":
        """Construct Week object from current date.

        :param system: Week numbering system, which may be ``cdc`` where the
            week starts on Sunday or ``iso`` where the week starts on Monday
            (default is ``cdc``)
        :type system: str
        """

        return cls.fromdate(date.today(), system)

    @property
    def year(self) -> int:
        """Return year as an integer"""
        return self._year

    @property
    def week(self) -> int:
        """Return week number as an integer"""
        return self._week

    @property
    def system(self) -> str:
        """Return week numbering system as a string"""
        return self._system

    def weektuple(self) -> Tuple[int, int]:
        """Return week as a tuple of (year, week)."""
        return self._year, self._week

    def cdcformat(self) -> str:
        """Return a string representing the week in CDC format ‘YYYYww’ for
        example ‘201908’.
        """

        return f"{self._year:04}{self._week:02}"

    def isoformat(self) -> str:
        """Return a string representing the week in ISO compact format
        ‘YYYYWww’ for example ‘2019W08’.
        """

        return f"{self._year:04}W{self._week:02}"

    def wndformat(self) -> str:
        """Return a string representing the week in WND format ‘YYYYww’ for
        example ‘201908’.
        """

        return f"{self._year:04}{self._week:02}"

    def startdate(self) -> date:
        """Return date for first day of week."""
        year_start_ordinal = _year_start(self._year, self._system)
        week_start_ordinal = year_start_ordinal + ((self._week - 1) * 7)
        startdate = date.fromordinal(week_start_ordinal)
        return startdate

    def enddate(self) -> date:
        """Return date for last day of week."""
        enddate = self.startdate() + timedelta(days=6)
        return enddate

    def iterdates(self) -> Iterator[date]:
        """Return an iterator that yield date objects for all days of week."""
        startdate = self.startdate()
        for day in range(0, 7):
            yield startdate + timedelta(days=day)

    def daydate(self, weekday: int = 6) -> date:
        """Return date for specific weekday of week.

        :param weekday: Week day, which may be ``0..6`` where Monday is 0 and
            Sunday is 6 (default is ``6``)
        :type weekday: int
        """

        diff = (_system_adjustment(self._system) + weekday) % 7
        return self.startdate() + timedelta(days=diff)

    def monday(self):
        return self.daydate(0)

    def tuesday(self):
        return self.daydate(1)

    def wednesday(self):
        return self.daydate(2)

    def thursday(self):
        return self.daydate(3)

    def friday(self):
        return self.daydate(4)

    def saturday(self):
        return self.daydate(5)

    def sunday(self):
        return self.daydate(6)


class Year:
    """A Year object represents a year in epidemiological week calendar."""

    __slots__ = "_year", "_system"

    def __init__(self, year: int, system: str = "cdc") -> None:
        """
        :param year: Epidemiological year
        :type year: int
        :param system: Week numbering system, which may be ``cdc`` where the
            week starts on Sunday or ``iso`` where the week starts on Monday
            (default is ``cdc``)
        :type system: str
        """

        _check_year(year)
        _check_system(system)
        self._year = year
        self._system = system.upper()

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}({self._year}, {self._system})"

    def __str__(self) -> str:
        return f"{self._year:04}"

    def __hash__(self) -> int:
        return hash((self._year, self._system))

    @classmethod
    def thisyear(cls, system: str = "cdc") -> "Year":
        """Construct Year object from current date.

        :param system: Week numbering system, which may be ``cdc`` where the
            week starts on Sunday or ``iso`` where the week starts on Monday
            (default is ``cdc``)
        :type system: str
        """

        return cls(date.today().year, system)

    @property
    def year(self) -> int:
        """Return year as an integer"""
        return self._year

    @property
    def system(self) -> str:
        """Return week numbering system as a string"""
        return self._system

    def totalweeks(self) -> int:
        """Return number of weeks in year."""
        return _year_total_weeks(self._year, self._system)

    def startdate(self) -> date:
        """Return date for first day of first week of year."""
        year_start_ordinal = _year_start(self._year, self._system)
        return date.fromordinal(year_start_ordinal)

    def enddate(self) -> date:
        """Return date for last day of last week of year."""
        year_end_ordinal = _year_start(self._year + 1, self._system) - 1
        return date.fromordinal(year_end_ordinal)

    def iterweeks(self) -> Iterator[Week]:
        """Return an iterator that yield Week objects for all weeks of year."""
        for week in range(1, self.totalweeks() + 1):
            yield Week(self._year, week, self._system, validate=False)


def _check_year(year: int) -> None:
    """Check value of year."""
    if not 1 <= year <= 9999:
        raise ValueError("year must be in 1..9999")


def _check_week(year: int, week: int, system: str) -> None:
    """Check value of week."""
    weeks = _year_total_weeks(year, system)
    if not 1 <= week <= weeks:
        raise ValueError(f"week must be in 1..{weeks} for year")


def _check_system(system: str) -> None:
    """Check value of week numbering system."""
    systems = ("cdc", "iso", "wnd")
    if system.lower() not in systems:
        raise ValueError(f"system must be '{systems[0]}' or '{systems[1]}'")


def _system_adjustment(system: str) -> int:
    """Return needed adjustment based on week numbering system."""
    return {"iso": 0, "cdc": 1, "wnd": 4}.get(system.lower())


def _year_start(year: int, system: str) -> int:
    """Return ordinal for first day of first week for year."""
    adjustment = _system_adjustment(system)
    mid_weekday = 3 - adjustment  # Sun is 6 .. Mon is 0
    jan1 = date(year, 1, 1)
    jan1_ordinal = jan1.toordinal()
    jan1_weekday = jan1.weekday()
    week1_start_ordinal = jan1_ordinal - jan1_weekday - adjustment
    if jan1_weekday > mid_weekday:
        week1_start_ordinal += 7
    return week1_start_ordinal


def _year_total_weeks(year: int, system: str) -> int:
    """Return number of weeks in year."""
    year_start_ordinal = _year_start(year, system)
    next_year_start_ordinal = _year_start(year + 1, system)
    weeks = (next_year_start_ordinal - year_start_ordinal) // 7
    return weeks
