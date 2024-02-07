"""init file for properties utils"""

from sayvai_tools.utils.system.properties.properties import (
    SystemProperties,
    get_all_properties,
)

__properties__ = get_all_properties()
__all__ = ["SystemProperties", "get_all_properties"]
