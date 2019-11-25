
from negmas import NamedObject
from negmas.visualizers import *
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from negmas.gui.named_viewer import named_viewer_objects
from negmas.gui.named_viewer.layout import layout as named_viewer_layout
from negmas.gui.config import (Layout, 
                    _left_up_button_group, 
                    _right_up_group_runnable_component, 
                    _new_checkpoint, 
                    _back_to_parent, 
                    _interval_one_second
                )
from negmas.gui.utils import render
from negmas.visualizer import Widget 

def layout(object_type: Type[NamedObject]):
    """
    Predefine the layout structure
    do not contain the data
    live update when call run_callback function
    """

    # get class type defined as obejct_type, return a visualizer calss, not instance
    # so can not access self.object in visualizer
    v = visualizer_type(object_type)

    # all widgets name
    widget_names = v.widget_names()

    # children_categories
    children_categories = v.children_categories()
    
    # layout id 
    layout_id = uuid.uuid4()
    
    # all widget html code saved in dict layouts_dict
    # can access all predefined layout from layouts_dict
    # such as here, all graph_widgets, basic_info and childrens info(negotiators)
    layouts_dict = {"graph_widgets":[]}

    # base on widget_names and children_categories to set the predefined layout, 
    # widget id format 'self.object.id_widget_name'
    # self.object.id is the id of object_type, 
    # later saved in the member self.object of Visualizer
    for widget_name in widget_names:
        widget_id = f'{object_type.id}_{widget_name}'
        kind, html_code = render(Widget(kind=v.widget_kind))
        

    # save all html here 
    children_layouts = [render(widget) for widget in widgets]

    # sorted the children_layouts as basic_info, childrens, graph_widgets

    for children_layout in children_layouts:
        if children_layout[0] == "graph_data":
            children_layout["graph_widgets"].append(children_layout)
        else:
            children_layouts_dict[children_layout[0]] = children_layout[1]

    layout = html.Div(
        id=layout_id,
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Br(),
                            # [System] control bar, predefined
                            _left_up_button_group,
                            html.Br(),
                            children_layouts_dict["basic_info"],
                            html.Br(),
                            children_layouts_dict["childrens"],
                            html.Br(),
                            # [System] save, predefined 
                            _new_checkpoint
                        ],
                        width={"size":Layout["left"]["size"], "offset": 1}
                    ),
                    dbc.Col(
                        [
                            html.Br(),
                            _right_up_group_runnable_component,
                        ] + children_layouts_dict['graph_widgets']
                    )
                ]
            ),
            _interval_one_second
        ],
    )

    return layout