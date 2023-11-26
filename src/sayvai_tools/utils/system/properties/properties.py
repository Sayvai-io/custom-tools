"""python file for system utils/properties"""
# with this one from src/sayvai_tools/utils/system/properties/__init__.py:
import os
import sys
import platform
from pydantic import BaseModel
my_system = platform.uname()

class SystemProperties(BaseModel):
    """properties class"""
    SYSTEM : str = my_system.system
    NODE : str = my_system.node
    RELEASE_DATE : str = my_system.release
    MACHINE : str = my_system.machine
    PROCESSOR : str = my_system.processor
    USERNAME : str = os.getlogin()
class Config:
    """config class"""
    def __init__(self):
        """init method"""
        self.system_properties = SystemProperties()

    def get_system_properties(self):
        """get system properties"""
        return self.system_properties

    def get_system(self):
        """get system"""
        return self.system_properties.SYSTEM

    def get_node(self):
        """get node"""
        return self.system_properties.NODE

    def get_release_date(self):
        """get release date"""
        return self.system_properties.RELEASE_DATE

    def get_machine(self):
        """get machine"""
        return self.system_properties.MACHINE

    def get_processor(self):
        """get processor"""
        return self.system_properties.PROCESSOR

    def get_os(self):
        """get os"""
        return os.name

    def get_python_version(self):
        """get python version"""
        return sys.version

    def get_python_version_info(self):
        """get python version info"""
        return sys.version_info


def getallproperties():
    config: dict = {}
    try:
        for value in SystemProperties():
            config[value[0]] = value[1]
    except Exception as e:
        print(e)
        config["error"] = e
    return config
