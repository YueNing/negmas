import dash_core_components as dcc 
import dash_bootstrap_components as dbc 
import dash_html_components as html
import plotly

from typing import Union, List
from negmas.visualizers import Widget

def render(widget: Union[str, Widget]) -> List[str]:
    """
    TODO:
    Render all widget content here, convert Widget to html
    return are widget name and rendered widget html content.
    """
    if isinstance(widget, Widget):
        if(widget.kind == "graph_data"):
            # here just need to get the id of widget and update the data below
            # example offer_utils, update the data of figure base on the id
            # of dcc.Graph
            figure = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
            figure = {'data':Widget.content['data'], 'params':widget.params}
            return figure
        elif(widget.kind == "dict"):
            # TODO: return the basic info, kind is dict
            return [widget.content.name, 
                html.Div(
                    id=widget.content.id, 
                    children=[]
                )
            ]   
    
    elif type(widget) == dict:
        # TODO: here is for children component, render here as dropmenu
        return [
            "childrens", 
            dcc.dropmenu(),
        ]
    elif type(widget) == str:
        # if input widget is str, for this version, is the widget name, 
        # need to convert this widget to a html code, as predefined, used for later,
        # when realistic data are converted also into html code based on the id of widget
        # for example basic_info, 'self.object.id_basic_info' is the id of this widget,
        # widget as a graph, here set figure as blank
        if(widget.kind == 'graph_data'):
            return [
                widget.kind,
                dcc.Graph(
                    id=widget.content.id,
                )
            ]

