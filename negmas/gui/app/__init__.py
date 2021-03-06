import flask
import dash
import uuid
from dash.dependencies import Input, Output, State
from flask_caching import Cache
from typing import List
from pathlib import Path

# set the negmas path, just used for test and debug
import sys
sys.path.insert(0,'c:/Users/n1085/Documents/GitHub/negmas')

from negmas.gui.app.settings import *
from negmas.gui.app.layouts.widget_layout import base, index_string
from negmas.gui.app.layouts.page_layout import PAGE_404
from negmas.helpers import get_full_type_name, instantiate, get_class

# runnable and named layouts
from negmas.gui.app.runnable_viewer.layout import layout as runnable_viewer_layout
from negmas.gui.app.named_viewer.layout import layout as named_viewer_layout
from negmas.gui.app.utils import validate_settings

# initial the dash app
f_app = flask.Flask(__name__)
app = dash.Dash(__name__, 
                external_stylesheets=EXTERNAL_STYLE_SHEETS, 
                server=f_app,
                assets_folder=ASSETS_FOLDER,
                index_string=index_string)

app.config.suppress_callback_exceptions = True
# set cache config for dash app
cache = Cache(app.server, config=CACHE_CONFIG)

def serve_layout():
    """ 
        used for pre-define the class id, 
        can import callback before render the layout,
        Call this function before run the dash server, 
        Can add setting check code here
    """
    # check the settings whether available
    assert validate_settings(Path('./settings.py'))

    if flask.has_request_context():
        return base
    
    # Get all runnable object layouts
    runnable_layouts: List = [runnable_viewer_layout(get_class(runnable)) for runnable in RUNNABLES]

    # import pdb;pdb.set_trace()
    # TODO: Get all named object layouts
    named_layouts: List = [named_viewer_layout(get_class(named)) for named in NAMED] 
    
    # The unique session_id, prepared for multi user
    session_id: str = str(uuid.uuid4())
    
    return html.Div([
        html.Div(session_id, id="negmas-session_id", style={'display':'none'}),
        base,
        HOME_PAGE,
    ] + runnable_layouts + named_layouts)

app.layout = serve_layout

# load callback function from module 
from negmas.gui.app.runnable_viewer.callbacks import run_callback

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    """ routing """
    if pathname ==  '/':
        return HOME_PAGE
    if pathname == '/load':
        return
    if pathname == '/run':
        # get the /run router, return the relative layout
        return run_callback.layout
    else:
        return PAGE_404

if __name__ == "__main__":
    app.run_server(debug=True)