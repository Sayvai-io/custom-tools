# pytest for testing imports

import pytest


def test_imports():
    from sayvai_tools import __author__, __author_email__, __version__

    assert __version__ == "0.0.3"
