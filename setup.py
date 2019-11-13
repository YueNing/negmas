from setuptools import setup

def get_version(filename):
    import ast
    version = None
    with open(filename) as f:
        for line in f:
            if line.startswith('__version__'):
                version = ast.parse(line).body[0].value.s
                break
        else:
            raise ValueError('No version found in %r.' % filename)
    if version is None:
        raise ValueError(filename)
    return version

version = get_version(filename='gym_duckietown/__init__.py')

setup(name='gym_negmas',
      version=version,
      install_requires=['gym']  # And any other dependencies foo needs
      keywords='negmas, environment, agent, rl, openaigym, gym',
      install_requires=[
            'gym',
            'negmas',
            'pyglet',
      ]
)