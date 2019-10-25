
from negmas import NamedObject
from negmas.visualizers import *
from negmas.gui.named_viewer import named_viewer_objects
from negmas.gui.named_viewer.layout import layout as named_viewer_layout

def layout(object_type: Type[NamedObject]):
    v = visualizer_type(object_type)
    widgets = v.widget_names()
    c = []

    for widget in widgets:
        rendered_widget = v.render_widget(widget, v.widget_params(widget))
        c.append(rendered_widget) 

    return c