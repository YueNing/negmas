"""
Basic config file, 
Layout: layout ratio
"""

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# DEBUG Mode
DEBUG = True

# Global Layout Setting params
LAYOUT_PARAMS = {
    "left":{"size": 4, "offset": 1},
    "right":{"size": 8, "layout":{"left":{"scale": 6}, "right":{"scale":6}}}
}

# Style for Sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# 'https://codepen.io/chriddyp/pen/bWLwgP.css',
EXTERNAL_STYLE_SHEETS = [dbc.themes.CERULEAN]

# Update interval, second, update time interval of runnable object
UPDATE_INTERVAL = 1

# showed in runnable page 
MAX_STEP = 100
MAX_CHECKPOINT_EVERY = 10
MAX_NUMBER_WIDGETS = 4
DEFAULT_NUMBER_WIDGETS = 2

from negmas.gui.app.layouts.page_layout import MAIN_LAYOUT, DEFAULT_LAYOUT_RUNNABLE, DEFAULT_LAYOUT_NAMED

#  Home Page/ Main_LAYOUT
HOME_PAGE =  MAIN_LAYOUT

# Runnable Object Layout settings
# when add a new runnables object, 
# at the same time need to 
# allocate the LAYOUT of this object
# When do not allocate, the system 
# will use default_layout as Layout
# Runnable object
RUNNABLES = [
    'negmas.apps.scml.SCMLWorld',
    'negmas.situated.World',
    'negmas.sao.SAOMechanism',
    'negmas.mechanisms.Mechanism'
]

# Default configuration for runnable object
from pathlib import Path
from negmas.helpers import unique_name
from negmas import SAOMechanism, MappingUtilityFunction, AspirationNegotiator

tmp_path = Path("./tmp")
new_folder: Path = tmp_path / unique_name("empty", sep="")

DEFAULT_RUNNABLE_PARAMS = {
    "negmas.sao.SAOMechanism": {
        "outcomes": 10,
        "n_steps": 100,
        "offering_is_accepting": True,
        "avoid_ultimatum": False,
        "checkpoint_every": 2,
        "checkpoint_folder": new_folder,
        "checkpoint_filename": "SAOMechanism",
        "extra_checkpoint_info": None,
        "exist_ok": True,
        "single_checkpoint": False,
        "negotiators": [AspirationNegotiator, AspirationNegotiator, AspirationNegotiator],
        "mapping_utility_function": MappingUtilityFunction
    },
}
# Named object
NAMED = [
    'negmas.negotiators.Negotiator',
    'negmas.negotiators.PassThroughNegotiator',
    'negmas.negotiators.EvaluatorNegotiator',
    'negmas.negotiators.RealComparatorNegotiator',
    'negmas.negotiators.BinaryComparatorNegotiator',
    'negmas.negotiators.NLevelsComparatorNegotiator',
    'negmas.negotiators.RankerNegotiator',
    'negmas.negotiators.RankerWithWeightsNegotiator',
    'negmas.negotiators.SorterNegotiator',
]
# layouts
LAYOUTS = {
    'default_runnable_layout': DEFAULT_LAYOUT_RUNNABLE,
    'default_named_layout': DEFAULT_LAYOUT_NAMED,
    'negmas.apps.scml.SCMLWorld': DEFAULT_LAYOUT_RUNNABLE,
    'negmas.situated.World': DEFAULT_LAYOUT_RUNNABLE,
    'negmas.sao.SAOMechanism': DEFAULT_LAYOUT_RUNNABLE,
    'negmas.mechanisms.Mechanism': DEFAULT_LAYOUT_RUNNABLE,
    'negmas.negotiators.Negotiator': DEFAULT_LAYOUT_NAMED,
    'negmas.negotiators.PassThroughNegotiator': DEFAULT_LAYOUT_NAMED,
    'negmas.negotiators.EvaluatorNegotiator': DEFAULT_LAYOUT_NAMED,
    'negmas.negotiators.RealComparatorNegotiator': DEFAULT_LAYOUT_NAMED,
    'negmas.negotiators.BinaryComparatorNegotiator': DEFAULT_LAYOUT_NAMED,
    'negmas.negotiators.NLevelsComparatorNegotiator': DEFAULT_LAYOUT_NAMED,
    'negmas.negotiators.RankerNegotiator': DEFAULT_LAYOUT_NAMED,
    'negmas.negotiators.RankerWithWeightsNegotiator': DEFAULT_LAYOUT_NAMED,
    'negmas.negotiators.SorterNegotiator': DEFAULT_LAYOUT_NAMED,
}


# Setting for cache 
CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    # Note that filesystem cache doesn't work on systems with ephemeral
    # filesystems like Heroku.
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory',

    # should be equal to maximum number of users on the app at a single time
    # higher numbers will store more data in the filesystem / redis cache
    'CACHE_THRESHOLD': 200
}