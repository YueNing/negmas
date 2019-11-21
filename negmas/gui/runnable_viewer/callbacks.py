from negmas.gui import app
from negmas.helpers import get_class
from dash.dependencies import Input, Output, State
import dash_html_components as html
import base64
import pandas as pd
import io
import json
from typing import Dict
from negmas.visualizers import *
from negmas.checkpoints import CheckpointRunner


def parse_contents(contents, filename, date) -> Dict:
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
    
    # get config from json file
    run_config = parse_contents(config_contents, filename, date)
    
    # generate a visualizer
    run_visualizer = visualizer(get_class(run_option)(**run_config))
    
    # return the self.object in class visualizer

    print(f"run_type={run_type}")

    if run_visualizer.object is not None:
        run_visualizer.object.run()
    
    # use attribute checkpointrunner of run_callback, step_by_step to check the result 
    run_callback.checkpointrunner = CheckpointRunner(folder=run_visualizer.object.checkpoint_folder)

    run_callback.checkpointrunner.run()
    print("==========================End Debug Information===================================================")
    return '/run'

@app.callback(Output('new-config-path', 'children'), [Input('new-config-path', 'filename')])
def config_file_callback(filename):
    if filename is not None:
        return html.Div(filename.split('.')[0])
    else:
        return html.Div('Config file path ... ')

@app.callback(
    Output('data_cache', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def cache_runnable_viewer(n):
    """
    Live cache data, update this data later use function update_runnable_viewer 
    """
    run_callback.checkpointrunner.loaded_object().
    pass

@app.callback(
    Output('graphs_group', 'figure'),
    [Input('data_cache', 'children')]
)
def update_runnable_viewer(cached_data):
    """
    When detect cached data, live update the graphs in runnable_viewer
    """
    # TODO: not Implemented
    pass

