import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from negmas.gui.settings import *
from negmas.gui.layouts.widget_layout import (
    _left_up_button_group,
    _new_checkpoint,
    _right_up_group_runnable_component,
    _interval_one_second,
    navbar,
    main_entry_body
)

# Used for entry page, home page '/'
MAIN_LAYOUT = html.Div([navbar, main_entry_body], style={"width": "100%"})

# DEFAULT_LAYOUT   described as following
# | button group   | control_bar |
# | basic_info     | graphs row1 |
# | new_checkpoint | graphs row2 |
# Used For Runnable object pages

DEFAULT_LAYOUT_RUNNABLE =  html.Div(
        id='DEFAULT_LAYOUT',
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Br(),
                            # [System] control bar, predefined
                            _left_up_button_group,
                            html.Br(),
                            html.Div(id="negmas-basic_info"),
                            html.Br(),
                            html.Div(id="negmas-children"),
                            html.Br(),
                            # [System] save, predefined 
                            _new_checkpoint
                        ],
                        width={"size":LAYOUT_PARAMS["left"]["size"], "offset": 1}
                    ),
                    dbc.Col(
                        [
                            html.Br(),
                            _right_up_group_runnable_component,
                            html.Br(),
                            html.Div(id="graphs")
                        ]
                    )
                ]
            ),
            _interval_one_second
        ],
    )


DEFAULT_LAYOUT_NAMED = html.Div()


def set_dynamically_layout(object_set):
    # now just need to add graphs into this layout
    # later can search by id
    # import pdb;pdb.set_trace()
    # object_set.layout.children[0].children[1].children[3] = html.Div[

    # ]
    # import pdb;pdb.set_trace()
    if hasattr(object_set, 'components'):
        if object_set.layout.children[0].children[1].children[3].id == "graphs":
            # object_set.graph_components
            # every row 2 graph
            step = 2
            graph_children = [dbc.Row([dbc.Col([dcc.Graph(id=g[0], figure=object_set.init_result[2])]) 
                                for g in object_set.graph_components[i:i+step]]) 
                                    for i in range(0,len(object_set.graph_components),step)
                            ]
            # import pdb;pdb.set_trace()
            object_set.layout.children[0].children[1].children[3] = html.Div(graph_children, id="graphs")
        else:
            print("please confirm the graphs position in function set_dynamically_layout!")
        
        if object_set.layout.children[0].children[0].children[3].id == 'negmas-basic_info':
            object_set.layout.children[0].children[0].children[3] = html.Div(object_set.init_result[0], id="negmas-basic_info")
        
        if object_set.layout.children[0].children[0].children[5].id == 'negmas-children':
            object_set.layout.children[0].children[0].children[5] = html.Div(object_set.init_result[1], id="negmas-children")
        # if object_set.layout.children[]
        # import pdb;pdb.set_trace()
    else:
        print(f"please set attr 'components' into {object_set}")