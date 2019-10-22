from negmas.gui import app
from negmas.helpers import get_class
from dash.dependencies import Input, Output, State
import dash_html_components as html
import base64
import pandas as pd
import io
import json

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    # print(decoded)
    try:
        if 'json' in filename:
            # Assume that the user uploaded an json file
            configs = json.loads(decoded)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    
    return configs

@app.callback(
    Output('url', 'pathname'),
    [Input('run', 'n_clicks')],
    [State('run_option', 'value'), 
    State('new-config-path', 'contents'), 
    State('new-config-path', 'filename'),
    State('new-config-path', 'last_modified')])
def run_callback(n_clicks, run_option, config_contents, filename, date):
    print('====================Debug Information for run_callback===========================================')
    print(f'n_clciks: {n_clicks}, run_option: {run_option}, filename: {filename} !!') 
    run_config = parse_contents(config_contents, filename, date)
    run_type = get_class(run_option)
    try:
        if run_type == get_class('negmas.apps.scml.world.SCMLWorld'):
            scmlworld = run_type.load_from_config()
        elif run_type == get_class('negmas.situated.World'):
            world = run_type.load_from_config()
        elif run_type == get_class('negmas.mechanisms.Mechanism'):
            mechanism = run_type.load_from_config()
        else:
            print("can not get the run class!!!")
    except Exception as e:
        print(e)
        print("need to realize the function load_from_config()")
 
    print(f"run_type={run_type}")
    print("==========================End Debug Information===================================================")
    return '/run'

@app.callback(Output('new-config-path', 'children'), [Input('new-config-path', 'filename')])
def config_file_callback(filename):
    if filename is not None:
        return html.Div(filename.split('.')[0])
    else:
        return html.Div('Config file path ... ')