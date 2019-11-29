from typing import Type
from negmas import NamedObject
from negmas.gui.settings import LAYOUTS
from negmas.helpers import get_full_type_name

def layout(object_type: Type[NamedObject]):
    type_name: str = get_full_type_name(object_type)
    
    if type_name in LAYOUTS:
        return LAYOUTS[type_name]
    
    return LAYOUTS['default_named_layout']