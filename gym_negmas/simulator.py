# coding=utf-8
from __future__ import division

from collections import namedtuple
from ctypes import POINTER
from dataclasses import dataclass
from typing import Tuple

@dataclass 
class DoneRewardInfo:
    """
    setup done reward information as a dataclass
    """
    done: bool
    done_why: str
    done_code: str
    reward: float

import gym 
import yaml 
from gym.utils import seeding 

# Objects utility code 
from .objects import WorldObj, TrafficLightObj, CarbotObj, CarObj, FactoryObj
# Graphics utility code
from .objmesh import *
# Randomization code
from .randomization import Randomizer
# self defined spaces inherite from gym.spaces
from gym_negmas.envs import spaces

# Rendering window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# Camera image size
DEFAULT_CAMERA_WIDTH = 640
DEFAULT_CAMERA_HEIGHT = 480

# Blue sky horizon color 
BLUE_SKY_COLOR = np.array([0.64, 0.71, 0.28])

# Ground/floor color
GROUND_COLOR = np.array([0.15, 0.15, 0.15])

# Angle at which the camera is pitched downwards
CAMERA_ANGLE = 15

DEFAULT_FRAMERATE = 30

DEFAULT_MAX_STEPS = 1500

DEFAULT_MAP_NAME = 'udem1'

# Factory propose or reject as action
DEFAULT_FRAME_SKIP = 10

