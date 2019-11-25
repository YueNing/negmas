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

from negmas.gui.run_callback.layout import layout
from negmas.gui.utils import render

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
    
    member of function run_callback can be used

    param run_callback.layout:
    param run_callback.checkpointrunner:
    param run_callback.runner_visualizer:
    """

    print('====================Debug Information for run_callback===========================================')
    print(f'n_clciks: {n_clicks}, run_option: {run_option}, filename: {filename} !!')

    # get config from json file
    run_config = parse_contents(config_contents, filename, date)
    
    # get the runner instance
    runner: Optional[SAOMechanism, SCMLWorld] = get_class(run_option)(**run_config)
    
    # use attribute checkpointrunner of run_callback, step_by_step to check the result 
    run_callback.checkpointrunner = CheckpointRunner(folder=runner.checkpoint_folder)
    
    # set the predefined layout base on the checkpointrunner instance
    run_callback.layout = layout(checkpointrunner.loaded_object())

    # get the runner_visualizer
    try:    
        # get the runner_visualizer from runner member
        run_callback.runner_visualizer = checkpointrunner.loaded_object().visualizer
    except:
        # search a new Visualizer and set object as runner
        run_callback.runner_visualizer = visualizer(checkpointrunner.loaded_object())

    try:
        run_callback.runner_visualizer.object.run()
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
    TODO: Live cache data, update this data later use function update_runnable_viewer 
    """
    obj = run_callback.checkpointrunner.loaded_object()

    basic_info_rendred = render(run_callback.runner_visualizer.render_widget('basic_info'))
    graphs_data_rendred = {
        'offer_utils': render(run_callback.runner_visualizer.render_widget('offer_utils'))
    }
    return {
        'basic_info_rendred': basic_info_rendred, 
        'childrens_rendred': childrens_rendred,
        'graphs_data_rendred': graphs_data_rendred,
        }


@app.callback(
    for widget_name in run_callback.runner_visualizer.widget_names:
        if run_callback.runner_visualizer.widget_kind(widget_name) == 'graph_datas':
            Output(f'{run_callback.runner_visualizer.object.id}_{widget_name}', 'figure')
        elif widget_name == 'basic_info':
            Output(f'{run_callback.runner_visualizer.object.id}_{widget_name}', 'basivc_info')
        elif widget_name == 'childrens':
            Output(f'{run_callback.runner_visualizer.object.id}_{widget_name}', 'childrens')
    [Input('data_cache', 'children')]
)
def update_runnable_viewer(cached_data):
    """
    When detect cached data, live update the graphs in runnable_viewer
    """
    # TODO: not Implemented
    for rendered_widget_name, rendered_data in cached_data.items():
        
    