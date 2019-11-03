import pytest
import epiweeks
from datetime import date, timedelta, datetime


@pytest.fixture(scope="module")
def week_cdc():
    return epiweeks.Week(2015, 1, system="cdc")


@pytest.fixture(scope="module")
def week_iso():
    return epiweeks.Week(2015, 1, system="iso")


@pytest.fixture(scope="module")
def week_wnd():
    return epiweeks.Week(2019, 47, system="wnd")


def test_week_representation(week_cdc, week_iso, week_wnd):
    assert week_cdc.__repr__() == "Week(2015, 1, CDC)"
    assert week_iso.__repr__() == "Week(2015, 1, ISO)"
    assert week_wnd.__repr__() == "Week(2019, 47, WND)"


def test_week_string(week_cdc, week_iso, week_wnd):
    assert week_cdc.__str__() == "201501"
    assert week_iso.__str__() == "2015W01"
    assert week_wnd.__str__() == "201947"


def test_week_hash(week_cdc, week_iso, week_wnd):
    assert week_cdc.__hash__() == hash((2015, 1, "CDC"))
    assert week_iso.__hash__() == hash((2015, 1, "ISO"))
    assert week_wnd.__hash__() == hash((2019, 47, "WND"))


def test_week_equality(week_cdc, week_iso, week_wnd):
    assert week_cdc == epiweeks.Week(2015, 1, system="cdc")
    assert week_cdc != epiweeks.Week(2014, 1, system="cdc")
    assert week_iso == epiweeks.Week(2015, 1, system="iso")
    assert week_iso != epiweeks.Week(2014, 1, system="iso")
    assert week_wnd == epiweeks.Week(2019, 47, system="wnd")
    assert week_wnd != epiweeks.Week(2020, 47, system="wnd")


def test_week_ordering(week_cdc, week_iso, week_wnd):
    assert week_cdc > epiweeks.Week(2014, 53, system="cdc")
    assert week_cdc >= epiweeks.Week(2015, 1, system="cdc")
    assert week_cdc < epiweeks.Week(2015, 2, system="cdc")
    assert week_cdc <= epiweeks.Week(2015, 1, system="cdc")
    assert week_iso > epiweeks.Week(2014, 52, system="iso")
    assert week_iso >= epiweeks.Week(2015, 1, system="iso")
    assert week_iso < epiweeks.Week(2015, 2, system="iso")
    assert week_iso <= epiweeks.Week(2015, 1, system="iso")
    assert week_wnd > epiweeks.Week(2019, 46, system="wnd")
    assert week_wnd >= epiweeks.Week(2019, 47, system="wnd")
    assert week_wnd < epiweeks.Week(2019, 48, system="wnd")
    assert week_wnd <= epiweeks.Week(2019, 47, system="wnd")


def test_week_addition(week_cdc, week_iso, week_wnd):
    assert (week_cdc + 1) == epiweeks.Week(2015, 2, system="cdc")
    assert (week_iso + 1) == epiweeks.Week(2015, 2, system="iso")
    assert (week_wnd + 1) == epiweeks.Week(2019, 48, system="wnd")


def test_week_subtracting(week_cdc, week_iso, week_wnd):
    assert (week_cdc - 1) == epiweeks.Week(2014, 53, system="cdc")
    assert (week_iso - 1) == epiweeks.Week(2014, 52, system="iso")
    assert (week_wnd - 1) == epiweeks.Week(2019, 46, system="wnd")


def test_week_containment(week_cdc, week_iso, week_wnd):
    assert date(2015, 1, 5) in week_cdc
    assert date(2015, 1, 1) in week_iso
    assert date(2019, 11, 24) in week_wnd


