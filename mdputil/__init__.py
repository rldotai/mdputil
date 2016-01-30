import inspect

from .linalg_util import *
from .solve import *


__version__ = "0.1.0"

# don't export modules unless they're actually wanted
_whitelist = []
__all__ = [name for name, x in locals().items() if not name.startswith('_') and
           (not inspect.ismodule(x) or x in _whitelist)]

__all__.append(__version__)