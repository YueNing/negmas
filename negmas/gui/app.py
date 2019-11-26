import dash
import sys
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as tbl
import dash_daq as daq
from typing import Type

from negmas import NamedObject
# from negmas.visualizers import *

from negmas.gui import app, main_entry_layout, serve_layout
from negmas.gui.settings import cache_config

# from named_viewer.callbacks import callbacks as named_viewer_callbacks
from negmas.gui.runnable_viewer.callbacks import run_callback, config_file_callback

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    """ routing """
    if pathname ==  '/':
        return main_entry_layout
    if pathname == '/load':
        return
    if pathname == '/run':
        # get the /run router, return the relative layout
        return run_callback.layout
    else:
        return '404'

def cli(debug=True):
    """Main entry point"""
    app.layout = serve_layout
    app.run_server(debug=debug)


if __name__ == "__main__":
    debug = False
    if len(sys.argv) > 1 and sys.argv[1] in ("debug", "--debug", "-d"):
        debug=True
    cli(debug=debug)