def test_week_comparison(week_cdc, week_iso, week_wnd):
    assert epiweeks.Week(2019, 46, system="wnd") > epiweeks.Week(2019, 46, system="cdc")
    assert epiweeks.Week(2019, 46, system="cdc") < epiweeks.Week(2019, 46, system="wnd")
    assert epiweeks.Week(2019, 45, system="wnd") < epiweeks.Week(2019, 46, system="cdc")
    assert epiweeks.Week(2019, 45, system="cdc") < epiweeks.Week(2019, 46, system="wnd")
    assert epiweeks.Week(2019, 46, system="wnd") > epiweeks.Week(2019, 45, system="cdc")
    assert epiweeks.Week(2019, 46, system="cdc") > epiweeks.Week(2019, 45, system="wnd")


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("__add__", "second operand must be 'int'"),
        ("__sub__", "second operand must be 'int'"),
        ("__contains__", "tested operand must be 'datetime.date' object"),
    ],
)
def test_week_operator_exception(week_cdc, week_iso, week_wnd, test_input, expected):
    with pytest.raises(TypeError) as e:
        getattr(week_cdc, test_input)("w")
        getattr(week_iso, test_input)("w")
        getattr(week_wnd, test_input)("w")
    assert str(e.value) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ((date(2014, 12, 28), "cdc"), ((2014, 53), "cdc")),
        ((date(2014, 12, 28), "iso"), ((2014, 52), "iso")),
        ((date(2015, 1, 2), "cdc"), ((2014, 53), "cdc")),
        ((date(2015, 1, 2), "iso"), ((2015, 1), "iso")),
        ((date(2016, 2, 14), "cdc"), ((2016, 7), "cdc")),
        ((date(2016, 2, 14), "iso"), ((2016, 6), "iso")),
        ((date(2017, 12, 31), "cdc"), ((2018, 1), "cdc")),
        ((date(2017, 12, 31), "iso"), ((2017, 52), "iso")),
        ((date(2019, 11, 13),), ((2019, 46), "cdc")),
        ((date(2019, 11, 14),), ((2019, 46), "wnd")),
        ((date(2019, 11, 20),), ((2019, 46), "wnd")),
        ((date(2019, 11, 21),), ((2019, 47), "wnd")),
        ((datetime(2019, 11, 21, 1, 2, 3),), ((2019, 47), "wnd")),
    ],
)
def test_week_fromdate(test_input, expected):
    week = epiweeks.Week.fromdate(*test_input)
    assert (week.weektuple(), week.system.lower()) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (("201453", "cdc"), (2014, 53)),
        (("201607", "cdc"), (2016, 7)),
        (("2014W52", "iso"), (2014, 52)),
        (("2015W01", "iso"), (2015, 1)),
        (("2016-W06", "iso"), (2016, 6)),
        (("2018-W01-2", "iso"), (2018, 1)),
        (("2017W527", "iso"), (2017, 52)),
        (("201948", "wnd"), (2019, 48)),
    ],
)
def test_week_fromstring(test_input, expected):
    week = epiweeks.Week.fromstring(*test_input)
    assert week.weektuple() == expected


def test_week_thisweek():
    cdc_week = epiweeks.Week.thisweek(system="cdc")
    cdc_diff = (date.today().weekday() + 1) % 7
    cdc_startdate = date.today() - timedelta(days=cdc_diff)
    assert cdc_week.startdate() == cdc_startdate
    iso_week = epiweeks.Week.thisweek(system="iso")
    iso_diff = date.today().isoweekday() - 1
    iso_startdate = date.today() - timedelta(days=iso_diff)
    assert iso_week.startdate() == iso_startdate


def test_week_year(week_cdc, week_iso, week_wnd):
    assert week_cdc.year == 2015
    assert week_iso.year == 2015
    assert week_wnd.year == 2019


def test_week_number(week_cdc, week_iso, week_wnd):
    assert week_cdc.week == 1
    assert week_iso.week == 1
    assert week_wnd.week == 47


def test_week_system(week_cdc, week_iso, week_wnd):
    assert week_cdc.system == "CDC"
    assert week_iso.system == "ISO"
    assert week_wnd.system == "WND"


def test_weektuple(week_cdc, week_iso, week_wnd):
    assert week_cdc.weektuple() == (2015, 1)
    assert week_iso.weektuple() == (2015, 1)
    assert week_wnd.weektuple() == (2019, 47)


def test_week_cdcformat(week_cdc):
    assert week_cdc.cdcformat() == "201501"


