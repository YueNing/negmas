"""
Define all widgets layout here
"""
import dash_daq as daq
from negmas.gui.settings import *

_interval_one_second = dcc.Interval(
    id="interval-component",
    interval=UPDATE_INTERVAL*1000, # one second
    n_intervals=0
)


# error indicator 
control_info_stop_start_error = dbc.Alert("Can not Stop/Start !", id="control-info-stop-start-error", dismissable=True, is_open=False)
control_info_previous_step_error = dbc.Alert("Can not goto previous step ! ", id="control-info-previous-step-error", dismissable=True, is_open=False)
control_info_next_step_error = dbc.Alert("Can not goto next step ! ", id="control-info-next-step-error", dismissable=True, is_open=False)

# base container
base = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        html.Div(
            [control_info_stop_start_error, control_info_previous_step_error, control_info_next_step_error]
        ),
        html.Div(
            id='page-content'
        ),
        html.Div(id='intermediate-value', style={'display': 'none'}),
    ]
)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Settings", href="/settings")),
        # dbc.DropdownMenu(
        #     nav=True,
        #     in_navbar=True,
        #     label="Menu",
        #     children=[
        #         dbc.DropdownMenuItem("Entry 1"),
        #         dbc.DropdownMenuItem("Entry 2"),
        #         dbc.DropdownMenuItem(divider=True),
        #         dbc.DropdownMenuItem("Entry 3"),
        #     ],
        # ),
    ],
    brand="NegMAS GUI",
    brand_href="#",
    sticky="top",
)

run_online = dbc.Card(
    dbc.CardBody(
        [
            html.P("Run a new component", className="card-text"),
            dbc.Select(
                options=[
                    {'label': 'SCMLWorld', 'value': 'negmas.apps.scml.SCMLWorld'},
                    {'label': 'World', 'value': 'negmas.situated.World'},
                    {'label': 'Mechanism', 'value': 'negmas.mechanisms.Mechanism'},
                    {'label': 'SAOMechanism', 'value': 'negmas.sao.SAOMechanism'},
                ],
                value='negmas.apps.scml.SCMLWorld',
                id="run_option",
                className="mt-1",
            ),
            dcc.Upload(
                id='new-config-path',
                children=html.Div([
                    'Config file path ... ',
                ]),
                style={
                    'width': '85%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
            ),
            html.Div(id='output-data-upload'),
            dbc.Button("Run", color="secondary", className="btn-block", id="run"),
        ]
    ),
    className="mt-3",
)

run_offline = dbc.Card(
    dbc.CardBody(
        [
            html.P("Monitor a component", className="card-text"),
            dbc.Input(
                placeholder='Checkpoint folder ...',
                type='file',
                value='',
                id="checkpoint-folder",
                className="mt-1",
            ),
            dbc.Input(
                placeholder='[Optional] component ID',
                type='text',
                value='',
                id="checkpoint-id",
                className="mt-1",
            ),
            dbc.Checklist(
                options=[
                    {'label': 'Watch Folder', 'value': 'watch'},
                ],
                value=[],
                id="checkpoint-options",
                className="mt-1",
            ),
            dbc.Button("Monitor")
        ]
    ),
    className="mt-3",
)

main_entry_body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Container(
                            [
                                dbc.Row(
                                    [
                                        html.H2("Load"),
                                    ],
                                ),
                                dbc.Row(
                                    [
                                        dbc.Tabs(
                                            [
                                                dbc.Tab(run_online, label="Online", tab_id="online"),
                                                dbc.Tab(run_offline, label="Offline", tab_id="offline"),
                                            ],
                                            id="open-tabs",
                                            active_tab="online",
                                        ),
                                    ],
                                ),
                                dbc.Row(
                                    [
                                        html.H2("Children"),
                                    ],
                                ),
                                dbc.Row(
                                    [
                                        html.P("Children will appear here")
                                    ],
                                ),
                            ],
                            className="mt-0",
                        ),
                    ],
                    md=3,
                ),
                dbc.Col(
                    [
                        html.H2("Showing xyz (ID fdfdsf)", id="basic"),
                        html.Div(id="main_widget")
                    ],
                    md=9,
                ),
            ]
        )
    ],
    className="mt-0",
)

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

# control bar

# _right_up_group_runnable_component = dbc.Row(                         
#     [
#         dbc.Col(
#             [
#                 dbc.Progress(id="progress", value=0, striped=True, animated=True),
#                 dcc.Interval(id="interval", interval=250, n_intervals=0),
#                 html.I(id="step_backward", n_clicks=0, className='fa fa-step-backward fa-lg'),
#                 html.I(id="play", n_clicks=0, className='fa fa-play'),
#                 html.I(id="step_forward", n_clicks=0, className='fa fa-step-forward')
#             ]
#         ),
#         dbc.Col(
#             [
#                 dbc.Button('test'),
#             ]
#         ),
#     ]
# )

_right_up_group_runnable_component = dbc.Row(
    [
        dbc.Col(
            [
                daq.GraduatedBar(id="negmas-progress", max=100, value=0),
                html.I(id="negmas-step-backward", n_clicks=0, className='fa fa-step-backward fa-lg'),
                html.I(id="negmas-play", n_clicks=0, className='fa fa-play'),
                html.I(id="negmas-step-forward", n_clicks=0, className='fa fa-step-forward'),
                daq.NumericInput(
                    id='negmas-step',
                    min=0,
                    value=0,
                    max=MAX_STEP,
                ),
            ]
        ),
        dbc.Col(
            [
                dbc.Label("Checkpoint every"),
                daq.NumericInput(
                    id='negmas-checkpoint-every',
                    min=1,
                    value=1,
                    max=MAX_CHECKPOINT_EVERY,
                ),
                dbc.Checkbox(
                    id="negmas-copy-checkpoints"
                ),
                dbc.Label("Copy Checkpoints"),
                dbc.Button(
                    "Fork", 
                    id="negmas-fork", 
                    color="secondary", 
                    className="mr-1"
                ),
            ]
        ),
        dbc.Col(
            [
                dbc.Label("n. Widgets"),
                daq.NumericInput(
                    id='negmas-number-widgets',
                    min=1,
                    value=4,
                    max=MAX_NUMBER_WIDGETS,
                ),
            ]
        )
    ]
)

_back_to_parent = dbc.Row(
    dcc.Link(dbc.Button("back_to_parent", id="back_to_parent", outline=True, color="secondary", className="mr-1"), href="/backToParent"),
)
