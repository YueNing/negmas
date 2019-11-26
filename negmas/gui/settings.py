"""
Basic config file, 
Layout: layout ratio
"""

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from negmas.gui.layout_style import DEFAULT_LAYOUT

# Default System Setting
LAYOUT_PARAMS = {
    "left":{"size": 4, "offset": 1},
    "right":{"size": 8, "layout":{"left":{"scale": 6}, "right":{"scale":6}}}
}

# layouts
LAYOUTS = {
    'default_layout': DEFAULT_LAYOUT, 
    'negmas.apps.scml.SCMLWorld': DEFAULT_LAYOUT,
    'negmas.situated.World': DEFAULT_LAYOUT,
    'negmas.mechanisms.Mechanism': DEFAULT_LAYOUT
}

# Runnable object
RUNNABLES = [
    'negmas.apps.scml.SCMLWorld',
    'negmas.situated.World',
    'negmas.mechanisms.Mechanism',
]

# Update interval, second, update time interval of runnable object
UPDATE_INTERVAL = 1

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