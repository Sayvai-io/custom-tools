# pytest for testing imports

import datetime

import pytest


def test_get_date():
    from sayvai_tools.tools import GetDate
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%A, %B %d, %Y %I:%M %p")
    assert GetDate()._run()[17] == str(current_time)[17]  # chunk
