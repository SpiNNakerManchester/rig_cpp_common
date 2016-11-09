"""A command-line utility which prints the path to rig_cpp_common.
For use by plugins etc to find make files etc.

Installed as "rig_cpp_common_path" by setuptools.
"""

import os.path
from rig_cpp_common import __file__ as f
import sys

def main(args=None):
    print(os.path.dirname(f))
    return 0

if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
