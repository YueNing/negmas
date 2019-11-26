import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from negmas.gui.settings import LAYOUT_PARAMS
from negmas.gui import (
                    _left_up_button_group, 
                    _right_up_group_runnable_component, 
                    _new_checkpoint, 
                    _back_to_parent, 
                    _interval_one_second
                )

# DEFAULT_LAYOUT   described as following
# | button group   | control_bar |
# | basic_info     | graphs row1 |
# | new_checkpoint | graphs row2 |

DEFAULT_LAYOUT =  html.Div(
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
                            html.Div(id="basic_info"),
                            html.Br(),
                            html.Div(id="childrens"),
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
                            dbc.Row([
                                dcc.Graph(id='graph1'),
                                dcc.Graph(id='graph2'),
                            ]),
                            html.Br(),
                            dbc.Row([
                                dcc.Graph(id='graph3'),
                                dcc.Graph(id='graph4'),
                            ]),
                        ]
                    )
                ]
            ),
            _interval_one_second
        ],
    )
