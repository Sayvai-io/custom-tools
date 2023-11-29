# pytest for testing imports

import pytest

def test_imports():
    from sayvai_tools import (
        __version__,
        __author__,
        __author_email__,
    )
    assert __version__ == "0.0.1"
    
