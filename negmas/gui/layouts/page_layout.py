import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from negmas.gui.settings import LAYOUT_PARAMS
from negmas.gui.layouts.widget_layout import (
    _left_up_button_group,
    _new_checkpoint,
    _right_up_group_runnable_component,
    _interval_one_second,
    navbar,
    main_entry_body
)

# DEFAULT_LAYOUT   described as following
# | button group   | control_bar |
# | basic_info     | graphs row1 |
# | new_checkpoint | graphs row2 |
# Used For Runnable object pages

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

# Used for entry page, home page '/'
MAIN_LAYOUT = html.Div([navbar, main_entry_body], style={"width": "100%"})
