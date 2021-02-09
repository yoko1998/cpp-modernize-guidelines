# https://docs.python-guide.org/writing/structure/
# https://docs.python-guide.org/writing/tests/

# To give the individual tests import context, create a tests/context.py file:
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import megasecret

# Then, within the individual test modules, import the module like so:
#    from .context import sample
# This will always work as expected, regardless of installation method.
