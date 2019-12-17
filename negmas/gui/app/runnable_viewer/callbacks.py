from negmas.gui import app
from negmas.helpers import get_class
from dash.dependencies import Input, Output, State
import dash_html_components as html
import base64
import pandas as pd
import io
import json
from typing import Dict, List
from negmas.checkpoints import CheckpointRunner
from negmas.sao import SAOMechanism
from scml.scml2019 import SCMLWorld
from negmas.visualizers import VISUALIZERS, visualizer
from negmas.helpers import get_full_type_name, instantiate, get_class
from negmas.utilities import UtilityFunction
from typing import Optional, Union

from negmas.gui.app.runnable_viewer.layout import layout
from negmas.gui.app.utils import render, set_callbacks
from negmas.gui.app.named_viewer.layout import layout
from negmas.gui.app.named_viewer.callbacks import *
from negmas.gui.app.layouts.page_layout import set_dynamically_layout

# cache used for cache expensive computate
from negmas.gui.app import cache, app
from negmas.gui.app.settings import DEBUG, DEFAULT_RUNNABLE_PARAMS, DEFAULT_NUMBER_WIDGETS

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
    
    # Need to pre-analyse the config, defined in json file and default config from settings.py
    def _pre_check_config(run_option, run_config: dict) -> List:
        assert(run_option == run_config["type"])
        del run_config["type"]
        if run_option == "negmas.sao.SAOMechanism":
            if 'negotiators' in run_config:
                if type(run_config['negotiators']) == list:
                    negotiators =  run_config.get('negotiators', None)
                elif type(run_config['negotiators']) == str:
                    negotiators = [get_class(_) for _ in run_config['negotiators'].replace(" ", "").split(',')]
                del run_config['negotiators']
            if 'mapping_utility_function' in run_config:
                if type(run_config['mapping_utility_function']) == str:
                    mapping_utility_function = get_class(run_config['mapping_utility_function'].strip())
                elif issubclass(run_config['mapping_utility_function'], UtilityFunction):
                    mapping_utility_function = run_config.get("mapping_utility_function", None)
                del run_config['mapping_utility_function']
            return run_config, negotiators, mapping_utility_function
        if run_option == "negmas.apps.scml.SCMLWorld":
            return run_config,
    
    # prepare the configs
    if filename is not None:
    # get config from json file
        run_config = parse_contents(config_contents, filename, date)
        config, *run_setting = _pre_check_config(run_option, run_config)
        # import pdb;pdb.set_trace()
    else:
        try:
            run_config = DEFAULT_RUNNABLE_PARAMS[run_option]
            # config pass through the runner, and run_setting are all config that needed by the runner
            config, *run_setting = _pre_check_config(run_option, run_config)
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
            ufuns = run_setting[1].generate_random(len(run_setting[0]), run_config['outcomes'])
            for i in range(len(run_setting[0])):
                runner.add(run_setting[0][i](name=f"agent{i}"), ufun=ufuns[i])
        if run_option == 'negmas.apps.scml.SCMLWorld':
            # TODO run the SCMLWorld
            runner = get_class(run_option)(**config)

    except Exception as e:
        if DEBUG:
            print(f"Can not get runner instance!: {e}")
        return "/"
    
    import pdb;pdb.set_trace()

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

    # try:
    run_callback.runner_visualizer.object.run()
    # dynamically set the init layout of runnable object

    # run_callback.components = []
    # save the layout components
    run_callback.components = set_runnable_dynamically_layout_callback()
    set_dynamically_layout(run_callback)

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
                widget = run_callback.runner_visualizer.render_widget(widget_name)
                dataframe[widget_name] = render(widget)
                if widget_name == 'children':
                    # need this widget to setup callback function
                    run_callback.widget_children = widget
        
        return dataframe
    
    return query_and_serialize_data(n, session_id)

def set_runnable_dynamically_layout_callback():
    """just call once, to set callback function and layout of runnable page"""

    # get data frame from cache, format is dict
    # first time to calculte the dataframe and get the dynamically layout and set callback function

    result = _compute_runnable_data(0, 'init')
    graph_components = [(f'graph{k+1}', 'figure') for k in range(len(result) - 2)]
    run_callback.graph_components = graph_components
    run_callback.init_result = result

    components = [
        {'func':update_runnable_callback, 
        'output':[('basic_info', 'children'), ('children', 'children')] + graph_components, 
        'input':[('interval-component', 'n_intervals'), ('session_id', 'children')], 
        }
    ]
    # set callback function for children component
    # subchildren-{m} subchildren-negotiators {'negotiators':[a1, a2], 'consumers':[c1, c2]}
    # import pdb;pdb.set_trace()
    try:
        for m in run_callback.widget_children.content:
            components.append(
                {'func':toggle_collapse, 
                'output':[(f'subchildren-{m}-collapse', 'is_open')], 
                'input':[(f'subchildren-{m}', 'n_clicks')], 
                'state':[(f'subchildren-{m}-collapse', 'is_open')]
                }
            )
            components.append(
                {'func':set_navitem_class, 
                'output':[(f'subchildren-{m}', 'className')], 
                'input':[(f'subchildren-{m}-collapse', 'is_open')]
                }
            )
        
    except:
        pass
    # import pdb;pdb.set_trace()
    set_callbacks(components, app)
    return components
    # set_callbacks(components)

def _compute_runnable_data(n, session_id):
    """get new page data"""
    df = get_dataframe(n, session_id)

    show_graphs = []
    if len(df['graphs']) > DEFAULT_NUMBER_WIDGETS:
        show_graphs = df['graphs'][:DEFAULT_NUMBER_WIDGETS]
    else:
        show_graphs = df['graphs'] + [render('empty')]*(DEFAULT_NUMBER_WIDGETS-len(df['graphs']))
    
    result = tuple([df['basic_info'], df['children']] + show_graphs)
    return result

def update_runnable_callback(n, session_id):
    """exactly callback function of runnable object"""
    print("update_runnable_callback")
    try:
        return _compute_runnable_data(n, session_id)
    except:
        # if callback except error, means the layout and callback function are not successfully init
        # need to init it and then return the result
        try:
            set_runnable_dynamically_layout_callback()
            return _compute_runnable_data(n, session_id)
        except:
            if DEBUG:
                print(f'error when update the runnable page!')
            else:
                pass



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
    if not(n_clicks==0):
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
            return False
        else:
            # open the control-info error alert, later use timecounter redirct to first page (select runnable object)
            return True
    return False

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
    if not(n_clicks==0) :
        if hasattr(run_callback, 'checkpointrunner'):
            try:
                next_step = run_callback.checkpointrunner.next_step
                run_callback.checkpointerrunner.goto(next_step)
                return False
            except:
                if DEBUG:
                    print(f"Something wrong when goto next step")
                    return True
                else:
                    return True
        else:
            return True
        
    return False

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
    if not(n_clicks==0):
        # if exist runn_callback.checkpointerrunner, then can control the obejct goto previous step
        if hasattr(run_callback, 'checkpointrunner'):
            try:
                previous_step = run_callback.checkpointrunner.previous_step
                run_callback.checkpointerrunner.goto(previous_step)
            except:
                if DEBUG:
                    print(f"Something wrong when goto previous step")
                else:
                    return True
        else:
            return True
    return False