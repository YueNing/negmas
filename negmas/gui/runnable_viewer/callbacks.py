from negmas.gui import app
from negmas.helpers import get_class
from dash.dependencies import Input, Output, State
import dash_html_components as html
import base64
import pandas as pd
import io
import json
from typing import Dict
from negmas.checkpoints import CheckpointRunner
from negmas.sao import SAOMechanism
from negmas.apps.scml import SCMLWorld
from negmas.visualizers import VISUALIZERS, visualizer
from negmas.helpers import get_full_type_name, instantiate, get_class
from typing import Optional, Union

from negmas.gui.runnable_viewer.layout import layout
from negmas.gui.utils import render
# cache used for cache expensive computate
from negmas.gui import cache
from negmas.gui.settings import DEBUG, DEFAULT_RUNNABLE_PARAMS

def parse_contents(contents, filename, date) -> Dict:
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    # print(decoded)
    try:
        if 'json' in filename:
            # Assume that the user uploaded an json file
            configs = json.loads(decoded)
    except Exception as e:
        if DEBUG:
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

    Note: run_callback.checkpointrunner.loaded_object === run_callback.runner_visualizer.object
    """

    print('====================Debug Information for run_callback===========================================')
    print(f'n_clciks: {n_clicks}, run_option: {run_option}, filename: {filename} !!')
    
    # Need to pre analyse the config, defined in json file
    def _pre_check_config(run_option, run_config: dict):
        if run_option == "negmas.sao.SAOMechanism":
            if 'negotiators' in run_config:
                negotiators = run_config.get('negotiators', None)
                del run_config['negotiators']
            if 'mapping_utility_function' in run_config:
                mapping_utility_function = run_config.get("mapping_utility_function", None)
                del run_config['mapping_utility_function']
            return run_config, negotiators, mapping_utility_function

    if filename is not None:
    # get config from json file
        run_config = parse_contents(config_contents, filename, date)
        config, negotiators, mapping_utility_function = _pre_check_config(run_option, run_config)

    else:
        try:
            run_config = DEFAULT_RUNNABLE_PARAMS[run_option]
            config, negotiators, mapping_utility_function = _pre_check_config(run_option, run_config)
        except Exception as e:
            if DEBUG:
                print(f"Can not get Default config of {run_option}, Please add Default Config in file settings")
            return '/'
            
    # get the runner instance
    try:
        # TODO: get the runnable object ,later need to config something, 
        # for example add Negotiators into Mechanism
        if run_option == 'negmas.sao.SAOMechanism':
            runner = get_class(run_option)(**config)
            ufuns = mapping_utility_function.generate_random(len(negotiators), run_config['outcomes'])
            for i, negotiator in enumerate(negotiators):
                runner.add(negotiator(name=f"agent{i}"), ufun=ufuns[i])
    except Exception as e:
        if DEBUG:
            print(f"Can not get runner instance!: {e}")
        return "/"
    
    try:
        # run the exactly runner, will create a folder
        runner.run()
    except Exception as e:
        if DEBUG:
            print(f"Something Wrong when running the runner: {e}")
        return '/'
    
    # use attribute checkpointrunner of run_callback, step_by_step to check the result 
    run_callback.checkpointrunner = CheckpointRunner(folder=runner._CheckpointMixin__checkpoint_folder)
    run_callback.checkpointrunner.step()

    # set the predefined layout base on the checkpointrunner instance
    run_callback.layout = layout(type(run_callback.checkpointrunner.loaded_object))

    # get the runner_visualizer
    try:    
        # get the runner_visualizer from runner member
        run_callback.runner_visualizer = run_callback.checkpointrunner.loaded_object.visualizer
    except:
        # search a new Visualizer and set object as runner
        run_callback.runner_visualizer = visualizer(run_callback.checkpointrunner.loaded_object)

    try:
        run_callback.runner_visualizer.object.run()
        # run_callback.checkpointrunner.run()
    
    except Exception as e:
        if DEBUG:
            print(f"Running Callback failure: {e} !")
        return '/'
    
    print("==========================End Debug Information===================================================")
    return '/run'


@app.callback(Output('new-config-path', 'children'), [Input('new-config-path', 'filename')])
def config_file_callback(filename):
    if filename is not None:
        return html.Div(filename.split('.')[0])
    else:
        return html.Div('Config file path ... ')



def get_dataframe(n, session_id):
    """
    Use flask_caching.Cache base on session_id to calculate the visualizer data and store it
    """
    @cache.memoize()
    def query_and_serialize_data(n, session_id):
        # just widgets basic_info, childrens, graphs needed to update
        dataframe = {
            'graphs':[], 
            'basic_info': None, 
            'childrens': None,
            }

        for widget_name in run_callback.runner_visualizer.widget_names():
            if run_callback.runner_visualizer.widget_kind(widget_name) == "graph_data":
                # Put all graph objects into a list
                dataframe['graphs'].append(render(
                    run_callback.runner_visualizer.render_widget(widget_name)
                ))
            else:
                # put another widget directly in dict dataframe
                dataframe[widget_name] = render(run_callback.runner_visualizer.render_widget(widget_name))
                
        return dataframe
    
    return query_and_serialize_data(n, session_id)

@app.callback(
    [
        Output('basic_info', 'children'),
        Output('childrens', 'children'),
        Output('graph1', 'figure'),
        Output('graph2', 'figure'),
        Output('graph3', 'figure'),
        Output('graph4', 'figure')
    ],
    [
        Input('interval-component', 'n_intervals'),
        Input('session_id', 'children'),
    ]
)
def update_page_default_layout(n, session_id):
    """
    Update entire page at once
    """

    # TODO: if session_id is changed, redirct to page /, means for another user

    # get data frame from cache, format is dict
    df = get_dataframe(n, session_id)

    if len(df['graphs']) > 4:
        show_graphs = df['graphs'][:4]
    else:
        show_graphs == df['graphs'] + [render('empty')]*(4-len(df['graphs']))
    
    result = tuple([df['basic_info'], df['childrens']] + show_graphs)

    return result


#TODO: control bar callback functions

@app.callback(
    Output('control-info-stop-start-error', 'is_open'),
    [
        Input('negmas-play', 'n_clicks')
    ]
)
def control_stop_start(n_clicks):
    """
    Contorl the negmas running
    """
    
    # first check wether exist a runnable object in run_callback
    if hasattr(run_callback, 'runner_visualizer'):
        # if exist a runnable obejct, then check this object is runnning or not
        if run_callback.runner_visualizer.obejct.running:    
            # stop this runnable object ,set the _running property as False 
            run_callback.runner_visualizer.object._running, run_callback.runner_visualizer.object._timedout = False, True
            run_callback.runner_visualizer.object.on_negotiation_end()
        else:
            # TODO: then resume this object and run again????     
            run_callback.runner_visualizer.object = run_callback.checkpointrunner.loaded_object
            run_callback.runner_visualizer.object.run()
    else:
        # open the control-info error alert, later use timecounter redirct to first page (select runnable object)
        return True

@app.callback(
    Output('control-info-next-step-error', 'is_open'),
    [
        Input('negmas-step-forward', 'n_clicks')
    ]
)
def control_next_step(n_clicks):
    """
    Contorl the negmas step
    """
    if hasattr(run_callback, 'checkpointrunner'):
        try:
            next_step = run_callback.checkpointrunner.next_step
            run_callback.checkpointerrunner.goto(next_step)
        except Exception as e:
            if DEBUG:
                raise(f"Something wrong when goto next step: {e}")
            else:
                return True
    else:
        return True

@app.callback(
    Output('control-info-previous-step-error', "is_open"),
    [
        Input('negmas-step-backward', 'n_clicks')
    ]
)
def control_previous_step(n_clicks):
    """
    Contorl the negmas step
    """
    
    # if exist runn_callback.checkpointerrunner, then can control the obejct goto previous step
    if hasattr(run_callback, 'checkpointrunner'):
        try:
            previous_step = run_callback.checkpointrunner.previous_step
            run_callback.checkpointerrunner.goto(previous_step)
        except Exception as e:
            if DEBUG:
                raise(f"Something wrong when goto previous step: {e}")
            else:
                return True
    else:
        return True

# @app.callback(
#     Output('url', 'pathname'),
#     [
#         Input('control-info-next-step-error', 'is_open'),
#         Input('control-info-previous-step-error', 'is_open'),
#         Input('control-info-stop-start-error', 'is_open'),
#     ]
# )
# def redirct_to(cins_is_open, cips_is_open, ciss_is_open):
#     """
#     control redirct mode
#     """
#     import time
#     time.sleep(3)
#     if cins_is_open or cips_is_open or ciss_is_open:
#         return '/', False, False, False
#     else:
#         return '/run', False, False, False

