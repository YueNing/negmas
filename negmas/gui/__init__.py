import flask
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq 
import uuid
from dash.dependencies import Input, Output, State
from flask_caching import Cache
from negmas.gui.runnable_viewer.layout import layout as runnable_viewer_layout
from negmas import Mechanism
from negmas.gui.settings import *
from negmas.gui.layouts.widget_layout import base
from negmas.helpers import get_full_type_name, instantiate, get_class
# from named_viewer.layout import layout as named_viewer_layout
from negmas.gui.runnable_viewer.layout import layout as runnable_viewer_layout
from negmas.gui.named_viewer.layout import layout as named_viewer_layout
from typing import List

# 'https://codepen.io/chriddyp/pen/bWLwgP.css',
external_style_sheets = [dbc.themes.CERULEAN]

app = dash.Dash(__name__, external_stylesheets=external_style_sheets)
cache = Cache(app.server, config=CACHE_CONFIG)

def serve_layout():
    """ 
        used for pre-define the class id, 
        can import callback before render the layout
    """
    if flask.has_request_context():
        return base
    
    # Get all runnable object layouts
    runnable_layouts: List = [runnable_viewer_layout(get_class(runnable)) for runnable in RUNNABLES]

    # TODO: Get all named object layouts
    named_layouts: List = [named_viewer_layout(get_class(named)) for named in ] 
    
    # The unique session_id, prepared for multi user
    session_id: str = str(uuid.uuid4())
    
    return html.Div([
        html.Div(session_id, id="session_id", style={'display':'none'}),
        base,
        HOME_PAGE,
    ] + runnable_layouts)