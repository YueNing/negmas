"""
Define all widgets layout here
"""
import dash_daq as daq
from negmas.gui.app.settings import *
import dash_core_components as dcc

_interval_one_second = dcc.Interval(
    id="negmas-interval-component",
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
        # why here need to set refresh as true, 
        # when set false, can not automatically call the register callback function
        # ??????
        dcc.Location(id='url', refresh=True),
        html.Div(
            [control_info_stop_start_error, control_info_previous_step_error, control_info_next_step_error]
        ),
        html.Div(
            id='page-content'
        ),
        html.Div(id='intermediate-value'),
    ]
)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Settings", href="/settings")),
        html.Div(id="view-on-github", children=[
            html.A(dbc.Row([
                        html.Img(id="github-marker",src="https://i.loli.net/2019/12/08/Bl7EyhWIHdVuQGq.png"),
                        dbc.NavItem(dbc.NavLink("View on Github", href="https://github.com/yasserfarouk/negmas")),
                    ]
                ), href="https://github.com/yasserfarouk/negmas")

        ])
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
                options=[dict(label=runnable.split('.')[-1], value=runnable) for runnable in RUNNABLES],
                value=RUNNABLES[0],
                id="run_option",
                className="mt-1",
            ),
            dcc.Upload(
                id='new-config-path',
                children=html.Div([
                    'Config file path ... ',
                ]),
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
            dcc.Upload(
                id='offline-checkpoint-file',
                children=html.Div([
                    'Checkpoint file',
                ]),
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
            dbc.Button("Monitor", color="secondary", className="btn-block", id="monitor"),
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
                            ],
                            className="mt-0",
                        ),
                    ],
                    md=3,
                ),
            ]
        )
    ],
    className="mt-0",
)

# left up button group compose of four buttons,  Run New, Run From Checkpoint, Tournament, Setting
_left_up_button_group = dbc.Row(
    [
        dcc.Link(dbc.Button("Run New", id="run_new", color="secondary", className="btn-block"), href="/run_new"),
        dcc.Link(dbc.Button("Run From Checkpoint", color="secondary", className="btn-block"), href="/checkpoint"),
        dcc.Link(dbc.Button("Tournament", color="secondary", className="btn-block"), href="/tournament"),
        dcc.Link(dbc.Button("Setting", color="secondary", className="btn-block"), href="/setting"),
    ],
                    
)

_new_checkpoint = dbc.Row(
    [
        dcc.Link(dbc.Button("Save Checkpoint", id="save_checkpoint", color="secondary", className="mr-1"), href="/save_newCheckpoint"),
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
                daq.GraduatedBar(id="negmas-progress", max=100, value=50),
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
    dcc.Link(dbc.Button("back_to_parent", id="back_to_parent", color="secondary", className="mr-1"), href="/backToParent"),
)

index_string = """<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Negmas Visualizer</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""