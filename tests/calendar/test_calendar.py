import os
from typing import Any, Dict, List, Optional, Text, Tuple

import dotenv
import pytest

from sayvai_tools.tools.calendar.calendar import Calendar


def test_positive(correct_parameters: Dict[str, Any]):
    scope = correct_parameters["scope"]
    email = correct_parameters["email"]
    summary = correct_parameters["summary"]
    date = correct_parameters["date"]
    cal = Calendar(scope=scope, email=email, summary=summary)
    assert cal._run(date)


def test_incorrect(incorrect_parameters: Dict[str, Any]):
    scope = incorrect_parameters["scope"]
    email = incorrect_parameters["email"]
    summary = incorrect_parameters["summary"]
    date = incorrect_parameters["date"]
    cal = Calendar(scope=scope, email=email, summary=summary)
    with pytest.raises(Exception):
        cal._run(date)


def test_past_date(past_date: Dict[str, Any]):
    scope = past_date["scope"]
    email = past_date["email"]
    summary = past_date["summary"]
    date = past_date["date"]
    cal = Calendar(scope=scope, email=email, summary=summary)
    assert cal._run(date) == "The provided date and time are in the past."


def test_time(past_time: Dict[str, Any]):
    scope = past_time["scope"]
    email = past_time["email"]
    summary = past_time["summary"]
    date = past_time["date"]
    cal = Calendar(scope=scope, email=email, summary=summary)
    assert cal._run(date) == "End time should be greater than start time."
