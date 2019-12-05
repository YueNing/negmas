import dash_core_components as dcc 
import dash_bootstrap_components as dbc 
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly

from typing import Union, List
from negmas.visualizers import Widget
import sys
from textwrap import dedent

def render(widget: Union[str, Widget]) -> Union[list, dict]:
    """
    TODO:
    Render all widget content here, convert Widget to html
    return are widget name and rendered widget dash html content.
    The input are dict or Widget
    ..version 0.1.1 
    Widget: basic_info, offer_utils, childrens
    """
    if isinstance(widget, Widget):
        # render the basic info and offer_utils(graph widget)
        if widget.kind == "dict":
            # directly get the data from content, such as, id, name and type in basic_info
            # widget.content is a dictionary, use Table to render the content
            return [
                dbc.Table(
                    [html.Tbody([html.Tr([html.Td(k), html.Td(v)]) for k, v in widget.content.items()])],
                    bordered=True,
                    dark=True,
                )
            ]
        elif widget.kind == "dict_list_dict":
            #render for childrens, format {'':[{}, {}, {}], need to set a sidebar not navigate the children
            sub_menus = []
            for m in widget.content:
                # set the layout component 
                sub_menu = [
                    html.Li(
                        dbc.Row(
                            [   
                                # Children group name, such as, Negotiators
                                dbc.Col(m),
                                dbc.Col(
                                    html.I(className="fas fa-chevron-right mr-3"), width="auto"
                                ),
                            ],
                        ),
                        id=f"subchildren-{m}"
                    ),
                    dbc.Collapse([dbc.NavLink(w['name'], href=f"/childrens/{m}/{w['name']}") 
                                    for w in widget.content[m]],
                                id=f"subchildren-{m}-collapse"
                                )
                ]

                sub_menus += sub_menu
            # set the component layout, need to later register relative callback function
            return [
                dbc.Nav(sub_menus, vertical=True)
            ]
        elif widget.kind == "graph_data":
            # get the data from content.data, such as, id, name and data in offer_utils
            # data are the data that need to insert into figure and update
            # widget.content.data [(agent1, agent2, agent3), (agent1, agent2, agent3),....]
            import pandas as pd 
            df = pd.DataFrame(widget.content['data'])
            # import pdb;pdb.set_trace()
            figure = dict(
                data = [
                    dict(
                        x=list(df.index),
                        y=df[a],
                        name=f'agent{a}',
                        mode=widget.params['mode'] if 'mode' in widget.params else 'lines',
                    )
                    for a in df
                ],
                layout=dict(
                    xaxis=widget.params['xaxis'] if 'xaxis' in widget.params else { 'title': 'X Axis'},
                    yaxis=widget.params['yaxis'] if 'yaxis' in widget.params else {'title': 'Y Axis'},
                    margin=widget.params['margin'] if 'margin' in widget.params else {'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend=widget.params['legent'] if 'legend' in widget.params else {'x': 0, 'y': 1},
                    hovermode=widget.params['hovermode'] if 'hovermode' in widget.params else 'closest',
                )
            )

            return figure
    
    return {}

# TODO:
# dynamically creating callbacks for a dynamically created layout
def create_callback(output_element,retfunc,name='callback'):
    """creates a callback function"""
    def callback(*input_values):
        print ('callback fired with :"{}"'.format(input_values))
        print(retfunc)
        retval = []
        if input_values is not None and input_values!='None':
            try:
                retval = retfunc(*input_values)
            except Exception as e:
                print(f"error when create callback function params are {input_values} error is {e}")  
        return retval                    
    return callback

def getComponentId(name):
    return f"negmas-{name}"

def register_callback(callbacks, object_app):
    """register callback for app callback"""
    print(f"registering {len(callbacks)} callbacks for negmas.gui")
    
    for callback_data in callbacks:
        dynamically_generated_function = create_callback(callback_data[0], callback_data[3])
        object_app.callback(output=callback_data[0], inputs=callback_data[1],state=callback_data[2])(dynamically_generated_function)
        # import pdb;pdb.set_trace()

def define_callback(output, input, func=None, state=None):
    """Defines the callback set"""
    return (
        [Output(getComponentId(id), attr) for (id, attr) in output],
        [Input(getComponentId(id), attr) for (id,attr) in input],
        [] if state is None else [State(getComponentId(id), attr) for (id,attr) in state],
        dummy_callback if func is None else func
    )

def dummy_callback(*input_data):
    print('dummy callback with:', *input_data)
    return []

def set_callbacks(components: list, app):
    """set callbacks for the app, 
    input components: [{"output":[(),()], "input", "func":}, {}, {}, {}]
    output data: [(Output,[Input],[State],callback_func), ...]
    """
    # import pdb;pdb.set_trace()
    callbacks = [
        define_callback(c['output'], c['input'], 
            func=c['func'], state=c['state'] if 'state' in c else None
        ) for c in components
    ]
    # return all predefined callbacks, later just call register_callback when   
    # import pdb;pdb.set_trace()  
    # return callbacks
    register_callback(callbacks, app)


def show_callbacks(app):
    """show the callbacks of app, as following format
    callback      router @ router.py:25       
    Output        dash-container.children     
    Inputs     1  url.pathname                
    States     0     
    Events     0   
    """
    import os
    def wrap_list(items, padding=24):
        return ("\n"+" "*padding).join(items)

    def format_regs(registrations):
        vals = sorted("{}.{}".format(i['id'], i['property'])
                      for i in registrations)
        return wrap_list(vals)

    output_list = []

    for callback_id, callback in app.callback_map.items():
        wrapped_func = callback["callback"].__wrapped__
        inputs = callback["inputs"]
        states = callback["state"]

        if callback_id.startswith(".."):
            outputs = callback_id.strip(".").split("...")
        else:
            outputs = [callback_id]

        str_values = {
            "callback": wrapped_func.__name__,
            "outputs": wrap_list(outputs),
            "filename": os.path.split(wrapped_func.__code__.co_filename)[-1],
            "lineno": wrapped_func.__code__.co_firstlineno,
            "num_inputs": len(inputs),
            "num_states": len(states),
            "inputs": format_regs(inputs),
            "states": format_regs(states),
            "num_outputs": len(outputs),
        }

        output = dedent(
            """                                                                                                                                                                                                      
            callback    {callback} @ {filename}:{lineno}                                                                                                                                                             
            Outputs{num_outputs:>3}  {outputs}                                                                                                                                                                       
            Inputs{num_inputs:>4}  {inputs}                                                                                                                                                                          
            States{num_states:>4}  {states}                                                                                                                                                                          
            """.format(**str_values)
        )

        output_list.append(output)
    return "\n".join(output_list)

def validate_settings(filepath):
    """Check the settings of system before running the server"""
    return True