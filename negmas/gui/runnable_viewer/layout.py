
from negmas import NamedObject
from negmas.visualizers import *
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from negmas.gui.named_viewer import named_viewer_objects
from negmas.gui.named_viewer.layout import layout as named_viewer_layout
from negmas.gui.config import (Layout, 
                    _left_up_button_group, 
                    _right_up_group_runnable_component, 
                    _new_checkpoint, 
                    _back_to_parent, 
                    _interval_one_second
                )

def layout(object_type: Type[NamedObject]):

    # get class type defined as obejct_type
    v = visualizer_type(object_type)

    # layout id 
    layout_id = uuid.uuid4()
    
    # save all widgets content here
    widgets = [v.render_widget(widget, v.widget_params(widget)) for widget in v.widget_names()]
    
    # save all html here 
    children_layouts = [render(widget) for widget in widgets]

    # sorted the children_layouts as basic_info, childrens, graph_widgets
    children_layouts_dict = {"graph_widgets":[]}

    for children_layout in children_layouts:
        if children_layout[0] == "graph_data":
            children_layout["graph_widgets"].append(children_layout)
        else:
            children_layouts_dict[children_layout[0]] = children_layout[1]

    layout = html.Div(
        id=layout_id,
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Br(),
                            # [System] control bar, predefined
                            _left_up_button_group,
                            html.Br(),
                            children_layouts_dict["basic_info"],
                            html.Br(),
                            children_layouts_dict["childrens"],
                            html.Br(),
                            # [System] save, predefined 
                            _new_checkpoint
                        ],
                        width={"size":Layout["left"]["size"], "offset": 1}
                    ),
                    dbc.Col(
                        [
                            html.Br(),
                            _right_up_group_runnable_component,
                        ] + children_layouts_dict['graph_widgets']
                    )
                ]
            ),
            _interval_one_second
        ],
    )

    return layout

def render(widget: Optional[Widget]) -> List[str]:
    """
    Render all widget content here, convert Widget to html
    return are widget name and rendered wiget html content.
    """
    if isinstance(widget, Widget):
        if(widget.kind == "graph_data"):
            return [widget.kind, 
                dcc.Graph(
                    id = widget.content.id,
                    figure={},
                )
            ]
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
