import pytest


@pytest.fixture
def correct_parameters():
    return {
        "scope": "https://www.googleapis.com/auth/calendar",
        "email": "info@sayvai.io",
        "summary": "sample test calendar",
        "date": "2023, 10, 4, 16, 00/2023, 10, 4, 16, 59/9629076714/SriDhanush",
    }


@pytest.fixture
def incorrect_parameters():
    return {
        "scope": "https://www.googleapis.com/auth/calendar",
        "email": "info@sayvai.io",
        "summary": "sample test calendar",
        "date": "2023, 10, 4, 16, 00/2023, 10, 4, 16, 59/SriDhanush",
    }


@pytest.fixture
def past_date():
    return {
        "scope": "https://www.googleapis.com/auth/calendar",
        "email": "info@sayvai.io",
        "summary": "sample test calendar",
        "date": "2023, 10, 4, 16, 00/2023, 10, 4, 16, 59/9629076714/SriDhanush",
    }


@pytest.fixture
def past_time():
    return {
        "scope": "https://www.googleapis.com/auth/calendar",
        "email": "info@sayvai.io",
        "summary": "sample test calendar",
        "date": "2023, 12, 4, 16, 00/2023, 12, 4, 13, 59/9629076714/SriDhanush",
    }

