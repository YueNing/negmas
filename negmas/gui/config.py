"""
Basic config file, 
Layout: layout ratio and info 
"""

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


# all config for Layout, contained settings and basic layout info
Layout = {
    "left":{"size": 4, "offset": 1},
    "right":{"size": 8, "layout":{"left":{"scale": 6}, "right":{"scale":6}}}
}

# left up button group compose of four buttons,  Run New, Run From Checkpoint, Tournament, Setting
_left_up_button_group = dbc.Row(
    [
        dcc.Link(dbc.Button("Run New", id="run_new", outline=True, color="secondary", className="mr-1"), href="/run_new"),
        dcc.Link(dbc.Button("Run From Checkpoint", outline=True, color="secondary", className="mr-1"), href="/checkpoint"),
        dcc.Link(dbc.Button("Tournament", outline=True, color="secondary", className="mr-1"), href="/tournament"),
        dcc.Link(dbc.Button("Setting", outline=True, color="secondary", className="mr-1"), href="/setting"),
    ],
                    
)

_new_checkpoint = dbc.Row(
    [
        dcc.Link(dbc.Button("Save Checkpoint", id="save_checkpoint", outline=True, color="secondary", className="mr-1"), href="/save_newCheckpoint"),
    ]
)

_right_up_group_runnable_component = dbc.Row(                         
    [
        dbc.Col(
            [
                dbc.Progress(id="progress", value=0, striped=True, animated=True),
                dcc.Interval(id="interval", interval=250, n_intervals=0),
                html.I(id="step_backward", n_clicks=0, className='fa fa-step-backward fa-lg'),
                html.I(id="play", n_clicks=0, className='fa fa-play'),
                html.I(id="step_forward", n_clicks=0, className='fa fa-step-forward')
            ]
        ),
        dbc.Col(
            [
                dbc.Button('test'),
            ]
        ),
    ]
)

_back_to_parent = dbc.Row(
    dcc.Link(dbc.Button("back_to_parent", id="back_to_parent", outline=True, color="secondary", className="mr-1"), href="/backToParent"),
)

_interval_one_second = dcc.Interval(
    id="interval-component",
    interval=1*1000, # one second
    n_intervals=0
)



# for system setting such as runnable_object
runnables = [
    'negmas.apps.scml.SCMLWorld',
    'negmas.situated.World',
    'negmas.mechanisms.Mechanism',
]