import os
import platform
from sayvai_tools.utils.system.properties.properties import getallproperties

def test_example():
    mysystem = platform.uname()
    properties = getallproperties()
    assert properties["SYSTEM"] == mysystem.system
    assert  properties["USERNAME"] == os.getlogin()