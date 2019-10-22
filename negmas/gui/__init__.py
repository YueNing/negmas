import flask
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
# from named_viewer.layout import layout as named_viewer_layout
# from runnable_viewer.layout import layout as runnable_view_layout

# 'https://codepen.io/chriddyp/pen/bWLwgP.css',
external_style_sheets = [dbc.themes.CERULEAN]

app = dash.Dash(__name__, external_stylesheets=external_style_sheets)
url_bar_and_content_div = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        html.Div(
            id='page-content'
        ),
        html.Div(id='intermediate-value', style={'display': 'none'})
    ]
)

def serve_layout():
    """ 
        used for pre-define the class id, 
        can import callback before render the layout
    """
    if flask.has_request_context():
        return url_bar_and_content_div
    return html.Div([
        url_bar_and_content_div,
        main_entry_layout,
        run_online,
        run_offline,
    ])

app.layout = serve_layout

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
                    {'label': 'Negotiation', 'value': 'negmas.mechanisms.Mechanism'},
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

main_entry_layout = html.Div([navbar, main_entry_body], style={"width": "100%"})