import dash
import uuid
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table as tbl
import dash_daq as daq
from typing import Type

from negmas import NamedObject
from negmas.visualizers import *
from negmas.gui.runnable_viewer.layout import render

from negmas.gui.config import (Layout, 
                            _left_up_button_group, 
                            _new_checkpoint, 
                            _back_to_parent
                        )

def layout(object_type: Type[NamedObject]):
    """Returns a layout appropriate for the given named object"""

    v = visualizer_type(object_type)
    layout_id = uuid.uuid4()

    #widgets composed of  basic_info, childrens, graph_widgets
    widgets = [v.render_widget(widget, v.widget_params(widget)) for widget in v.widget_names()]

    # save all html here 
    children_layouts = [render(widget) for widget in widgets]

    # sorted the children_layouts as basic_info, childrens, graph_widgets
    children_layouts_dict = {"graph_widgets":[]}

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
                            # [System] just appear in not runnable page
                            _back_to_parent,
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
                        ] + children_layouts_dict['graph_widgets']
                    )
                ]
            )
        ],
    )

    return layout