def test_week_isoformat(week_iso):
    assert week_iso.isoformat() == "2015W01"


def test_week_wndformat(week_wnd):
    assert week_wnd.wndformat() == "201947"


def test_week_startdate(week_cdc, week_iso, week_wnd):
    assert week_cdc.startdate() == date(2015, 1, 4)
    assert week_iso.startdate() == date(2014, 12, 29)
    assert week_wnd.startdate() == date(2019, 11, 21)


def test_week_enddate(week_cdc, week_iso, week_wnd):
    assert week_cdc.enddate() == date(2015, 1, 10)
    assert week_iso.enddate() == date(2015, 1, 4)
    assert week_wnd.enddate() == date(2019, 11, 27)


def test_week_dates(week_cdc, week_iso, week_wnd):
    cdc_week_dates = [
        date(2015, 1, 4),
        date(2015, 1, 5),
        date(2015, 1, 6),
        date(2015, 1, 7),
        date(2015, 1, 8),
        date(2015, 1, 9),
        date(2015, 1, 10),
    ]
    iso_week_dates = [
        date(2014, 12, 29),
        date(2014, 12, 30),
        date(2014, 12, 31),
        date(2015, 1, 1),
        date(2015, 1, 2),
        date(2015, 1, 3),
        date(2015, 1, 4),
    ]
    wnd_week_dates = [
        date(2019, 11, 21),
        date(2019, 11, 22),
        date(2019, 11, 23),
        date(2019, 11, 24),
        date(2019, 11, 25),
        date(2019, 11, 26),
        date(2019, 11, 27),
    ]
    assert list(week_cdc.iterdates()) == cdc_week_dates
    assert list(week_iso.iterdates()) == iso_week_dates
    assert list(week_wnd.iterdates()) == wnd_week_dates


def test_week_daydate(week_cdc, week_iso, week_wnd):
    cdc_week_dates = [
        date(2015, 1, 5),
        date(2015, 1, 6),
        date(2015, 1, 7),
        date(2015, 1, 8),
        date(2015, 1, 9),
        date(2015, 1, 10),
        date(2015, 1, 4),
    ]
    iso_week_dates = [
        date(2014, 12, 29),
        date(2014, 12, 30),
        date(2014, 12, 31),
        date(2015, 1, 1),
        date(2015, 1, 2),
        date(2015, 1, 3),
        date(2015, 1, 4),
    ]
    wnd_week_dates = [
        date(2019, 11, 25),
        date(2019, 11, 26),
        date(2019, 11, 27),
        date(2019, 11, 21),
        date(2019, 11, 22),
        date(2019, 11, 23),
        date(2019, 11, 24),
    ]
    for i, daydate in enumerate(cdc_week_dates):
        assert week_cdc.daydate(i) == daydate
    for i, daydate in enumerate(iso_week_dates):
        assert week_iso.daydate(i) == daydate
    for i, daydate in enumerate(wnd_week_dates):
        assert week_wnd.daydate(i) == daydate


@pytest.fixture(scope="module")
def year_cdc():
    return epiweeks.Year(2015, system="cdc")


@pytest.fixture(scope="module")
def year_iso():
    return epiweeks.Year(2015, system="iso")


@pytest.fixture(scope="module")
def year_wnd():
    return epiweeks.Year(2020, system="wnd")


def test_year_repr(year_cdc, year_iso, year_wnd):
    assert year_cdc.__repr__() == "Year(2015, CDC)"
    assert year_iso.__repr__() == "Year(2015, ISO)"
    assert year_wnd.__repr__() == "Year(2020, WND)"


def test_year_string(year_cdc):
    assert year_cdc.__str__() == "2015"


def test_year_hash(year_cdc, year_iso, year_wnd):
    assert year_cdc.__hash__() == hash((2015, "CDC"))
    assert year_iso.__hash__() == hash((2015, "ISO"))
    assert year_wnd.__hash__() == hash((2020, "WND"))


