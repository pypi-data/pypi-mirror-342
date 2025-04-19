"""
pstatstools: A demonstration package for statistical analysis.

This package provides tools for sampling and analysis. The main sample
function is exposed directly at the package level for convenience.
"""

from .samples import sample

from . import distributions
from . import samples

__all__ = [
    # Functions
    'sample',
    
    # Submodules
    'distributions',
    'samples',
    'inferential'
]