from software_release.utils import load
from .. import Node

# Import all class implementing the BaseCommand, inside this module's directory
load(Node)


# Probably we do not need the __all__ to be defined
# simple do in client code 'import node_components'

# modules = glob.glob(join(dirname(__file__), "*.py"))
# __all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

