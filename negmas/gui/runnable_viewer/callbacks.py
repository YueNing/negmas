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
from negmas.sao import SAOMechanism
from negmas.apps.scml import SCMLWorld
from negmas.visualizers import VISUALIZERS, visualizer
from negmas.helpers import get_full_type_name, instantiate, get_class

from typing import Optional

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
    """
    visualizer run callback has two option, 
    1. runner(Optional[SAOMechanism, SCMLWorld]) has member visualizer, just directly use visualizer member
    2、search from VISUALIZER
    3. use visualizer to get a new Visualizer
    
    """
    print('====================Debug Information for run_callback===========================================')
    print(f'n_clciks: {n_clicks}, run_option: {run_option}, filename: {filename} !!')
    
    # get config from json file
    run_config = parse_contents(config_contents, filename, date)
    
    # get the runner instance
    runner: Optional[SAOMechanism, SCMLWorld] = get_class(run_option)(**run_config)
    
    # get the runner_visualizer
    try:    
        # get the runner_visualizer from runner member
        runner_visualizer = runner.visualizer
    except:
        try:
            # if already register in VISUALIZERS, get visualizer type from VISUALIZERS
            runner_visualizer = get_class(VISUALIZERS[run_option])(runner)
        except:
            # search a new Visualizer
            runner_visualizer = visualizer(runner)

    try:
        runner_visualizer.object.run()
        # use attribute checkpointrunner of run_callback, step_by_step to check the result 
        run_callback.checkpointrunner = CheckpointRunner(folder=runner_visualizer.object.checkpoint_folder)
        run_callback.checkpointrunner.run()
    except Exception as e:
        print(f"Running Callback failure: {e} !")
    
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
    run_callback.checkpointrunner.loaded_object()

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

