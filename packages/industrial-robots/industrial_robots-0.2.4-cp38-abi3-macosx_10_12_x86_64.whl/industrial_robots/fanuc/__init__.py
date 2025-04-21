"""
This module provides classes representing FANUC robots and their kinematics.
"""

from ..industrial_robots import _fanuc

# Global import of all functions
for name in [n for n in dir(_fanuc) if not n.startswith("_")]:
    globals()[name] = getattr(_fanuc, name)
