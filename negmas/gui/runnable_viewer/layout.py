# from negmas.gui.named_viewer import named_viewer_objects
from negmas import NamedObject
from negmas.helpers import get_full_type_name
from negmas.gui.settings import LAYOUTS
from typing import Type

def layout(object_type: Type[NamedObject]):
    """
    Predefine the layout structure
    do not contain the data
    live update when call run_callback function,
    means different object type can define different self layout,
    """

    # get class type defined as obejct_type, return a visualizer calss, not instance
    # so can not access self.object in visualizer
    type_name: str = get_full_type_name(object_type)
    
    if type_name in LAYOUTS:
        return LAYOUTS[type_name]
    
    return LAYOUTS['default_runnable_layout']