def test_year_thisyear():
    today_year = date.today().year
    cdc_year = epiweeks.Year.thisyear(system="cdc")
    cdc_year_start = epiweeks._year_start(today_year, system="cdc")
    iso_year = epiweeks.Year.thisyear(system="iso")
    iso_year_start = epiweeks._year_start(today_year, system="iso")
    assert cdc_year.startdate().toordinal() == cdc_year_start
    assert iso_year.startdate().toordinal() == iso_year_start


def test_year_number(year_cdc, year_iso, year_wnd):
    assert year_cdc.year == 2015
    assert year_iso.year == 2015
    assert year_wnd.year == 2020


def test_year_system(year_cdc, year_iso, year_wnd):
    assert year_cdc.system == "CDC"
    assert year_iso.system == "ISO"
    assert year_wnd.system == "WND"


def test_year_totalweeks(year_cdc, year_iso, year_wnd):
    assert year_cdc.totalweeks() == 52
    assert year_iso.totalweeks() == 53
    assert year_wnd.totalweeks() == 52


def test_year_startdate(year_cdc, year_iso, year_wnd):
    assert year_cdc.startdate() == date(2015, 1, 4)
    assert year_iso.startdate() == date(2014, 12, 29)
    assert year_wnd.startdate() == date(2020, 1, 2)


def test_year_enddate(year_cdc, year_iso, year_wnd):
    assert year_cdc.enddate() == date(2016, 1, 2)
    assert year_iso.enddate() == date(2016, 1, 3)
    assert year_wnd.enddate() == date(2020, 12, 30)


def test_year_weeks(year_cdc, year_iso, year_wnd):
    cdc_weeks = []
    for w in range(1, 53):
        cdc_weeks.append(epiweeks.Week(2015, w))
    assert list(year_cdc.iterweeks()) == cdc_weeks
    iso_weeks = []
    for w in range(1, 54):
        iso_weeks.append(epiweeks.Week(2015, w, system="iso"))
    assert list(year_iso.iterweeks()) == iso_weeks
    wnd_weeks = []
    for w in range(1, 53):
        wnd_weeks.append(epiweeks.Week(2020, w, system="wnd"))
    assert list(year_wnd.iterweeks()) == wnd_weeks


def test_check_valid_week():
    try:
        epiweeks._check_week(2015, 53, system="iso")
    except ValueError:
        pytest.fail("week should be valid")


def test_check_invalid_week():
    with pytest.raises(ValueError) as e:
        epiweeks._check_week(2015, 0, system="cdc")
        epiweeks._check_week(2015, 53, system="cdc")
    assert str(e.value) == "week must be in 1..52 for year"


def test_check_valid_year():
    try:
        epiweeks._check_year(2018)
    except ValueError:
        pytest.fail("year should be valid")


def test_check_invalid_year():
    with pytest.raises(ValueError) as e:
        epiweeks._check_year(0)
        epiweeks._check_year(20155)
    assert str(e.value) == "year must be in 1..9999"


def test_check_valid_system():
    try:
        epiweeks._check_system("CDC")
        epiweeks._check_system("cdc")
        epiweeks._check_system("ISO")
        epiweeks._check_system("iso")
        epiweeks._check_system("WND")
        epiweeks._check_system("wnd")
    except ValueError:
        pytest.fail("method should be valid")


def test_check_invalid_system():
    with pytest.raises(ValueError) as e:
        epiweeks._check_system("mmwr")
    assert str(e.value) == "system must be 'cdc' or 'iso'"


@pytest.mark.parametrize("test_input, expected", [("cdc", 1), ("iso", 0), ("wnd", 4)])
def test_system_adjustment(test_input, expected):
    assert epiweeks._system_adjustment(test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [((2015, "cdc"), 735602), ((2015, "iso"), 735596), ((2020, "wnd"), 737426)],
)
def test_year_start_ordinal(test_input, expected):
    assert epiweeks._year_start(*test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [((2015, "cdc"), 52), ((2015, "iso"), 53), ((2019, "iso"), 52)],
)
def test_year_total_weeks(test_input, expected):
    assert epiweeks._year_total_weeks(*test_input) == expected
