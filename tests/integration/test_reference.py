from datetime import date
import pytest
import pathlib
import json
import epiweeks


def load_params_from_json(file):
    jsonfile = pathlib.Path(__file__).parent.joinpath("fixtures", file)
    content = jsonfile.read_text(encoding="utf-8")
    data = [[tuple(i) for i in x] for x in json.loads(content)]
    params = [tuple(x) for x in data]
    params_reversed = [tuple(x[::-1]) for x in data]
    return params, params_reversed


cdc_weeks = load_params_from_json("cdc_weeks.json")
iso_weeks = load_params_from_json("iso_weeks.json")


@pytest.mark.parametrize("test_input, expected", cdc_weeks[0])
def test_cdc_week_to_startdate(test_input, expected):
    year, week = test_input
    startdate = epiweeks.Week(year, week, "cdc").startdate()
    assert startdate.timetuple()[:3] == expected


@pytest.mark.parametrize("test_input, expected", cdc_weeks[1])
def test_cdc_week_from_startdate(test_input, expected):
    week = epiweeks.Week.fromdate(date(*test_input), "cdc").weektuple()
    assert week == expected


@pytest.mark.parametrize("test_input, expected", iso_weeks[0])
def test_iso_week_to_startdate(test_input, expected):
    year, week = test_input
    startdate = epiweeks.Week(year, week, "iso").startdate()
    assert startdate.timetuple()[:3] == expected


@pytest.mark.parametrize("test_input, expected", iso_weeks[1])
def test_iso_week_from_startdate(test_input, expected):
    week = epiweeks.Week.fromdate(date(*test_input), "iso").weektuple()
    assert week == expected