class Simulator(gym.Env):
    """
    Simple factory simulator to test RL training
    Draws a Supply Chain ManagementWorld using OpenGL, and siumates basic business behaviors
    Such as: Autonomous Negotiation and Supply Chain combine with Negmas
    """

    metadata = {
        'render.modes': ['human', 'rgb_array', 'app'],
        'video.frames_per_second': 30
    }

    def __init__(
        self,
        map_name = DEFAULT_MAP_NAME,
        max_steps = DEFAULT_MAX_STEPS,
        frame_rate = DEFAULT_FRAMERATE,
        frame_skip = DEFAULT_FRAME_SKIP,
        camera_width = DEFAULT_CAMERA_WIDTH,
        camera_height = DEFAULT_CAMERA_HEIGHT,
        full_transparency = False,
        seed = None,
        distortion = False,
        randomize_maps_on_reset = False,
         
    ):
        """
        :param
        """
        # initialize the RNG
        self.seed_value = seed
        self.seed(seed=self.seed_value)

        # If true, then we publish all transparency information
        # here mean all the factory know the preference of opponent
        self.full_transparency = full_transparency

        # full map file path, set in _load_map()
        self.map_file_path = None

        # The parsed content of the map_file
        self.map_data = None

        # Maximum number of steps per episode
        self.max_steps = max_steps 

        # Frame rate to run at 
        self.frame_rate = frame_rate
        self.delte_time = 1.0 / self.frame_rate

        # Number of frames to skip per action
        self.frame_skip = frame_skip

        # Produce graphical output 
        self.graphics = True 
        
        # 3 disrete value represente ['go_up', 'go_down', 'stay'] [0, 1, 2]
        self.action_sapce = spaces.Discrete(3)

        self.camera_width = camera_width
        self.camera_height = camera_height

        # Observe space we observe here ubs and time defined in paper
        self.observation_space = spaces.Dict(spaces={
            'ub(wat)':spaces.Discrete(10),
            'ub(wbt)':spaces.Discrete(10),
            'ub(wat-1)':spaces.Discrete(10),
            'ub(wbt-1)':spaces.Discrete(10),
            'time':spaces.Discrete(n=self.max_steps),
        })

        # reward defined here as maximum utility [0, 1]
        self.reward_range = (0, 1) 
        
        # Window for displaying the environment to humans 
        self.window = None 

        import pyglet 
        # invisble window to render into(shadow OpenGL context)
        self.shadow_window = pyglet.window.Window(width=1, height=1, visible=False)

        # For displaying text
        self.text_label = pyglet.text.Lable(
            font_name="Arial",
            font_size=14,
            x=5,
            y=WINDOW_HEIGHT - 19
        )

        # create a frame buffer object for observation
        self.multi_fbo, self.final_fbo = create_frame_buffers(
            self.camera_width,
            self.camera_height,
            4
        )

        # save text and image into file (for observation) or render into image
        self.text = {}
        self.observation_file_path = None
        self.img_array = np.zeros(shape=(WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)

        # create a frame buffer object for human rendering
        self.multi_fbo_human, self.final_fbo_human = create_frame_buffers(
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
            4
        )

        # Array to render the image into (for human rendering)
        self.img_array_human = np.zeros(shape=(WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)

        # load the map
        self._load_map(map_name)

        self.randomize_maps_on_reset = randomize_maps_on_reset

        # initialize the state
        self.reset()

        self.last_action = np.array([None])
        
    def _load_map(self, map_name):
        """
        Load the map layout from a yaml file
        """

        # store the map name
        self.map_name = map_name

        # Get the full map file path
        self.map_file_path = get_file_path('maps', map_name, 'yaml')

        logger.debug(f'loading map file {self.map_file_path}')
        with open(self.map_file_path, 'r') as f:
            self.map_data = yaml.load(f, loader=yaml.Loader)
        
        self._interpret_map(self.map_data)
    
    def _interpret_map(self, map_data: dict):
        if not 'tile_size' in map_data:
            msg = 'Must now include explicit tile_size in the map data.'
            raise ValueError(msg)
        
        self.road_tile_size = map_data['tile_size']
        self._init_vlists()

        tiles = map_data['tiles']
        assert len(tiles) > 0
        assert len(tiles[0]) > 0

        # Create the grid
        self.grid_height = len(tiles)
        self.grid_width = len(tiles[0])
        self.grid = [None] * self.grid_width * self.grid_height

        # We keep a separate list of drivable titles
        self.drivable_titles = []

         # For each row in the grid
        for j, row in enumerate(tiles):
            msg = "each row of tiles must have the same length"
            if len(row) != self.grid_width:
                raise Exception(msg)

            # For each tile in this row
            for i, tile in enumerate(row):
                tile = tile.strip()

                if tile == 'empty':
                    continue

                if '/' in tile:
                    kind, orient = tile.split('/')
                    kind = kind.strip(' ')
                    orient = orient.strip(' ')
                    angle = ['S', 'E', 'N', 'W'].index(orient)
                    drivable = True
                elif '4' in tile:
                    kind = '4way'
                    angle = 2
                    drivable = True
                else:
                    kind = tile
                    angle = 0
                    drivable = False

                tile = {
                    'coords': (i, j),
                    'kind': kind,
                    'angle': angle,
                    'drivable': drivable
                }

                self._set_tile(i, j, tile)

                if drivable:
                    tile['curves'] = self._get_curve(i, j)
                    self.drivable_tiles.append(tile)
            
            self.mesh = ObjMesh.get('carbot')
            self._load_objects(map_data)
            
            # Get the starting tile from the map, if specified
            self.start_tile = None
            if 'start_tile' in map_data:
                coords = map_data['start_tile']
                self.start_tile = self._get_tile(*coords)
    

    def _init_vlists(self):
        import pyglet
        # create the vertex for our road quad
        # Note: the vertices are centered around the origin so we can easily
        # roate the titles about their center
        half_size = self.road_tile_size / 2
        verts = [
            -half_size, 0.0, -half_size,
            half_size, 0.0, -half_size,
            half_size, 0.0, half_size,
            -half_size, 0.0, half_size,
        ]

        textCoords = [
            1.0, 0.0,
            0.0, 0.0,
            0.0, 1.0,
            1.0, 1.0
        ]
        self.road_vlist = pyglet.graphics.vertex_list(4, ('v3f', verts), ('t2f', texCoords))
        verts = [
            -1, -0.8, 1,
            -1, -0.8, -1,
            1, -0.8, -1,
            1, -0.8, 1
        ]
        self.ground_vlist = pyglet.graphics.vertex_list(4, ('v3f', verts))

    def _load_objects(self, map_data):
        # Create the objects array
        self.objects = []

        # The corners for every object, regardless if collidable or not
        self.object_corners = []

        # Arrays for checking collisions with N static objects
        # (Dynamic objects done separately)
        # (N x 2): Object position used in calculating reward
        self.collidable_centers = []

        # (N x 2 x 4): 4 corners - (x, z) - for object's boundbox
        self.collidable_corners = []

        # (N x 2 x 2): two 2D norms for each object (1 per axis of boundbox)
        self.collidable_norms = []

        # (N): Safety radius for object used in calculating reward
        self.collidable_safety_radii = []

        # For each object
        for obj_idx, desc in enumerate(map_data.get('objects', [])):
            kind = desc['kind']

            pos = desc['pos']
            x, z = pos[0:2]
            y = pos[2] if len(pos) == 3 else 0.0

            rotate = desc['rotate']
            optional = desc.get('optional', False)

            pos = self.road_tile_size * np.array((x, y, z))

            # Load the mesh
            mesh = ObjMesh.get(kind)

            if 'height' in desc:
                scale = desc['height'] / mesh.max_coords[1]
            else:
                scale = desc['scale']
            assert not ('height' in desc and 'scale' in desc), "cannot specify both height and scale"

            static = desc.get('static', True)

            obj_desc = {
                'kind': kind,
                'mesh': mesh,
                'pos': pos,
                'scale': scale,
                'y_rot': rotate,
                'optional': optional,
                'static': static,
            }

            # obj = None
            if static:
                if kind == "trafficlight":
                    obj = TrafficLightObj(obj_desc, self.domain_rand, SAFETY_RAD_MULT)
                else:
                    obj = WorldObj(obj_desc, self.domain_rand, SAFETY_RAD_MULT)
            else:
                if kind == "carbot":
                    obj = CarbotObj(obj_desc, self.domain_rand, SAFETY_RAD_MULT, WHEEL_DIST,
                                       ROBOT_WIDTH, ROBOT_LENGTH)
                elif kind == "car":
                    obj = CarObj(obj_desc, self.domain_rand, SAFETY_RAD_MULT, self.road_tile_size)
                else:
                    msg = 'I do not know what object this is: %s' % kind
                    raise Exception(msg)

            self.objects.append(obj)

            # Compute collision detection information

            # angle = rotate * (math.pi / 180)

            # Find drivable tiles object could intersect with
            possible_tiles = find_candidate_tiles(obj.obj_corners, self.road_tile_size)

            # If the object intersects with a drivable tile
            if static and kind != "trafficlight" and self._collidable_object(
                    obj.obj_corners, obj.obj_norm, possible_tiles
            ):
                self.collidable_centers.append(pos)
                self.collidable_corners.append(obj.obj_corners.T)
                self.collidable_norms.append(obj.obj_norm)
                self.collidable_safety_radii.append(obj.safety_radius)

        # If there are collidable objects
        if len(self.collidable_corners) > 0:
            self.collidable_corners = np.stack(self.collidable_corners, axis=0)
            self.collidable_norms = np.stack(self.collidable_norms, axis=0)

            # Stack doesn't do anything if there's only one object,
            # So we add an extra dimension to avoid shape errors later
            if len(self.collidable_corners.shape) == 2:
                self.collidable_corners = self.collidable_corners[np.newaxis]
                self.collidable_norms = self.collidable_norms[np.newaxis]

        self.collidable_centers = np.array(self.collidable_centers)
        self.collidable_safety_radii = np.array(self.collidable_safety_radii)

    def step(self):
        pass
    
    def reset(self):
        pass
    
    def render(self):
        pass
    
    def seeding(self):
        pass
    
def create_frame_buffers(width, height, num_samples):
    """Create the frame buffer objects"""
    from pyglet import gl

    # Create a frame buffer (rendering target)
    multi_fbo = gl.GLuint(0)
    gl.glGenFramebuffers(1, byref(multi_fbo))
    gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, multi_fbo)

    # The try block here is because some OpenGL drivers
    # (Intel GPU drivers on macbooks in particular) do not
    # support multisampling on frame buffer objects
    try:
        if not gl.gl_info.have_version(major=3, minor=2):
            raise Exception('OpenGL version 3.2+ required for \
                            GL_TEXTURE_2D_MULTISAMPLE')

        # Create a multisampled texture to render into
        fbTex = gl.GLuint(0)
        gl.glGenTextures( 1, byref(fbTex))
        gl.glBindTexture(gl.GL_TEXTURE_2D_MULTISAMPLE, fbTex)
        gl.glTexImage2DMultisample(
            gl.GL_TEXTURE_2D_MULTISAMPLE,
            num_samples,
            gl.GL_RGBA32F,
            width,
            height,
            True
        )
        gl.glFramebufferTexture2D(
                gl.GL_FRAMEBUFFER,
                gl.GL_COLOR_ATTACHMENT0,
                gl.GL_TEXTURE_2D_MULTISAMPLE,
            fbTex,
            0
        )

        # Attach a multisampled depth buffer to the FBO
        depth_rb = gl.GLuint(0)
        gl.glGenRenderbuffers(1, byref(depth_rb))
        gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, depth_rb)
        gl.glRenderbufferStorageMultisample(gl.GL_RENDERBUFFER, num_samples, gl.GL_DEPTH_COMPONENT, width, height)
        gl.glFramebufferRenderbuffer(gl.GL_FRAMEBUFFER, gl.GL_DEPTH_ATTACHMENT, gl.GL_RENDERBUFFER, depth_rb)

    except:
        logger.debug('Falling back to non-multisampled frame buffer')

        # Create a plain texture texture to render into
        fbTex = gl.GLuint(0)
        gl.glGenTextures( 1, byref(fbTex))
        gl.glBindTexture(gl.GL_TEXTURE_2D, fbTex)
        gl.glTexImage2D(
            gl.GL_TEXTURE_2D,
            0,
            gl.GL_RGBA,
            width,
            height,
            0,
            gl.GL_RGBA,
            gl.GL_FLOAT,
            None
        )
        gl.glFramebufferTexture2D(
            gl.GL_FRAMEBUFFER,
            gl.GL_COLOR_ATTACHMENT0,
            gl.GL_TEXTURE_2D,
            fbTex,
            0
        )

        # Attach depth buffer to FBO
        depth_rb = gl.GLuint(0)
        gl.glGenRenderbuffers(1, byref(depth_rb))
        gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, depth_rb)
        gl.glRenderbufferStorage(gl.GL_RENDERBUFFER, gl.GL_DEPTH_COMPONENT, width, height)
        gl.glFramebufferRenderbuffer(gl.GL_FRAMEBUFFER, gl.GL_DEPTH_ATTACHMENT, gl.GL_RENDERBUFFER, depth_rb)

    # Sanity check
    import pyglet
    if pyglet.options['debug_gl']:
      res = gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER)
      assert res == gl.GL_FRAMEBUFFER_COMPLETE

    # Create the frame buffer used to resolve the final render
    final_fbo = gl.GLuint(0)
    gl.glGenFramebuffers(1, byref(final_fbo))
    gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, final_fbo)

    # Create the texture used to resolve the final render
    fbTex = gl.GLuint(0)
    gl.glGenTextures(1, byref(fbTex))
    gl.glBindTexture(gl.GL_TEXTURE_2D, fbTex)
    gl.glTexImage2D(
        gl. GL_TEXTURE_2D,
        0,
        gl.GL_RGBA,
        width,
        height,
        0,
        gl. GL_RGBA,
        gl.GL_FLOAT,
        None
    )
    gl.glFramebufferTexture2D(
            gl.GL_FRAMEBUFFER,
            gl.GL_COLOR_ATTACHMENT0,
            gl.GL_TEXTURE_2D,
        fbTex,
        0
    )
    import pyglet
    if pyglet.options['debug_gl']:
      res = gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER)
      assert res == gl.GL_FRAMEBUFFER_COMPLETE

    # Enable depth testing
    gl.glEnable(gl.GL_DEPTH_TEST)

    # Unbind the frame buffer
    gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

    return multi_fbo, final_fbo



if __name__ == '__main__':

    simulator = Simulator()